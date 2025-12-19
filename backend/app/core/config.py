import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Assignment Helper")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # Still keep for fallback or if needed
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # Email Settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "test@example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    
    # WhatsApp Settings
    WHATSAPP_API_TOKEN: str = os.getenv("WHATSAPP_API_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

    class Config:
        case_sensitive = True

    def reload(self):
        """Reload settings from .env file."""
        load_dotenv(override=True)
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

settings = Settings()
