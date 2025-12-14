import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """تنظیمات برنامه"""
    
    # App
    APP_NAME: str = "BIM Backend API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./bim.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Admin
    ADMIN_EMAIL: str = "admin@bim.com"
    ADMIN_PASSWORD: str = "admin123"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
