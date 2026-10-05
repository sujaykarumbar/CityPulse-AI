from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    app_name: str = "CityPulse API"
    environment: str = "local"
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    llm_provider: str | None = None
    llm_model: str | None = None
    llm_api_key: str | None = None
    llm_base_url: str | None = None
    llm_temperature: float = 0.0
    llm_max_tokens: int = 800

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CITYPULSE_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
