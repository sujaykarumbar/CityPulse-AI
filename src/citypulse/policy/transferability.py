from __future__ import annotations

from typing import Any


def assess_transferability(*, source_city: str, target_city: str, overlap: dict[str, Any] | None = None) -> dict[str, Any]:
    if not overlap:
        return {"status": "UNKNOWN", "source_city": source_city, "target_city": target_city, "evidence": "INSUFFICIENT_DATA"}
    return {"status": "MEDIUM", "source_city": source_city, "target_city": target_city, "evidence": "PARTIALLY_SUPPORTED", "overlap": overlap}
