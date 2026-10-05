from __future__ import annotations

from enum import Enum
from typing import Any


class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    SENSITIVE = "sensitive"


def classify_dataset(metadata: dict[str, Any] | None) -> DataClassification:
    classification = (metadata or {}).get("classification", "internal")
    normalized = str(classification).lower()
    try:
        return DataClassification(normalized)
    except ValueError:
        return DataClassification.INTERNAL
