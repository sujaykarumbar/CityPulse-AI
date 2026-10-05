from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


class EnvironmentSettings:
    def __init__(self, environment: str | None = None) -> None:
        self.environment = environment or os.getenv("CITYPULSE_ENVIRONMENT", "development")
        root = Path(__file__).resolve().parent
        defaults = _load_yaml(root / "defaults.yaml")
        env_file = root / "environments" / f"{self.environment}.yaml"
        env_config = _load_yaml(env_file)
        merged = {**defaults, **env_config}
        for key, value in merged.items():
            setattr(self, key, value)

    def validate(self) -> None:
        required = [
            "database_url",
            "redis_url",
            "kafka_brokers",
            "model_registry_url",
            "object_storage_url",
            "api_base_url",
            "frontend_base_url",
            "jwt_issuer",
            "jwt_audience",
        ]
        if self.environment == "production":
            missing = [name for name in required if not getattr(self, name, None)]
            if missing:
                raise RuntimeError(f"Missing required production configuration: {', '.join(missing)}")


def load_settings(environment: str | None = None) -> EnvironmentSettings:
    settings = EnvironmentSettings(environment)
    settings.validate()
    return settings
