"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "Banking API"
    version: str = "1.0.0"
    description: str = "A secure REST API for banking operations"
    
    # Security - IMPORTANT: Change these values in production!
    # Generate a secure secret key with: openssl rand -hex 32
    secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./bank.db"
    
    class Config:
        env_file = ".env"


settings = Settings()
