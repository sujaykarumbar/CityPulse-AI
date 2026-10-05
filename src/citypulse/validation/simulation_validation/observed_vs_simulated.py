from __future__ import annotations

from citypulse.validation.benchmarking.metrics import regression_metrics


def compare_observed_simulated(observed: list[float], simulated: list[float]) -> dict:
    metrics = regression_metrics(observed, simulated)
    if metrics.get("status") != "MEASURED":
        return {"status": "VALIDATION_NOT_AVAILABLE", "result_type": "SIMULATED", "metrics": metrics, "residuals": []}
    residuals = [float(actual - estimate) for actual, estimate in zip(observed, simulated, strict=True)]
    return {
        "status": "VALIDATED",
        "result_type": "SIMULATED",
        "metrics": metrics,
        "residuals": residuals,
        "limitations": ["Validation only applies to the supplied aligned observations and simulation outputs.", "Agreement does not establish causal validity."],
    }
