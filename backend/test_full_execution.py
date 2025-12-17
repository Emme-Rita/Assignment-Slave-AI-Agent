import requests
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    """Create a simple test PDF"""
    filename = "test_submission.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Test Assignment Submission")
    c.drawString(100, 700, "Question: Explain the importance of testing code.")
    c.save()
    return filename

def test_execution():
    pdf_file = create_test_pdf()
    url = "http://localhost:8000/api/v1/execute"
    
    # Use the email we verified earlier
    target_email = "atenuiemmerita@gmail.com"
    target_whatsapp = "1234567890" # Dummy number, user can update if they want real WA test

    print(f"Testing Full Execution Flow...")
    print(f"Target Email: {target_email}")
    print(f"Target WhatsApp: {target_whatsapp}")

    with open(pdf_file, 'rb') as f:
        files = {
            'file': (pdf_file, f, 'application/pdf')
        }
        data = {
            'prompt': 'Please analyze this test file and provide a brief answer.',
            'student_level': 'University',
            'department': 'Computer Science',
            'submission_format': 'pdf',
            'email': target_email,
            'whatsapp': target_whatsapp,
            'use_research': 'false', # Speed up test
            'stealth_mode': 'false'
        }
        
        try:
            print("Sending request... (This may take a moment)")
            response = requests.post(url, files=files, data=data) 
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ Execution Successful!")
                print(f"File Generated: {result.get('file_generated')}")
                print(f"Email Sent: {result.get('email_sent')}")
                print(f"WhatsApp Sent: {result.get('whatsapp_sent')}")
                
               #  print(f"\nResponse Data:\n{result.get('data')}")
            else:
                print(f"\n❌ Execution Failed: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"Error: {e}")
            
    # Cleanup
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

if __name__ == "__main__":
    test_execution()
