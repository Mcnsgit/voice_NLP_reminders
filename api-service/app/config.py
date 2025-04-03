import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Voice Task Manager API"
    api_prefix: str = "/api/v1"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    allowed_origins: list = ["*"]  # For development

settings = Settings()