from __future__ import annotations

from typing import Any, Dict


def run_service_scenario(
    city_id: str,
    service_type: str,
    scenario: str,
    assumptions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Create a reproducible service scenario summary with explicit assumptions."""
    assumptions = assumptions or {}
    return {
        "city_id": city_id,
        "service_type": service_type,
        "scenario": scenario,
        "status": "MODEL_DERIVED",
        "assumptions": assumptions,
        "scenario_outcome": {
            "coverage_change": 0.0,
            "accessibility_change": 0.0,
            "capacity_gap_change": 0.0,
        },
        "method": "SIMULATED_SCENARIO",
        "limitations": [
            "Scenario outputs are simulation estimates and must be distinguished from observed events or causal effects.",
        ],
    }
