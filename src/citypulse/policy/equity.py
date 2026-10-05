from __future__ import annotations

from typing import Any


def equity_analysis(metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    metrics = metrics or {}
    if not metrics:
        return {"status": "NOT_AVAILABLE", "distribution": {}, "limitations": ["No equity data available."]}
    return {"status": "MEASURED", "distribution": metrics, "limitations": []}
