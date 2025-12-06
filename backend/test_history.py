import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

print("Testing execute endpoint...")
data = {
    "prompt": "Test history save",
    "student_level": "University",
    "department": "Testing",
    "submission_format": "docx",
    "use_research": "false",
    "stealth_mode": "false"
}

response = requests.post(f"{BASE_URL}/execute", data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

print("\nWaiting 2 seconds...")
time.sleep(2)

print("\nTesting history endpoint...")
response2 = requests.get(f"{BASE_URL}/history")
print(f"Status: {response2.status_code}")
if response2.status_code == 200:
    print(f"Response: {response2.json()}")
else:
    print(f"Error: {response2.text}")
