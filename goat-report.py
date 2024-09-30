import http.client
import sys
import json
import os

# Fetch the token from environment variables
hex_string = os.getenv('GOAT_TOKEN')

# Ensure the token is present
if not hex_string or len(hex_string) != 32 or not all(c in '0123456789abcdef' for c in hex_string.lower()):
    print("Error: The GOAT_TOKEN environment variable must be set and contain a 32-character hexadecimal value.")
    sys.exit(1)

# Define the endpoint URL and path
url = "supgoat.cryptards.lol"
path = "/report"

# Prepare the payload
payload = json.dumps({'goat_id': hex_string})

# Create a connection
conn = http.client.HTTPSConnection(url)

# Set the headers
headers = {
    'Content-type': 'application/json'
}

# Send the HTTP POST request
try:
    conn.request("POST", path, payload, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    print(data)
except Exception as e:
    print(f"Error sending request: {e}")
finally:
    conn.close()
