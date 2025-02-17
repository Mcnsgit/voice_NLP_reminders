import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # API Config
    PROJECT_NAME: str = "Task Manager API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    ALGORITHM: str = "HS256"

    # Environment settings
    DEBUG: bool = True
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    WORKERS_COUNT: int = int(os.getenv("WORKERS_COUNT", "1"))

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    DB_ECHO: bool = DEBUG

    # Postgres settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "taskmanager")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "taskmanager")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "taskmanager_db")

    # Development Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "taskmanager")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "taskmanager")
    DB_NAME: str = os.getenv("DB_NAME", "taskmanager_db")

    # Production Database
    NEON_DB_URL: Optional[str] = os.getenv("NEON_DB_URL")

    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Rate limiting
    ENABLE_RATE_LIMIT: bool = True
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",  # Allow extra fields from env files
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()


settings = get_settings()
