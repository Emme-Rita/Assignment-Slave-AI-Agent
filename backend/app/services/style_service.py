import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class StyleService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro-latest')
    
    async def analyze_style(self, text_sample: str) -> str:
        """
        Analyzes the input text and returns a prompt instruction describing the specific writing style.
        """
        try:
            # We limit sample size to avoid token limits if sample is huge
            sample = text_sample[:5000] 
            
            prompt = f"""
            TASK: Analyze the writing style of the following text sample.
            
            GOAL: Create a specific instruction set that would help an AI mimic this exact author.
            
            FOCUS ON:
            1. Sentence structure (length, complexity, rhythm).
            2. Vocabulary level (simple, academic, flowery, technical).
            3. Tone (formal, casual, sarcastic, dry, enthusiastic).
            4. Common patterns (e.g. "frequently uses bullet points", "starts sentences with conjunctions").
            
            SAMPLE TEXT:
            {sample}
            
            OUTPUT:
            Return a concise paragraph starting with "Write in a style that..." 
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            print(f"Style analysis failed: {e}")
            return "Write in a balanced, clear academic tone."

style_service = StyleService()
