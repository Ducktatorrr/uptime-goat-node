import logging
import os
import sys
import time
import requests
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Fetch environment variables
ENDPOINTS_URL = os.getenv("ENDPOINTS_URL")
ENDPOINTS_FILE_PATH = "/app/endpoints.json"


# Function to check if either the ENDPOINTS_URL is set or the file exists
def precondition_check():
    if ENDPOINTS_URL:
        logging.info(f"ENDPOINTS_URL is set: {ENDPOINTS_URL}")
    elif os.path.isfile(ENDPOINTS_FILE_PATH):
        logging.info(f"Using endpoints from local file: {ENDPOINTS_FILE_PATH}")
    else:
        logging.error("ENDPOINTS_URL not set and no local endpoints found. Exiting...")
        sys.exit(1)


# Let's make sure we have the endpoints before we start anything
precondition_check()


# Function to fetch the latest endpoints and update the JSON file
def fetch_and_update_endpoints():
    logging.info("🔦 Mission: get endpoints, status: started")
    try:
        # Fetch the latest endpoints
        response = requests.get(ENDPOINTS_URL, timeout=30)

        # Ensure the response is successful (status code 200)
        response.raise_for_status()

        # Parse the JSON response
        endpoints = response.json()

        # Some crazy person validation coming up
        # Validate the format of the endpoints (ensure it's a dictionary)
        if not isinstance(endpoints, dict):
            logging.error(
                "Mission failed: Invalid format received: " "Expected a dictionary."
            )
            return

        # Validate the URLs in the dictionary
        for key, value in endpoints.items():
            if (
                not isinstance(key, str)
                or not isinstance(value, str)
                or not value.startswith("http")
            ):
                logging.error(
                    "Mission failed: Invalid endpoint format for "
                    f"key: {key}, value: {value}."
                )
                return

        # Write the endpoints to a local JSON file
        with open(ENDPOINTS_FILE_PATH, "w") as f:
            json.dump(endpoints, f, indent=2)
        logging.info("⭐ Mission: get endpoints, status: completed")
        logging.info("😴 Agent Endpoint going off duty for 10 minutes")

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: Failed to fetch endpoints: {e}")
    except ValueError as e:
        logging.error(f"ValueError: Failed to parse JSON response: {e}")
    except OSError as e:
        logging.error(f"OSError: Write failed to {ENDPOINTS_FILE_PATH}: {e}")


# Main loop to fetch endpoints every 10 minutes
def do_loop():
    while True:
        fetch_and_update_endpoints()
        time.sleep(600)


if __name__ == "__main__":
    try:
        logging.info("🫡 Agent Endpoint at your service")
        do_loop()
    except KeyboardInterrupt:
        logging.info("🫡 Agent Endpoint signing off. Exiting...")
