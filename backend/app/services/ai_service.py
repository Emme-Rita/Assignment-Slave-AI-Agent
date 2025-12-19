import os
from groq import Groq
from app.core.config import settings
import PyPDF2
import docx
import io
import json
import re
from typing import Optional, List

class AIService:
    def __init__(self):
        # Configure on init to pick up latest settings
        self._setup()
        self.model = "llama-3.3-70b-versatile"
    
    def _setup(self):
        """Configure Groq with latest settings."""
        # Force reload settings from .env
        settings.reload()
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            self.client = None
    
    async def generate_response(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None,
        audio_data: Optional[dict] = None, # Audio skipped in Groq migration for now
        student_level: Optional[str] = None,
        department: Optional[str] = None,
        style_instruction: Optional[str] = None,
        history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate AI response based on prompt, file content, optional context, and chat history using Groq.
        """
        # Ensure latest settings are loaded and configured
        self._setup()
        
        if not self.client:
            raise Exception("Groq API Key not configured. Please add GROQ_API_KEY to your .env file.")
        
        try:
            messages = []
            
            # 1. System Prompt & Output Constraints
            system_prompt = """
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
            """
            
            # Add role context
            if student_level or department:
                system_prompt += "\nRole Context:\n"
                if student_level:
                    system_prompt += f"You are writing for a {student_level} level student. Adjust complexity accordingly.\n"
                if department:
                    system_prompt += f"The field of study is {department}. Use appropriate terminology.\n"

            messages.append({"role": "system", "content": system_prompt})

            # 2. Contextual Information
            context_text = ""
            if style_instruction:
                context_text += f"STYLE INSTRUCTION (MIMIC THIS AUTHOR):\n{style_instruction}\n"
            if context:
                context_text += f"Research Context:\n{context}\n"
            if file_content:
                context_text += f"Assignment Content:\n{file_content}\n"
            
            if context_text:
                messages.append({"role": "user", "content": f"REFER TO THIS CONTEXT:\n{context_text}"})

            # 3. Chat History (if any)
            if history:
                for msg in history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
                
                messages.append({
                    "role": "user", 
                    "content": f"The user wants to refine the previous output. Apply the following changes to the EXISTING work: {prompt}\nIMPORTANT: You MUST return the ENTIRE updated assignment as a single complete output."
                })
            else:
                # 4. Current Instructions (Initial Request)
                messages.append({"role": "user", "content": f"User Instructions:\n{prompt}"})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                stream=False,
                response_format={"type": "json_object"} if "llama-3" in self.model else None
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            error_str = str(e)
            
            if "429" in error_str or "quota" in error_str.lower():
                raise Exception(
                    "Groq API Quota Exceeded. Please try again later or check your Groq plan."
                )
            
            raise Exception(f"AI Service Error (Groq): {error_str}")
    
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
