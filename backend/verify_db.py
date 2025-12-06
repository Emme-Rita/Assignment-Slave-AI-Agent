import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_db_integration():
    print("1. Submitting Assignment to trigger DB save...")
    # Using the /submit endpoint
    url = f"{BASE_URL}/submit"
    
    # We can send just a prompt for a quick test
    data = {"prompt": "What is 2+2?"}
    
    # Needs to be multipart/form-data
    response = requests.post(url, data=data) 
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Success! ID: {result.get('id')}")
        assignment_id = result.get('id')
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return

    print("\n2. Checking History List...")
    time.sleep(1) # Give it a moment (though sqlite is sync usually)
    history_url = f"{BASE_URL}/history/"
    response = requests.get(history_url)
    
    if response.status_code == 200:
        history = response.json()
        print(f"   History Items: {len(history)}")
        found = False
        for item in history:
            print(f"   - {item['id']}: {item['title']} ({item['created_at']})")
            if item['id'] == assignment_id:
                found = True
        
        if found:
            print("   ✅ Created assignment found in history list.")
        else:
            print("   ❌ Created assignment NOT found in history list.")
    else:
        print(f"   Failed to list history: {response.status_code}")

    print(f"\n3. Retrieving Details for {assignment_id}...")
    detail_url = f"{BASE_URL}/history/{assignment_id}"
    response = requests.get(detail_url)
    
    if response.status_code == 200:
        detail = response.json()
        print(f"   ID: {detail['id']}")
        print(f"   Prompt: {detail['prompt']}")
        print(f"   Response keys: {detail.get('response', {}).keys()}")
        if detail['prompt'] == "What is 2+2?":
            print("   ✅ Details match submitted data.")
        else:
            print("   ❌ Details do not match.")
    else:
        print(f"   Failed to get details: {response.status_code}")

if __name__ == "__main__":
    test_db_integration()
