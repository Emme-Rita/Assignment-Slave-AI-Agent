"""
Simple test to verify the assignment endpoint works with a PDF-like text file
"""
import requests

BASE_URL = "http://localhost:8000"

def test_assignment_endpoint():
    print("Testing assignment analysis endpoint...")
    
    # Create a simple test content
    test_content = """
    Math Problem:
    Calculate the area of a circle with radius 5 cm.
    Formula: A = πr²
    """
    
    # Prepare the request
    files = {
        'file': ('assignment.txt', test_content.encode(), 'text/plain')
    }
    data = {
        'prompt': 'Please solve this math problem and show your work',
        'use_research': 'false'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/assignment/analyze",
            files=files,
            data=data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"\nResponse:")
        print(response.json())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_assignment_endpoint()
