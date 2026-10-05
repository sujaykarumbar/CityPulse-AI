from __future__ import annotations

from typing import Any, Dict, List


def optimize_facility_locations(
    city_id: str,
    candidates: List[Dict[str, Any]],
    objective_weights: Dict[str, float] | None = None,
    budget: float | None = None,
) -> Dict[str, Any]:
    """Return Pareto-style candidate results instead of one universal optimum."""
    objective_weights = objective_weights or {"coverage": 0.5, "equity": 0.3, "resilience": 0.2}
    scenarios: List[Dict[str, Any]] = []
    for candidate in candidates:
        coverage = float(candidate.get("coverage_gain", 0.0))
        equity = float(candidate.get("equity_gain", 0.0))
        resilience = float(candidate.get("resilience_gain", 0.0))
        score = (coverage * objective_weights.get("coverage", 0.0)) + (
            equity * objective_weights.get("equity", 0.0)
        ) + (resilience * objective_weights.get("resilience", 0.0))
        scenarios.append({
            "candidate_id": candidate.get("candidate_id", "unknown"),
            "location": candidate.get("location", "unknown"),
            "estimated_score": round(score, 3),
            "coverage_gain": coverage,
            "equity_gain": equity,
            "resilience_gain": resilience,
            "cost": candidate.get("cost"),
            "budget_constraint": budget,
            "status": "MODEL_DERIVED",
        })

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "objective_weights": objective_weights,
        "pareto_candidates": scenarios,
        "method": "multi_objective_candidate_analysis",
        "limitations": [
            "The returned candidate portfolio is a model-based trade-off set, not a guaranteed optimal facility placement.",
        ],
    }
