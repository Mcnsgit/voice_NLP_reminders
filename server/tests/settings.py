# tests/settings.py
from app.core.config import Settings


class TestSettings(Settings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    ENVIRONMENT: str = "test"
    DEBUG: bool = True
    TESTING: bool = True

    class Config:
        env_file = ".env.test"
