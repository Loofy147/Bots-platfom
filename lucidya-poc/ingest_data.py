import requests
import json

# URL of the nlp-worker's ingest endpoint
url = "http://localhost:8000/ingest"

# Path to the sample data file
data_file = "data/incoming/sample_data.json"

# Read the sample data from the file
with open(data_file, "r") as f:
    data = json.load(f)

# Send each item in the data to the ingest endpoint
for item in data:
    try:
        response = requests.post(url, json=item)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Successfully sent data: {item}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
