from __future__ import annotations

from typing import Any


def normalize_treatment(treatment: str, treatment_type: str = "binary", metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "treatment": treatment,
        "treatment_type": treatment_type,
        "metadata": metadata or {},
        "status": "TREATMENT_DEFINED",
    }
