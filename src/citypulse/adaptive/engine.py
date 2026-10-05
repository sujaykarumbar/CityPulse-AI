from __future__ import annotations

from typing import Any

from .assumptions import check_assumption
from .change_detection import detect_change
from .strategy import StrategyLifecycle, compute_strategy_health, generate_alternatives


class AdaptiveUrbanIntelligenceEngine:
    """Orchestrates monitoring, drift detection, and strategy reassessment."""

    def __init__(self) -> None:
        self.lifecycle = StrategyLifecycle()

    def monitor_strategy(
        self,
        *,
        city_id: str,
        strategy_id: str,
        observed_metrics: dict[str, float],
        expected_metrics: dict[str, float],
        assumptions: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        health = compute_strategy_health(observed_metrics)
        reasons: list[str] = []

        for metric_name, expected_value in expected_metrics.items():
            observed_value = observed_metrics.get(metric_name, expected_value)
            if observed_value < expected_value:
                reasons.append(f"{metric_name} below expected threshold")

        if assumptions:
            for assumption in assumptions:
                result = check_assumption(
                    assumption_id=str(assumption.get("assumption_id", "unknown")),
                    description=str(assumption.get("description", "check")),
                    variable=str(assumption.get("variable", "unknown")),
                    expected_range=tuple(assumption.get("expected_range", (0.0, 0.0))),
                    observed_value=float(assumption.get("observed_value", 0.0)),
                )
                if result["triggered"]:
                    reasons.append(f"assumption drift: {result['variable']}")

        status = "ON_TRACK" if not reasons and health["overall_status"] == "ON_TRACK" else "REVIEW_REQUIRED"
        return {
            "city_id": city_id,
            "strategy_id": strategy_id,
            "status": status,
            "health": health,
            "observed_metrics": observed_metrics,
            "expected_metrics": expected_metrics,
            "reasons": reasons,
            "alternatives": generate_alternatives(strategy_id, ["continue", "modify", "scale_up"]),
            "monitoring": {"source": "adaptive_engine", "status": "MODEL_DERIVED"},
        }

    def detect_change(self, *, metric_name: str, previous_value: float, current_value: float, threshold: float) -> dict[str, Any]:
        return detect_change(
            metric_name=metric_name,
            previous_value=previous_value,
            current_value=current_value,
            threshold=threshold,
        )
