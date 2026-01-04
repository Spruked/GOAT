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
    
    # Security - SECRET_KEY should be set via environment variable
    SECRET_KEY: str = os.getenv("SECRET_KEY", "goat-super-secret-key-change-in-production-INSECURE-DEFAULT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour (reduced from 30 days for better security)
    
    # Database
    DATABASE_URL: str = "sqlite:///./goat.db"
    
    # External services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def validate_environment(self):
        """Validate critical environment variables"""
        if self.SECRET_KEY == "goat-super-secret-key-change-in-production-INSECURE-DEFAULT":
            import warnings
            warnings.warn(
                "Using default SECRET_KEY! Set SECRET_KEY environment variable in production!",
                RuntimeWarning
            )


settings = Settings()
