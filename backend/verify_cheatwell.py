"""
Test CheatWell Workflow Endpoints
"""
import requests
import json
import os
from reportlab.pdfgen import canvas

BASE_URL = "http://localhost:8000/api/v1"

def create_test_pdf(filename="verify_cheatwell.pdf"):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "CheatWell Test Assignment")
    c.drawString(100, 700, "What is the capital of France?")
    c.save()
    return filename

def test_submit_endpoint():
    print("\nTesting /submit Endpoint...")
    pdf_file = create_test_pdf()
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {
                'image': (pdf_file, f, 'application/pdf'),
            }
            
            # Note: We are testing with just a file (simulating image)
            response = requests.post(f"{BASE_URL}/submit", files=files)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON Structure:")
            print(json.dumps(data, indent=2))
            
            # Verify keys
            expected_keys = ["id", "title", "question", "answer", "summary", "note", "more"]
            missing_keys = [k for k in expected_keys if k not in data]
            
            if not missing_keys:
                print("✅ JSON structure matches requirements!")
            else:
                print(f"❌ Missing keys: {missing_keys}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Test Error: {e}")
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

if __name__ == "__main__":
    test_submit_endpoint()
