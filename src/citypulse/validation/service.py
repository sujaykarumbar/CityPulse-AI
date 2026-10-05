from __future__ import annotations

import math
from typing import Any

from citypulse.validation.benchmarking.metrics import regression_metrics
from citypulse.validation.robustness.missing_data import apply_missingness
from citypulse.validation.registry.experiment_registry import ValidationRegistry
from citypulse.validation.schemas import MetricResult, ValidationResult
from citypulse.validation.simulation_validation.observed_vs_simulated import compare_observed_simulated
from citypulse.validation.synthetic.energy_generator import generate_energy
from citypulse.validation.synthetic.mobility_generator import generate_mobility
from citypulse.validation.synthetic.quality import synthetic_quality_report
from citypulse.validation.synthetic.comparison import compare_real_synthetic
from citypulse.validation.synthetic.traffic_generator import generate_traffic
from citypulse.validation.synthetic.weather_generator import generate_weather


class ValidationService:
    def __init__(self) -> None:
        self.registry = ValidationRegistry()

    def status(self) -> dict[str, Any]:
        return {
            "status": "VALIDATION_NOT_AVAILABLE" if not self.registry.list() else "MEASURED_RUNS_AVAILABLE",
            "real_datasets": "NOT_AVAILABLE",
            "trained_models": "NOT_AVAILABLE",
            "validation_runs": len(self.registry.list()),
            "experiment_results": "NOT_MEASURED",
            "limitations": ["No verified real CITYPULSE dataset/model artifacts are present in this checkout."],
        }

    def compare(self, task: str, observed: list[float], predicted: list[float], dataset_version: str | None, model_version: str | None, result_type: str = "FORECAST") -> ValidationResult:
        metrics = regression_metrics(observed, predicted)
        metric_results = []
        for key, value in metrics.items():
            if key == "status":
                continue
            measured = isinstance(value, float) and math.isfinite(value)
            metric_results.append(
                MetricResult(
                    name=key,
                    value=value if measured else None,
                    status="MEASURED" if measured else "NOT_MEASURED",
                )
            )
        result = ValidationResult(
            task=task,
            dataset_version=dataset_version,
            model_version=model_version,
            metric_results=metric_results,
            status="VALIDATED" if metrics.get("status") == "MEASURED" else "VALIDATION_NOT_AVAILABLE",
            result_type=result_type,
            limitations=["Metrics describe only the explicitly supplied aligned arrays."],
        )
        return self.registry.register(result)

    def synthetic(self, domain: str, config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        generators = {"traffic": generate_traffic, "mobility": generate_mobility, "energy": generate_energy, "weather": generate_weather}
        if domain not in generators:
            raise ValueError("UNSUPPORTED_SYNTHETIC_DOMAIN")
        frame = generators[domain](config)
        return frame.to_dict(orient="records"), synthetic_quality_report(frame)

    def simulation_compare(self, observed: list[float], simulated: list[float]) -> dict[str, Any]:
        return compare_observed_simulated(observed, simulated)

    def compare_synthetic(self, real_values: list[float], synthetic_values: list[float]) -> dict[str, Any]:
        return compare_real_synthetic(real_values, synthetic_values)

    def missingness_experiment(self, values: list[float], rate: float, seed: int, mode: str) -> dict[str, Any]:
        import pandas as pd

        frame = pd.DataFrame({"value": values})
        changed = apply_missingness(frame, rate=rate, seed=seed, mode=mode)
        return {
            "status": "PERTURBATION_MEASURED",
            "data_origin": "SYNTHETIC_ROBUSTNESS_TEST",
            "mode": mode,
            "requested_rate": rate,
            "measured_missing_rate": float(changed["value"].isna().mean()),
            "seed": seed,
            "model_degradation": "NOT_MEASURED",
        }
