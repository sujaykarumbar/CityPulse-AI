from __future__ import annotations

from typing import Any


def aggregate_health(components: dict[str, str]) -> dict[str, Any]:
    order = {"HEALTHY": 0, "UNKNOWN": 1, "DEGRADED": 2, "UNAVAILABLE": 3}
    if not components:
        return {"status": "UNKNOWN", "components": {}, "summary": "No health inputs were provided."}
    worst_status = max(components.values(), key=lambda value: order.get(value, -1))
    return {"status": worst_status, "components": components, "summary": "Health is reported based on the worst observed component state."}
