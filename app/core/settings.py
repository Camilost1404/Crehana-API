import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings.
    """

    # Application settings
    app_name: str = "Crehana API"
    app_version: str = "1.0.0"

    # Database settings
    database_url: str = "sqlite:///./test.db"

    # JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


try:
    settings = Settings()
except Exception as e:
    logger.error("Failed to load settings: %s", e)
    raise
