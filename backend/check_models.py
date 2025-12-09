import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print(f"Checking models with key: {api_key[:5]}...")

try:
    print("Available models supporting generateContent:")
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            count += 1
    if count == 0:
        print("No models found. Check API key permissions/region.")
except Exception as e:
    print(f"Error listing models: {e}")
