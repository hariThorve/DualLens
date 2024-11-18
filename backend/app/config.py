from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    MAX_SEARCH_RESULTS: int = 10
    REQUEST_TIMEOUT: int = 30
    
    # LLM API Keys
    GEMINI_API_KEY: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()