"""
Test script to verify API endpoints are working correctly
"""
import requests
import os

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_research():
    """Test research endpoint"""
    print("Testing research endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/v1/research/research",
        json={"query": "Python programming basics", "max_results": 3}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Query: {data['data']['query']}")
        print(f"Number of sources: {len(data['data']['sources'])}\n")
    else:
        print(f"Error: {response.text}\n")

def test_assignment_with_text():
    """Test assignment endpoint with a simple text file"""
    print("Testing assignment endpoint with text file...")
    
    # Create a simple test file
    test_content = "What is 2 + 2? Please solve this math problem."
    
    files = {
        'file': ('test.txt', test_content, 'text/plain')
    }
    data = {
        'prompt': 'Please solve the math problem in the file',
        'use_research': 'false'
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/assignment/analyze",
        files=files,
        data=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Response preview: {result.get('response', '')[:200]}...\n")
    else:
        print(f"Error: {response.text}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("API Testing Script")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_research()
        # test_assignment_with_text()  # Uncomment when ready to test
    except Exception as e:
        print(f"Error during testing: {e}")
