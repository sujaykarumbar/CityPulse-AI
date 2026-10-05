from __future__ import annotations

from typing import Any, Dict, List


def estimate_service_demand(
    city_id: str,
    service_type: str,
    population: float | None = None,
    density: float | None = None,
    historical_utilization: float | None = None,
    proxy_label: str = "PROXY",
) -> Dict[str, Any]:
    """Estimate demand using direct observations or clearly labeled proxies."""
    metric = population if population is not None else density if density is not None else historical_utilization
    if metric is None:
        return {
            "city_id": city_id,
            "service_type": service_type,
            "status": "MODEL_DERIVED",
            "demand_estimate": None,
            "proxy_label": "UNKNOWN",
            "method": "no_valid_direct_or_proxy_signal",
            "limitations": ["Demand cannot be estimated without a valid observation or proxy variable."],
        }

    demand = float(metric)
    return {
        "city_id": city_id,
        "service_type": service_type,
        "status": "MODEL_DERIVED",
        "demand_estimate": round(demand, 3),
        "proxy_label": proxy_label,
        "method": "MODEL_ESTIMATE" if proxy_label != "DIRECT_OBSERVATION" else "DIRECT_OBSERVATION",
        "limitations": [
            "This is a modeled demand estimate and should not be interpreted as observed service demand without data provenance.",
        ],
    }


def forecast_service_demand(
    city_id: str,
    service_type: str,
    history: List[float],
    horizon: int = 1,
) -> Dict[str, Any]:
    """Provide a simple historical-average forecast when sufficient history exists."""
    if not history:
        return {
            "city_id": city_id,
            "service_type": service_type,
            "status": "MODEL_DERIVED",
            "forecast": None,
            "method": "NOT_RUN",
            "limitations": ["No demand history is available for a forecast."],
        }

    average = sum(history) / len(history)
    return {
        "city_id": city_id,
        "service_type": service_type,
        "status": "MODEL_DERIVED",
        "forecast": round(average, 3),
        "horizon_periods": horizon,
        "method": "HISTORICAL_AVERAGE",
        "limitations": [
            "This is a simple time-series estimate and not a validated causal demand forecast.",
        ],
    }
