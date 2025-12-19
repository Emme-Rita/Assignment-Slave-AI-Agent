import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.services.ai_service import ai_service
from app.services.humanizer_service import humanizer_service

async def test_groq_integration():
    print("Testing Groq Integration...")
    
    # 1. Test AI Service
    prompt = "Write a short paragraph about the impact of AI on education."
    print(f"\nAI Service Test: '{prompt}'")
    try:
        response = await ai_service.generate_response(prompt=prompt, student_level="University")
        print("Response received:")
        print(response)
    except Exception as e:
        print(f"AI Service Error: {e}")

    # 2. Test Humanizer Service
    text_to_humanize = "Artificial intelligence will significantly change how students learn by providing personalized tutoring."
    print(f"\nHumanizer Service Test: '{text_to_humanize}'")
    try:
        humanized = await humanizer_service.humanize_text(text=text_to_humanize, student_level="University")
        print("Humanized text:")
        print(humanized)
    except Exception as e:
        print(f"Humanizer Service Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_groq_integration())
