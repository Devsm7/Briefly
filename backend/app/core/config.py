"""Core application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from .env via pydantic-settings."""

    APP_NAME: str = "Briefly"
    DEBUG: bool = False

    DATABASE_URL: str = ""

    SECRET_KEY: str = "change-me-to-a-long-random-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral"
    OPENAI_API_KEY: str = ""

    NEWS_API_KEY: str = ""
    SCRAPE_INTERVAL_HOURS: int = 6

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
