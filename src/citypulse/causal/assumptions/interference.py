from __future__ import annotations


def check_interference(estimated_spillover: float | None = None) -> dict[str, str | float | list[str]]:
    if estimated_spillover is None:
        return {"status": "NOT_CHECKED", "assumption": "interference"}
    if abs(estimated_spillover) > 0.1:
        return {"status": "PARTIALLY_SUPPORTED", "assumption": "interference", "spillover": estimated_spillover}
    return {"status": "SUPPORTED", "assumption": "interference", "spillover": estimated_spillover}
