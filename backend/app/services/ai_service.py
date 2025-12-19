import google.generativeai as genai
from app.core.config import settings
import PyPDF2
import docx
import io
import json
from typing import Optional, List

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIService:
    def __init__(self):
        # We try to use gemini-2.0-flash-lite for higher quotas and better stability
        # Models to try in order of preference
        models = ['gemini-2.0-flash-lite', 'gemini-2.0-flash', 'gemini-flash-latest']
        
        self.model = None
        for m_name in models:
            try:
                self.model = genai.GenerativeModel(m_name)
                # Test the model immediately
                # self.model.generate_content("hi") # Removed to avoid burning quota during init
                break
            except:
                continue
        
        if not self.model:
            self.model = genai.GenerativeModel('gemini-flash-latest')
            
        self.audio_model = self.model
    
    async def generate_response(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None,
        audio_data: Optional[dict] = None,
        student_level: Optional[str] = None,
        department: Optional[str] = None,
        style_instruction: Optional[str] = None,
        history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate AI response based on prompt, file content, optional context, audio, and chat history.
        """
        try:
            # Build the prompt parts
            parts = []
            
            # 1. Base Context & Persona
            if student_level or department:
                profile_context = "Role Context:\n"
                if student_level:
                    profile_context += f"You are writing for a {student_level} level student. Adjust complexity accordingly.\n"
                if department:
                    profile_context += f"The field of study is {department}. Use appropriate terminology.\n"
                parts.append(profile_context)

            # 2. Reference Materials (Fixed Data)
            if style_instruction:
                parts.append(f"STYLE INSTRUCTION (MIMIC THIS AUTHOR):\n{style_instruction}\n")

            if context:
                parts.append(f"Research Context:\n{context}\n")
            
            if file_content:
                parts.append(f"Assignment Content:\n{file_content}\n")

            # 3. Chat History (if any)
            if history:
                parts.append("CONVERSATION SO FAR:\n")
                for msg in history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    parts.append(f"{role.upper()}: {content}\n")
                
                parts.append("\nREFINEMENT INSTRUCTION:\n")
                parts.append(f"The user wants to refine the previous output. Apply the following changes to the EXISTING work: {prompt}\n")
                parts.append("IMPORTANT: Do NOT just answer the refinement. You MUST return the ENTIRE updated assignment (original + new additions/changes) as a single complete output.\n")
            else:
                # 4. Current Instructions (Initial Request)
                parts.append(f"User Instructions:\n{prompt}")
            
            # 5. Output Constraints (System Instructions)
            parts.append("""
            IMPORTANT: Follow these strict instructions:
            1. You must return the response in valid JSON format with the following structure.
            2. The content of 'answer' MUST be written in 100% natural, human-like language. 
            3. Do NOT use phrases like "As an AI", "Based on the provided text", "Here is the solution", "In conclusion". 
            4. Do NOT mention that you are an AI or that this is an AI-generated response.
            5. Write directly as if you are a student submitting the work.
            6. Vary sentence structure and length to avoid AI detection patterns.
            7. **STRICT FORMATTING RULE**: Do NOT use LaTeX math syntax (e.g., `$$`, `\text{}`, `\frac{}`). Use standard text symbols (e.g., "A -> B", "x^2", "1/2").
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
            
            # Select model and add audio if present
            if audio_data:
                model = self.audio_model
                parts.append({
                    "mime_type": audio_data['mime_type'],
                    "data": audio_data['data']
                })
            else:
                model = self.model
            
            # Generate response
            response = await model.generate_content_async(parts)
            
            # Safety check: Verify valid response
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            elif response.candidates and response.candidates[0].finish_reason:
                # If finished but no text, usually safety block
                 return json.dumps({
                    "id": "safety_block",
                    "title": "Content Blocked",
                    "question": "Safety Filter Triggered",
                    "answer": f"The AI model refused to generate this content. Reason code: {response.candidates[0].finish_reason}. Please modify your prompt.",
                    "summary": "Safety restriction",
                    "note": "Try rephrasing or removing sensitive keywords."
                })
            else:
                 return json.dumps({
                    "id": "error",
                    "title": "Generation Error",
                    "question": "Unknown Error",
                    "answer": "The AI returned an empty response.",
                    "summary": "Error",
                    "note": "Please try again."
                })
        
        except Exception as e:
            error_str = str(e)
            
            # Handle quota exceeded errors with user-friendly message
            if "429" in error_str or "quota" in error_str.lower():
                raise Exception(
                    "AI Service Quota Exceeded: You've hit the daily request limit. "
                    "Please try again later (quota resets at midnight UTC) or upgrade your Gemini API plan. "
                    "Visit https://ai.google.dev/pricing for more information."
                )
            
            # Handle rate limit errors
            if "rate limit" in error_str.lower():
                raise Exception(
                    "AI Service Rate Limited: Too many requests in a short time. "
                    "Please wait a few seconds and try again."
                )
            
            # Generic error
            raise Exception(f"AI Service Error: {error_str}")
    
    def _build_prompt(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None,
        student_level: Optional[str] = None,
        department: Optional[str] = None
    ) -> str:
        """Build comprehensive prompt from components."""
        parts = []
        
        if student_level or department:
            if student_level:
                parts.append(f"Target Level: {student_level}")
            if department:
                parts.append(f"Department: {department}")
            parts.append("\n")
        
        if context:
            parts.append(f"Research Context:\n{context}\n")
        
        if file_content:
            parts.append(f"Assignment Content:\n{file_content}\n")
        
        parts.append(f"User Instructions:\n{prompt}")
        
        return "\n".join(parts)
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extract text from Word document."""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"DOCX extraction error: {str(e)}")

ai_service = AIService()
