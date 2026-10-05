from __future__ import annotations

from typing import Any


def define_outcome(outcome: str, unit: str = "city_hour", metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "unit": unit,
        "metadata": metadata or {},
        "status": "OUTCOME_DEFINED",
    }
