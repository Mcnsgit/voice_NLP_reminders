# app/core/config.py
import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

load_dotenv()


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://taskmanager:taskmanager@localhost:5432/taskmanager_db",
    )
    NEON_DB_URL: Optional[str] = os.getenv("DATABASE_URL")

    # Database Pool Settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_ECHO: bool = os.getenv("DEBUG", "False") == "True"

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")

    @property
    def get_database_url(self) -> str:
        """Get the appropriate database URL based on environment"""
        if self.ENVIRONMENT == "test":
            return "sqlite+aiosqlite:///./test.db"
        elif self.ENVIRONMENT == "development":
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        else:
            if not self.NEON_DB_URL:
                raise ValueError("NEON_DB_URL must be set in production")

            # Modify this line to ensure sslmode is not included
            url = self.NEON_DB_URL.replace(
                "postgresql://", "postgresql+asyncpg://"
            ).split("?")[0]
            return url  # Ensure no sslmode is appended
        # Other settings

    PROJECT_NAME: str = "Task Manager API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    ALGORITHM: str = "HS256"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    WORKERS_COUNT: int = int(os.getenv("WORKERS_COUNT", "1"))

    # Rate limiting
    ENABLE_RATE_LIMIT: bool = os.getenv("ENABLE_RATE_LIMIT", "False") == "True"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()


settings = get_settings()
