"""
Verify Communication Endpoints
Tests /send/gmail and /send/whatsapp
Note: These tests are expected to fail or return 500 if credentials are not configured in .env
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_email_endpoint():
    print("\nTesting /send/gmail Endpoint...")
    payload = {
        "recipient": "test@example.com",
        "subject": "Test Email",
        "content": "This is a test email from CheatWell backend.",
        "attachments": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/send/gmail", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Email Test Error: {e}")

def test_whatsapp_endpoint():
    print("\nTesting /send/whatsapp Endpoint...")
    payload = {
        "phone_number": "1234567890",
        "message": "Test message from CheatWell backend.",
        "media_url": None
    }
    
    try:
        response = requests.post(f"{BASE_URL}/send/whatsapp", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"WhatsApp Test Error: {e}")

if __name__ == "__main__":
    test_email_endpoint()
    test_whatsapp_endpoint()
