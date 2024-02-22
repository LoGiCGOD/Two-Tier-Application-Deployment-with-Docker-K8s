
import requests
import json
import random
import string
from concurrent.futures import ThreadPoolExecutor

# Function to generate random string
def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# Function to send a single request
def send_request(url, json_data):
    response = requests.post(url, data=json.dumps(json_data), headers={'Content-Type': 'application/json'})
    return response.status_code, response.text

# URL to send the requests
url = "http://192.168.49.2:80/users"

# Number of requests to send
num_requests = 500

# Generate random JSON data for all requests
json_data_list = [
    {"username": generate_random_string(20), "password": generate_random_string(12)}
    for _ in range(num_requests)
]

# Use ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit the requests to the executor
    futures = [executor.submit(send_request, url, json_data) for json_data in json_data_list]

    # Wait for all requests to complete
    responses = [future.result() for future in futures]

# Print response status codes and contents
for i, (status_code, content) in enumerate(responses, start=1):
    print(f"Request {i}: Status Code: {status_code}, Response Content: {content}")
