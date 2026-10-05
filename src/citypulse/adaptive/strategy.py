from __future__ import annotations

from typing import Any


class StrategyLifecycle:
    """A simple lifecycle manager for urban strategy states."""

    TRANSITIONS = {
        "DRAFT": {"validate": "VALIDATED", "review": "REVIEW_REQUIRED"},
        "VALIDATED": {"approve": "APPROVED", "review": "REVIEW_REQUIRED"},
        "APPROVED": {"activate": "ACTIVE", "review": "REVIEW_REQUIRED"},
        "ACTIVE": {"monitor": "MONITORING", "review": "REVIEW_REQUIRED", "deprecate": "DEPRECATED"},
        "MONITORING": {"review": "REVIEW_REQUIRED", "deprecate": "DEPRECATED"},
        "REVIEW_REQUIRED": {"reassess": "REASSESSMENT", "archive": "ARCHIVED"},
        "REASSESSMENT": {"update": "UPDATED", "archive": "ARCHIVED"},
        "UPDATED": {"activate": "ACTIVE", "review": "REVIEW_REQUIRED"},
        "DEPRECATED": {"archive": "ARCHIVED"},
    }

    def advance(self, current_status: str, action: str) -> str:
        next_state = self.TRANSITIONS.get(current_status, {}).get(action)
        return next_state or current_status


def compute_strategy_health(metrics: dict[str, float]) -> dict[str, Any]:
    """Summarize strategy health without collapsing to a single opaque score."""

    scores = {name: float(value) for name, value in metrics.items()}
    if not scores:
        return {"overall_status": "INSUFFICIENT_DATA", "dimensions": {}, "status": "INSUFFICIENT_DATA"}

    average = sum(scores.values()) / len(scores)
    if average < 0.6:
        overall_status = "DEGRADING"
    elif average < 0.75:
        overall_status = "REVIEW_REQUIRED"
    else:
        overall_status = "ON_TRACK"

    return {
        "overall_status": overall_status,
        "status": overall_status,
        "dimensions": {key: {"value": value, "status": "MODEL_DERIVED"} for key, value in scores.items()},
        "average_score": average,
    }


def generate_alternatives(strategy_id: str, options: list[str]) -> list[dict[str, str]]:
    """Create candidate policy variations with traceability to the current strategy."""

    alternatives: list[dict[str, str]] = []
    for option in options:
        alternatives.append({
            "strategy_id": strategy_id,
            "alternative_id": f"{strategy_id}-{option}",
            "action": option,
            "status": "SCENARIO_ESTIMATE",
            "parent_strategy": strategy_id,
        })
    return alternatives
