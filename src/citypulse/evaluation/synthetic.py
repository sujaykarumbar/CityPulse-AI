from __future__ import annotations

from typing import Any

from citypulse.evaluation.benchmark import build_synthetic_scenario


def generate_synthetic_scenario(domain: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_synthetic_scenario(domain, config)


def create_synthetic_scenario(domain: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_synthetic_scenario(domain, config)
