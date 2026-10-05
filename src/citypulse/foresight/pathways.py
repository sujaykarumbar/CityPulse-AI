from __future__ import annotations

from typing import Any

from .schemas import TriggerResult


def evaluate_trigger(
    *,
    metric_name: str,
    current_value: float,
    threshold: float,
    direction: str = "above",
) -> dict[str, Any]:
    """Evaluate a single metric against a threshold and return a decision signal."""

    direction = direction.lower()
    triggered = current_value > threshold if direction == "above" else current_value < threshold
    if metric_name == "transit_ridership":
        signal = "TRANSIT_EXPANSION_REVIEW" if triggered else "MAINTAIN_CURRENT_STRATEGY"
    elif metric_name == "traffic_volume":
        signal = "TRAFFIC_RESPONSE_REVIEW" if triggered else "STABILITY_OK"
    else:
        signal = "CHECK_METRIC" if triggered else "MONITOR"

    return TriggerResult(
        metric_name=metric_name,
        current_value=current_value,
        threshold=threshold,
        direction=direction,
        triggered=triggered,
        signal=signal,
        status="MODEL_DERIVED",
    ).model_dump()


class AdaptivePathwayEngine:
    """Creates adaptive, replayable policy pathways for long-horizon planning."""

    def build_pathway(
        self,
        *,
        initial_strategy: str,
        monitors: list[str],
        thresholds: dict[str, float],
        alternative_strategy: str,
    ) -> dict[str, Any]:
        monitoring = [
            {
                "metric": metric,
                "threshold": thresholds.get(metric, 0.0),
                "check": evaluate_trigger(
                    metric_name=metric,
                    current_value=thresholds.get(metric, 0.0),
                    threshold=thresholds.get(metric, 0.0),
                    direction="above",
                ),
            }
            for metric in monitors
        ]

        return {
            "initial_strategy": initial_strategy,
            "monitoring": monitoring,
            "thresholds": thresholds,
            "alternative_strategy": alternative_strategy,
            "next_action": "MONITOR",
            "provenance": {"status": "MODEL_DERIVED", "source": "synthetic_pathway"},
        }
