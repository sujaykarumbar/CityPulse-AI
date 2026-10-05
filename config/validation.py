from __future__ import annotations

from config.settings import load_settings


def validate_environment_config(environment: str | None = None) -> dict[str, str | bool]:
    settings = load_settings(environment)
    return {
        "environment": settings.environment,
        "database_configured": bool(getattr(settings, "database_url", None)),
        "redis_configured": bool(getattr(settings, "redis_url", None)),
        "kafka_configured": bool(getattr(settings, "kafka_brokers", None)),
        "production_validation": settings.environment == "production",
    }
