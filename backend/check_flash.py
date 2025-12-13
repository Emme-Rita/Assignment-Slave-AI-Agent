"""
Test Gemini Flash Latest availability
"""
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def check_model():
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_model()
