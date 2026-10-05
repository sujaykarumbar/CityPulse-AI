from __future__ import annotations

from config.settings import load_settings


def get_environment_settings(environment: str | None = None):
    return load_settings(environment)
