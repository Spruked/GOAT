import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    WORKERS: int = 1
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"
    ENABLE_DOCS: bool = True
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "goat-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./goat.db"
    
    # External services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def validate_environment(self):
        """Validate critical environment variables"""
        pass


settings = Settings()
