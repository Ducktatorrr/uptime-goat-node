import logging
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file, if present
load_dotenv()

# Set up logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Fetch environment variables so standalone can also be used
GOAT_TOKEN = os.getenv("GOAT_TOKEN")
ENDPOINTS = ["https://hellogoat.cryptards.lol/report", "https://supgoat.cryptards.lol/report"]

# Function to send the request using requests because it's cooler
def send_request():
    if not GOAT_TOKEN or len(GOAT_TOKEN) != 32 or not all(c in '0123456789abcdef' for c in GOAT_TOKEN.lower()):
        logging.error("GOAT_TOKEN must be a valid 32-character hexadecimal value")
        return

    for url in ENDPOINTS:
        logging.info(f"Submitting request to {url}")

        # Prepare the payload
        payload = json.dumps({'goat_id': GOAT_TOKEN})

        # Set the headers
        headers = {
            'Content-type': 'application/json'
        }

        # Send the POST request to each endpoint
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=30)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response JSON
                response_data = response.json()

                # Extract and format the relevant fields for better readability
                formatted_response = (
                    f"Name: {response_data.get('name')}\n"
                    f"Time: {response_data.get('time')}\n"
                    f"Consecutives: {response_data.get('consecutives')}\n"
                    f"Locked Rewards: {response_data.get('locked_rewards')}\n"
                    f"Unlocked Rewards: {response_data.get('unlocked_rewards')}"
                )

                # Log the beautified response
                logging.info(f"Request successful from {url}:\n{formatted_response}")

                # Optionally log the raw response if needed
                logging.debug(f"Raw response from {url}: {response.text}")

            else:
                logging.error(f"Request failed with status {response.status_code} from {url}: {response.text}")
        except requests.exceptions.RequestException as err:
            logging.error(f"Error during request to {url}: {err}")

# Entry point of the script
if __name__ == '__main__':
    if not GOAT_TOKEN:
        logging.error("GOAT_TOKEN is not defined. Please set the GOAT_TOKEN environment variable.")
    else:
        logging.info("⚙️ Sending goat report")
        send_request()
