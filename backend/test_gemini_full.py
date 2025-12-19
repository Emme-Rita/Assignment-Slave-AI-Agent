import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

    # Mimic ai_service.py logic
    prompt = "test"
    student_level = "University"
    department = "General"
    context = "Some research context"
    file_content = None
    history = []
    
    parts = []
    
    # 1. Base Context
    profile_context = "Role Context:\n"
    profile_context += f"You are writing for a {student_level} level student. Adjust complexity accordingly.\n"
    profile_context += f"The field of study is {department}. Use appropriate terminology.\n"
    parts.append(profile_context)

    # 2. Context
    parts.append(f"Research Context:\n{context}\n")
    
    # 3. Instruction
    parts.append(f"User Instructions:\n{prompt}")
    
    # 4. Constraints
    parts.append("""
            IMPORTANT: Follow these strict instructions:
            1. You must return the response in valid JSON format with the following structure.
            2. The content of 'answer' MUST be written in 100% natural, human-like language. 
            3. Do NOT use phrases like "As an AI", "Based on the provided text", "Here is the solution", "In conclusion". 
            4. Do NOT mention that you are an AI or that this is an AI-generated response.
            5. Write directly as if you are a student submitting the work.
            6. Vary sentence structure and length to avoid AI detection patterns.
            7. **STRICT FORMATTING RULE**: Do NOT use LaTeX math syntax (e.g., $$, \\text{}, \\frac{}). Use standard text symbols (e.g., "A -> B", "x^2", "1/2").
            8. **DIRECT ANSWER ONLY**: Do NOT provide explanations, introductory filler ("Here is the answer"), or "meta-commentary". Just provide the solution/essay/code itself.
            9. **DIAGRAMS**: If the question involves a process, flow, or graph, YOU MUST PROVIDE A CLEAR TEXT-BASED DIAGRAM (ASCII Art) wrapped in triple backticks (```).

            JSON Structure:
            {
                "id": "unique_id",
                "title": "Assignment Title",
                "question": "The main question or topic identified",
                "answer": "The detailed answer/solution. This should be the full essay/code/calculation.",
                "summary": "A brief summary of the answer",
                "note": "Any important notes or warnings",
                "more": "Additional resources or related topics"
            }
            Do not include markdown formatting (like ```json) in the response, just the raw JSON string.
            """)

    print(f"DEBUG: parts list: {parts}")
    
    try:
        response = model.generate_content(parts)
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("API Key not found")
