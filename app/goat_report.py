import logging
import os
import sys
import aiohttp
import asyncio
import json
from dotenv import load_dotenv

# Load environment variables from .env file, if present
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Fetch environment variables
GOAT_ID = os.getenv("GOAT_ID", None)
GOAT_KEY = os.getenv("GOAT_KEY", None)
ENDPOINTS_FILE_PATH = "/app/endpoints.json"


# Validate GOAT_ID and GOAT_KEY
def validate_hex(value, name):
    if (
        not value
        or len(value) != 32
        or not all(c in "0123456789abcdef" for c in value.lower())
    ):
        logging.error(f"{name} must be a valid 32-character hexadecimal value")
        sys.exit(1)


def precondition_check():
    if os.path.isfile(ENDPOINTS_FILE_PATH):
        logging.info(f"Using endpoints from local file: {ENDPOINTS_FILE_PATH}")
    else:
        logging.error("Endpoints file does not exist. Exiting...")
        sys.exit(1)


# Validate GOAT_ID and GOAT_KEY
validate_hex(GOAT_ID, "GOAT_ID")
validate_hex(GOAT_KEY, "GOAT_KEY")
precondition_check()


# Load the cached endpoints from the JSON file
def load_endpoints(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading endpoints from {file_path}: {e}")
        sys.exit(1)


# Function to send asynchronous requests
async def send_request(session, server_name, url, previous_consecutives):
    payload = {"goat_id": GOAT_ID, "goat_key": GOAT_KEY}
    headers = {"Content-type": "application/json"}

    try:
        async with session.post(
            url, json=payload, headers=headers, timeout=30
        ) as response:
            if response.status == 200:
                data = await response.json()
                miner_name = data.get("name", "Unknown")
                consecutive_number = data.get("consecutives", 0)
                deviation_ms = data.get("ms_deviation", 0)

                # If this happens you're done
                if previous_consecutives[server_name] > 0 and consecutive_number == 0:
                    logging.info(f"RUGGED 💀 on {server_name}")

                # Update the previous consecutive count
                previous_consecutives[server_name] = consecutive_number

                logging.info(
                    f"{server_name} OK for {miner_name}, "
                    f"consecutive: {consecutive_number}, "
                    f"deviation: {deviation_ms}ms"
                )
            else:
                logging.error(
                    f"Request failed with status {response.status} from {url}"
                )
    except asyncio.TimeoutError:
        logging.error(f"TimeoutError during request to {url}. Skipping...")
    except aiohttp.ClientError as e:
        logging.error(f"ClientError during request to {url}: {e}")


# Main async loop to send requests
async def do_loop():
    loop = asyncio.get_event_loop()
    # Get the initial timestamp in seconds
    initial_timestamp = loop.time()

    async with aiohttp.ClientSession() as session:
        while True:
            # Get the current event loop time in seconds
            current_time = loop.time()

            # Calculate how much time has passed since the script started
            time_since_start = current_time - initial_timestamp
            time_to_next_interval = 60 - (time_since_start % 60)

            # Load endpoints before each reporting cycle
            endpoints = load_endpoints(ENDPOINTS_FILE_PATH)
            previous_consecutives = {key: 0 for key in endpoints}
            await asyncio.sleep(time_to_next_interval)

            logging.info("📯 Sending goat report")

            # Send requests concurrently
            tasks = [
                send_request(session, server_name, url, previous_consecutives)
                for server_name, url in endpoints.items()
            ]
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        logging.info("🐐 Starting goat report...")
        logging.info("😴 Sleeping for 60 seconds to prevent drift...")
        asyncio.run(do_loop())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user. Exiting...")
