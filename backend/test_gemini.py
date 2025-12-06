
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv(dotenv_path='C:\\Users\\Placi\\OneDrive\\Desktop\\antigravity\\Assignment-Slave-AI-Agent-1\\backend\\.env')

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")

genai.configure(api_key=api_key)

async def test_model():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Testing gemini-1.5-flash...")
        response = model.generate_content("Hello, can you hear me?")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error testing gemini-1.5-flash: {e}")

    try:
        model = genai.GenerativeModel('gemini-pro')
        print("Testing gemini-pro...")
        response = model.generate_content("Hello, can you hear me?")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error testing gemini-pro: {e}")

    try:
        model = genai.GenerativeModel('gemini-flash-latest') 
        print("Testing gemini-flash-latest...")
        response = model.generate_content("Hello?")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error testing gemini-flash-latest: {e}")

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest') 
        print("Testing gemini-1.5-pro-latest...")
        response = model.generate_content("Hello?")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error testing gemini-1.5-pro-latest: {e}")

if __name__ == "__main__":
    asyncio.run(test_model())
