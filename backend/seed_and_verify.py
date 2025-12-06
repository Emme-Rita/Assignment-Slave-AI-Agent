from app.db.session import SessionLocal, engine, Base
from app.models.conversation import Conversation
import uuid
import json
import requests

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_and_test():
    db = SessionLocal()
    try:
        print("1. Seeding Database...")
        test_id = str(uuid.uuid4())
        fake_response = {
            "id": test_id,
            "title": "Test Conversation",
            "question": "Test Question",
            "answer": "Test Answer",
            "summary": "Summary",
            "note": "Note",
            "more": "More"
        }
        
        item = Conversation(
            id=test_id,
            title="Seeded Test Conversation",
            prompt="This is a seeded test prompt",
            response_json=json.dumps(fake_response)
        )
        db.add(item)
        db.commit()
        print(f"   Seeded ID: {test_id}")
        
    finally:
        db.close()

    print("\n2. Verifying via API...")
    try:
        response = requests.get("http://localhost:8000/api/v1/history")
        if response.status_code == 200:
            history = response.json()
            found = False
            for h in history:
                if h["id"] == test_id:
                    print(f"   ✅ Found seeded item via API: {h['title']}")
                    found = True
                    break
            if not found:
                print("   ❌ Seeded item NOT found in API response.")
                print(f"   Response: {history}")
        else:
             print(f"   ❌ API connection failed: {response.status_code}")
             
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

if __name__ == "__main__":
    seed_and_test()
