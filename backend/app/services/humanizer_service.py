import google.generativeai as genai
from app.core.config import settings
from typing import Optional

# Configure Gemini (re-using main config, but ideally could use a different model/config)
genai.configure(api_key=settings.GEMINI_API_KEY)

class HumanizerService:
    def __init__(self):
        # We use flash for speed/cost or pro for better reasoning. 
        # For "humanizing", sometimes a less perfect model is actually better, 
        # but we need high adherence to the "humanizing" instructions.
        # Use gemini-1.5-flash for speed and reliability
        self.model = genai.GenerativeModel('gemini-1.5-flash') 
    
    async def humanize_text(self, text: str, student_level: str = "University") -> str:
        """
        Rewrites text to mimic human writing patterns (high perplexity/burstiness).
        """
        try:
            # Tuned prompts for different levels
            style_guide = ""
            if student_level == "High School":
                style_guide = "Use simple sentence structures. Occasionally start sentences with 'And' or 'But'. Avoid overly complex academic jargon unless defined. Make 1-2 minor grammatical 'soft' errors (like splitting an infinitive) that a high schooler might make."
            elif student_level == "University":
                style_guide = "Use a mix of long and short sentences. Use active voice mostly but passive voice occasionally where appropriate for academic formal tone. Avoid repetitive sentence starts."
            elif student_level == "Masters" or student_level == "PhD":
                style_guide = "Use sophisticated vocabulary but avoid 'AI-sounding' words like 'delve', 'explore', 'landscape', 'tapestry'. Focus on deep critical analysis and nuanced argument structures."

            prompt = f"""
            TASK: Rewrite the following assignment content to bypass AI detection and sound like a HUMAN student.
            
            TARGET LEVEL: {student_level}
            
            STYLE INSTRUCTIONS:
            1. {style_guide}
            2. PERPLEXITY: Do not be predictable. Use varied vocabulary. 
            3. BURSTINESS: vary sentence length significantly. Have a very long complex sentence followed by a short punchy one.
            4. Remove standard AI transitions like "In conclusion,", "Furthermore,", "It is important to note that". Use more natural transitions.
            5. Keep the factual content and answers correct, but change the *voice*.
            
            CONTENT TO REWRITE:
            {text}
            
            OUTPUT:
            Return ONLY the rewritten text.
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9 # High temperature for more randomness/creativity
                )
            )
            
            return response.text
        
        except Exception as e:
            # If humanization fails, return original text to be safe
            print(f"Humanization failed: {e}")
            return text

humanizer_service = HumanizerService()
