"""
Configuration management for MzeeChakula backend.
Loads environment variables and provides app-wide settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "MzeeChakula API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    
    # Redis (optional)
    REDIS_URL: str | None = None
    
    # AI Services
    GROQ_API_KEY: str
    SUNBIRD_API_KEY: str
    HUGGINGFACE_TOKEN: str
    
    # Vector DB
    PINECONE_API_KEY: str | None = None
    PINECONE_ENVIRONMENT: str | None = None
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173"
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "/app/uploads"
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".doc", ".docx", ".txt"]
    
    # Model
    MODEL_DIR: str = "/app/models"
    HUGGINGFACE_REPO: str = "Shakiran/MzeeChakula_Model"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
