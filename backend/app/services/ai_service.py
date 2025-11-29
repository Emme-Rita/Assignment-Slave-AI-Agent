import google.generativeai as genai
from app.core.config import settings
import PyPDF2
import docx
import io
from typing import Optional, List

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro-latest')
    
    async def generate_response(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Generate AI response based on prompt, file content, and optional context.
        
        Args:
            prompt: User's instruction/question
            file_content: Extracted text from uploaded files
            context: Additional context (e.g., from research)
        
        Returns:
            AI-generated response
        """
        try:
            # Build the full prompt
            full_prompt = self._build_prompt(prompt, file_content, context)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            raise Exception(f"AI Service Error: {str(e)}")
    
    def _build_prompt(
        self, 
        prompt: str, 
        file_content: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Build comprehensive prompt from components."""
        parts = []
        
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
