"""
Test script for new endpoints: Email, WhatsApp, and Student Details
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_email_endpoint():
    print("\nTesting Email Endpoint...")
    url = f"{BASE_URL}/api/v1/email/send"
    payload = {
        "recipient": "student@example.com",
        "subject": "Assignment Results",
        "content": "Here are your assignment results.",
        "attachments": ["result.pdf"]
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_whatsapp_endpoint():
    print("\nTesting WhatsApp Endpoint...")
    url = f"{BASE_URL}/api/v1/whatsapp/send"
    payload = {
        "phone_number": "+1234567890",
        "message": "Your assignment is ready.",
        "media_url": "http://example.com/result.pdf"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_student_endpoint():
    print("\nTesting Student Details Endpoint...")
    url = f"{BASE_URL}/api/v1/student/details"
    payload = {
        "name": "Jane Doe",
        "matricule": "MAT123456",
        "department": "Computer Science",
        "level": "300"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting verification of new endpoints...")
    test_email_endpoint()
    test_whatsapp_endpoint()
    test_student_endpoint()
