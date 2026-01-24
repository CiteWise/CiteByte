"""
Configuration module for Literature Survey System.
All settings loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    semantic_scholar_api_key: str = "mock_key"
    ieee_api_key: str = "mock_key"
    crossref_api_key: str = "mock_key"
    
    # Optional LLM API keys
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./literature_survey.db"
    
    # Application behavior
    use_mock_apis: bool = True
    use_mock_llm: bool = True
    max_papers_retrieve: int = 50
    top_papers_full_text: int = 5
    
    # Text chunking
    chunk_max_tokens: int = 500
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
