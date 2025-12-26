"""
Configuration management for the conference registration backend.
Uses Pydantic Settings to load and validate environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All sensitive credentials should be stored in .env file.
    """
    
    # Google Sheets Configuration
    google_sheets_credentials_path: str
    google_sheet_id: str
    
    # mNotify SMS Configuration (Ghana-based SMS service)
    mnotify_api_key: str
    
    # Application Configuration
    secret_key: str
    conference_name: str = "IYC Conference 2025"
    
    # URLs and Links
    whatsapp_group_link: str
    facebook_url: str
    youtube_url: str
    frontend_url: str = "http://localhost:8000"
    
    # Frontend Configuration
    frontend_path: str = "../frontend"
    
    # CORS Configuration
    allowed_origins: list[str] = [
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://localhost:3000",  # Common dev server port
        "http://127.0.0.1:3000"
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
