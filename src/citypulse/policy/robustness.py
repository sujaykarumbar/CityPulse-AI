from __future__ import annotations

from typing import Any


def robustness_report(*, policy_id: str, scenarios: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if not scenarios:
        return {"status": "NOT_RUN", "policy_id": policy_id, "reason": "No stress scenarios were supplied."}
    return {"status": "MEASURED", "policy_id": policy_id, "scenarios": scenarios}
