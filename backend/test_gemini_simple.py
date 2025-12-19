import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load from current dir (.env in backend)
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    parts = [
        "Test Instruction",
        "IMPORTANT: Keep it short"
    ]

    try:
        response = model.generate_content(parts)
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error: {e}")
else:
    print("API Key not found in .env")
