import requests

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

def test_endpoint(url, method="GET", data=None, files=None):
    try:
        print(f"Testing {method} {url}...")
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=data, files=files)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# 1. Test Root
test_endpoint(f"{BASE_URL}/")

# 2. Test Health
test_endpoint(f"{BASE_URL}/health")

# 3. Test Assignment Execute (Simple)
# Using dummy data to just check if endpoint exists (should probably get 422 Unprocessable Entity or 500)
# But if it gets 404, we verify the path is wrong.
data = {
    "prompt": "Test Prompt",
    "student_level": "University",
    "department": "General",
    "submission_format": "docx",
    "use_research": "false"
}
test_endpoint(f"{BASE_URL}{API_PREFIX}/assignment/execute", method="POST", data=data)

# 4. Test Research
test_endpoint(f"{BASE_URL}{API_PREFIX}/research/research", method="POST", data='{"query": "test"}', 
              files=None) # sending json body for research
