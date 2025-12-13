import os
from dotenv import load_dotenv
import google.generativeai as genai
from tavily import TavilyClient
import asyncio

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

print(f"Loaded GEMINI_API_KEY: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:] if GEMINI_API_KEY else 'None'}")
print(f"Loaded TAVILY_API_KEY: {TAVILY_API_KEY[:4]}...{TAVILY_API_KEY[-4:] if TAVILY_API_KEY else 'None'}")

async def test_gemini():
    print("\nTesting Gemini API...")
    if not GEMINI_API_KEY:
        print("FAIL: No Gemini Key found.")
        return

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = await model.generate_content_async("Test payload")
        print("SUCCESS: Gemini API is working.")
    except Exception as e:
        print(f"FAIL: Gemini Error: {e}")

def test_tavily():
    print("\nTesting Tavily API...")
    if not TAVILY_API_KEY:
        print("FAIL: No Tavily Key found.")
        return

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query="Test")
        print("SUCCESS: Tavily API is working.")
    except Exception as e:
        print(f"FAIL: Tavily Error: {e}")

async def main():
    await test_gemini()
    test_tavily()

if __name__ == "__main__":
    asyncio.run(main())
