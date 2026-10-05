from __future__ import annotations

from typing import Any


class MultiCityPolicySimulation:
    """A simple regional coordination simulation that preserves distributional trade-offs."""

    def __init__(self, *, city_policies: dict[str, dict[str, Any]] | None = None) -> None:
        self.city_policies = city_policies or {}

    def simulate(self) -> dict[str, Any]:
        city_results: list[dict[str, Any]] = []
        for city_id, policy in self.city_policies.items():
            gain = float(policy.get("expected_gain", 0.0))
            city_results.append(
                {
                    "city_id": city_id,
                    "policy": policy.get("policy", "unknown"),
                    "expected_gain": gain,
                    "tradeoff_class": "LOCAL_GAIN" if gain > 0 else "DISTRIBUTIONAL_TRADEOFF",
                }
            )

        regional_gain = sum(item["expected_gain"] for item in city_results)
        tradeoff = "SYSTEM_WIDE_IMPROVEMENT" if regional_gain > 0 else "INSUFFICIENT_EVIDENCE"
        return {
            "status": "MODEL_DERIVED",
            "regional_gain": round(regional_gain, 4),
            "tradeoff_class": tradeoff,
            "cities": city_results,
            "limitations": [
                "Policy coordination results are scenario estimates and require validation against real evidence before acting on them.",
            ],
        }
