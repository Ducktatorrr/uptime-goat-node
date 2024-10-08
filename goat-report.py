import logging
import time
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
ENDPOINTS = ["https://hellogoat.cryptards.lol/report","https://supgoat.cryptards.lol/report"]

# Function to send the request using requests because is cooler
def send_request():
	if not GOAT_TOKEN or len(GOAT_TOKEN) != 32 or not all(c in '0123456789abcdef' for c in GOAT_TOKEN.lower()):
		logging.error("GOAT_TOKEN must be a valid 32-character hexadecimal value")
		return

	for url in ENDPOINTS:
		logging.info("Submitting request to %s" % url)

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
				logging.info("Request successful from %s: %s" % (url, response.text))
			else:
				logging.error("Request failed with status %s from %s: %s" % (response.status_code, url, response.text))
		except requests.exceptions.RequestException as err:
			logging.error(f"Error during request to {url}: {err}")

# Main loop function
def do_loop():
	sleep_time = 60  # Fixed 60-second interval to mimic spacerabbits cron job behavior
	while True:
		logging.info("⚙️ Sending goat report")
		send_request()

		logging.info("Sleeping for %s seconds" % sleep_time)
		time.sleep(sleep_time)

# Entry point of the script
if __name__ == '__main__':
	if not GOAT_TOKEN:
		logging.error("GOAT_TOKEN is not defined. Please set the GOAT_TOKEN environment variable.")
	else:
		do_loop()
