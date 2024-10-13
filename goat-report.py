import logging
import os
import aiohttp
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file, if present
load_dotenv()

# Set up logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s %(levelname)s: %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

# Fetch environment variables
GOAT_TOKEN = os.getenv("GOAT_TOKEN", None)
ENDPOINTS = {
	"hellogoat": "https://hellogoat.cryptards.lol/report"
	"supgoat": "https://supgoat.cryptards.lol/report",
}


# Validate GOAT_TOKEN
if not GOAT_TOKEN or len(GOAT_TOKEN) != 32 or not all(c in '0123456789abcdef' for c in GOAT_TOKEN.lower()):
	logging.error("GOAT_TOKEN must be a valid 32-character hexadecimal value")
	exit(1)

# Initialize previous consecutive counts to detect RUGS
previous_consecutives = {key: 0 for key in ENDPOINTS}

# Function to send asynchronous requests
async def send_request(session, server_name, url, previous_consecutives):
	payload = {'goat_id': GOAT_TOKEN}
	headers = {'Content-type': 'application/json'}
	
	try:
		async with session.post(url, json=payload, headers=headers, timeout=30) as response:
			if response.status == 200:
				data = await response.json()
				miner_name = data.get("name", "Unknown")
				consecutive_number = data.get("consecutives", 0)
				deviation_ms = data.get("ms_deviation", 0)
				
				print(data)
	
				# Check if the consecutive count has reset from non-zero to zero
				# If this happens you're done
				if previous_consecutives[server_name] > 0 and consecutive_number == 0:
					logging.info(f"RUGGED 💀 on {server_name}")

				# Update the previous consecutive count
				previous_consecutives[server_name] = consecutive_number

				logging.info(f"{server_name} OK for {miner_name}, consecutive: {consecutive_number}, deviation: {deviation_ms}ms")
			else:
				logging.error(f"Request failed with status {response.status} from {url}")
	except aiohttp.ClientError as e:
		logging.error(f"Error during request to {url}: {e}")

# Main async loop to send requests
async def do_loop():
	loop = asyncio.get_event_loop()
	initial_timestamp = loop.time()  # Get the initial timestamp in seconds

	async with aiohttp.ClientSession() as session:
		while True:
			current_time = loop.time()  # Get the current event loop time in seconds

			# Calculate how much time has passed since the script started
			time_since_start = current_time - initial_timestamp
			time_to_next_interval = 60 - (time_since_start % 60)

			await asyncio.sleep(time_to_next_interval)
			
			logging.info("📯 Sending goat report")

			# Send requests concurrently
			tasks = [send_request(session, server_name, url, previous_consecutives) for server_name, url in ENDPOINTS.items()]
			await asyncio.gather(*tasks)


if __name__ == '__main__':
	try:
		logging.info("🐐 Starting goat report...")
		logging.info("😴 Sleeping for 60 seconds to prevent drift...")
		asyncio.run(do_loop())
	except KeyboardInterrupt:
		logging.info("Script interrupted by user. Exiting...")
