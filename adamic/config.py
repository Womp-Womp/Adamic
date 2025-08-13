import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application configuration loaded from environment variables."""
    api_key: str | None = os.getenv("GEMINI_API_KEY")
    model_name: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")


settings = Settings()
