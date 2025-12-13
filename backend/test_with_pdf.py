"""
Create a test PDF and test the assignment endpoint
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests
import os

def create_test_pdf():
    """Create a simple test PDF with a math problem"""
    filename = "test_assignment.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Add content to PDF
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "Math Assignment")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Problem 1:")
    c.drawString(100, 680, "Calculate the area of a circle with radius 5 cm.")
    c.drawString(100, 660, "Use π = 3.14159")
    c.drawString(100, 620, "Problem 2:")
    c.drawString(100, 600, "What is the derivative of f(x) = x^2 + 3x + 2?")
    
    c.save()
    print(f"Created test PDF: {filename}")
    return filename

def test_with_pdf():
    """Test the assignment endpoint with the PDF"""
    pdf_file = create_test_pdf()
    
    print("\nTesting assignment endpoint with PDF...")
    
    with open(pdf_file, 'rb') as f:
        files = {'file': (pdf_file, f, 'application/pdf')}
        data = {
            'prompt': 'Please solve both math problems and show your work step by step',
            'use_research': 'false'
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/assignment/analyze",
            files=files,
            data=data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Success: {result.get('success')}")
            print(f"File processed: {result.get('file_processed')}")
            print(f"\nAI Response:\n{result.get('response')}")
        else:
            print(f"\n❌ Error: {response.text}")
    
    # Clean up
    if os.path.exists(pdf_file):
        os.remove(pdf_file)
        print(f"\nCleaned up test file: {pdf_file}")

if __name__ == "__main__":
    try:
        test_with_pdf()
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: You may need to install reportlab: pip install reportlab")
