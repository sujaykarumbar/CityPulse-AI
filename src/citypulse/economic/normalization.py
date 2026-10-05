from __future__ import annotations

from typing import Any


def normalize_economic_value(value: float, *, unit: str, inflation_basis: str | None = None) -> dict[str, Any]:
    output = {
        "value": float(value),
        "unit": unit,
        "status": "MODEL_DERIVED",
    }
    if inflation_basis:
        output["inflation_basis"] = inflation_basis
    return output


def normalize_geography(geography: str) -> str:
    return geography.strip().lower()
