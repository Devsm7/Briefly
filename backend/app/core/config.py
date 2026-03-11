"""Core application settings loaded from environment variables."""

# TODO: Import pydantic_settings.BaseSettings
# TODO: Define Settings class with all env fields:
#       - APP_NAME, DEBUG
#       - DATABASE_URL
#       - SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
#       - OLLAMA_BASE_URL, OLLAMA_MODEL, OPENAI_API_KEY
#       - NEWS_API_KEY, SCRAPE_INTERVAL_HOURS
# TODO: Instantiate settings = Settings() at module level


class Settings:
    """Application configuration loaded from .env via pydantic-settings."""

    # TODO: implement all fields
    pass


settings = Settings()
