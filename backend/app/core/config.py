import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Assignment Helper")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

settings = Settings()
