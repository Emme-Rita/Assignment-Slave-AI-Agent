from app.db.session import SessionLocal, engine, Base
from app.models.conversation import Conversation
import uuid
import json
import requests
import time

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_and_test():
    print("1. Submitting Assignment WITH Notification Request...")
    # NOTE: Since we don't have real credentials, these will fail in the logs, but shouldn't crash the server.
    url = "http://localhost:8000/api/v1/submit"
    
    data = {
        "prompt": "Test notification prompt",
        "email": "test@example.com",
        "whatsapp_number": "1234567890"
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("   ✅ Submission accepted (Check server logs for email/whatsapp attempts)")
            result = response.json()
            print(f"   ID: {result.get('id')}")
        else:
            print(f"   ❌ Submission failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Network error: {e}")

if __name__ == "__main__":
    seed_and_test()
