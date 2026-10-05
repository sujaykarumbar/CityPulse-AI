from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from citypulse.governance.classification import DataClassification


@dataclass
class RetentionPolicy:
    name: str
    classification: DataClassification
    days: int = 30
    action: str = "retain"


def evaluate_retention(policy: RetentionPolicy, age_days: int) -> dict[str, Any]:
    if age_days > policy.days:
        return {"status": "delete", "action": policy.action, "classification": policy.classification.value, "age_days": age_days}
    return {"status": "retain", "action": policy.action, "classification": policy.classification.value, "age_days": age_days}
