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
        # gemini-flash-latest is explicitly listed in available models
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.audio_model = genai.GenerativeModel('gemini-flash-latest')
    
    async def generate_response(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None,
        audio_data: Optional[dict] = None,
        student_level: Optional[str] = None,
        department: Optional[str] = None,
        style_instruction: Optional[str] = None
    ) -> str:
        """
        Generate AI response based on prompt, file content, optional context, and audio.
        
        Args:
            prompt: User's instruction/question
            file_content: Extracted text from uploaded files
            context: Additional context (e.g., from research)
            audio_data: Dict containing 'data' (bytes) and 'mime_type' (str)
            student_level: Academic qualification level
            department: Field of study
        """
        try:
            # Build the prompt parts
            parts = []
            
            # Add persona/context based on student profile
            if student_level or department:
                profile_context = "Role Context:\n"
                if student_level:
                    profile_context += f"You are writing for a {student_level} level student. Adjust complexity accordingly.\n"
                if department:
                    profile_context += f"The field of study is {department}. Use appropriate terminology.\n"
                parts.append(profile_context)

            if style_instruction:
                parts.append(f"STYLE INSTRUCTION (MIMIC THIS AUTHOR):\n{style_instruction}\n")

            if context:
                parts.append(f"Research Context:\n{context}\n")
            
            if file_content:
                parts.append(f"Assignment Content:\n{file_content}\n")
            
            parts.append(f"User Instructions:\n{prompt}")
            
            parts.append("""
            IMPORTANT: Follow these strict instructions:
            1. You must return the response in valid JSON format with the following structure.
            2. The content of 'answer' MUST be written in 100% natural, human-like language. 
            3. Do NOT use phrases like "As an AI", "Based on the provided text", "Here is the solution", "In conclusion". 
            4. Do NOT mention that you are an AI or that this is an AI-generated response.
            5. Write directly as if you are a student submitting the work.
            6. Vary sentence structure and length to avoid AI detection patterns.
            7. CRITICAL: Identify and solve ALL distinct questions, tasks, or sections found in the content. Do not summarize; provide the full solution for each part. Use markdown headers to separate different questions/sections within the 'answer' field.

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
            raise Exception(f"AI Service Error: {str(e)}")
    
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
