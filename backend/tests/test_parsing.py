
import re
import json
import uuid

def test_extraction(ai_response_text):
    print(f"Testing input: {ai_response_text[:50]}...")
    try:
        cleaned_response = ai_response_text.replace("```json", "").replace("```", "").strip()
        response_json = json.loads(cleaned_response)
        print("Success (Direct JSON)")
        return response_json
    except json.JSONDecodeError:
        try:
            match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
            if match:
                response_json = json.loads(match.group())
                print("Success (Regex Extraction)")
                return response_json
            else:
                print("Failed (No JSON found)")
                return None
        except Exception as e:
            print(f"Failed (Exception: {e})")
            return None

def test_formatting(response_json):
    answer_text = response_json.get("answer", "Default Answer")
    title = response_json.get("title", "Assignment Submission")
    question = response_json.get("question", "")
    summary = response_json.get("summary", "")
    
    document_content = f"Title: {title}\n"
    if question:
        document_content += f"\nQuestion / Topic:\n{question}\n"
    
    document_content += f"\n{'-'*20}\n"
    document_content += f"\nAnswer:\n\n{answer_text}\n"
    
    if summary:
        document_content += f"\n{'-'*20}\nSummary:\n{summary}\n"
        
    print("\nGenerated Content Preview:")
    print("-" * 40)
    print(document_content)
    print("-" * 40)

# 1. Clean JSON
json_clean = '{"title": "Test", "answer": "Answer"}'
test_extraction(json_clean)

# 2. JSON with Markdown
json_md = '```json\n{"title": "Test MD", "answer": "Answer MD"}\n```'
test_extraction(json_md)

# 3. Dirty JSON (The User Issue)
json_dirty = 'Here is the result:\n{"title": "Dirty", "answer": "Real Answer", "question": "The Q"}\nHope this helps.'
extracted = test_extraction(json_dirty)
if extracted:
    test_formatting(extracted)

# 4. JSON with Nested Braces (Code)
json_nested = '{"title": "Code", "answer": "function test() { return true; }"}'
test_extraction(json_nested)
