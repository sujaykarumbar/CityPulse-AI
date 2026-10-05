from __future__ import annotations

from typing import Any


def robustness_analysis(*, strategy_scores: dict[str, float]) -> dict[str, Any]:
    """Compute a bounded robustness summary across candidate strategies."""

    values = list(strategy_scores.values())
    if not values:
        return {"status": "MODEL_DERIVED", "robustness": 0.0, "strategy_scores": {}, "mean": 0.0}

    mean_score = sum(values) / len(values)
    return {
        "status": "MODEL_DERIVED",
        "robustness": round(mean_score, 6),
        "mean": round(mean_score, 6),
        "minimum": min(values),
        "strategy_scores": {key: float(value) for key, value in strategy_scores.items()},
    }


def regret_analysis(*, strategy_scores: dict[str, float], best_score: float) -> dict[str, Any]:
    """Measure regret relative to the best observed or modelled strategy score."""

    strategy_regret = {key: max(0.0, float(best_score) - float(value)) for key, value in strategy_scores.items()}
    total_regret = sum(strategy_regret.values())
    return {
        "status": "MODEL_DERIVED",
        "best_score": float(best_score),
        "regret_total": round(total_regret, 6),
        "strategy_regret": {key: round(value, 6) for key, value in strategy_regret.items()},
    }
