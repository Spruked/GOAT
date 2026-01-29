# backend/app/config.py
"""
Configuration management for SKG GOAT Edition
Fail-fast validation and environment handling
"""

import os
import secrets
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from pathlib import Path


class Settings(BaseSettings):
    # UCM Integration
    UCM_BASE_URL: str = "http://localhost:8000"
    """Application settings with validation"""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    WORKERS: int = 1
    RELOAD: bool = False
    LOG_LEVEL: str = "INFO"
    ENABLE_DOCS: bool = True

    # Database
    DB_TYPE: str = "sqlite"  # sqlite, postgresql
    DATABASE_URL: str = "sqlite:///./skg_goat.db"
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "skg_goat"

    # Cache
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None

    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "local"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_PRIVATE_KEY: Optional[str] = None
    JWT_PUBLIC_KEY: Optional[str] = None

    # Storage
    STORAGE_DIR: Path = Path("storage")
    VIDEOS_DIR: Path = STORAGE_DIR / "videos"

    # JWT Configuration
    JWT_SECRET_KEY: str = "your_jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Configuration
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "localhost"
    SERVER_HOST: str = "http://localhost"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: str = '["http://localhost:3000", "http://localhost:8080"]'

    # Video Processing
    VIDEO_OUTPUT_DIR: str = "./videos"
    AUDIO_CACHE_DIR: str = "./audio_cache"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra environment variables

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v, values):
        """Assemble database URL from components"""
        if v and v != "sqlite:///./skg_goat.db":
            return v

        db_type = values.get("DB_TYPE", "sqlite")
        if db_type == "postgresql":
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD")
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT")
            db = values.get("POSTGRES_DB")
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return v

    def validate_environment(self):
        """Fail-fast environment validation"""
        required_in_prod = ["SECRET_KEY"]

        if self.ENVIRONMENT == "production":
            missing = [key for key in required_in_prod if not getattr(self, key)]
            if missing:
                raise ValueError(f"Missing required production settings: {missing}")

        # Validate directories exist
        self.STORAGE_DIR.mkdir(exist_ok=True)
        self.VIDEOS_DIR.mkdir(exist_ok=True)

# Global settings instance
settings = Settings()