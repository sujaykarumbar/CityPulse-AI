from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np


MAX_MONTE_CARLO_SAMPLES = 5_000
MAX_OUTPUT_DIMENSIONS = 256


def run_monte_carlo(
    simulator: Callable[[dict[str, float]], float | Sequence[float]],
    parameter_distributions: dict[str, dict[str, float | str]],
    sample_count: int = 1_000,
    seed: int = 42,
) -> dict[str, Any]:
    if not parameter_distributions or not 1 <= sample_count <= MAX_MONTE_CARLO_SAMPLES:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED_OR_INVALID_CONFIGURATION")

    normalized_distributions: dict[str, dict[str, float | str]] = {}
    for name, distribution in parameter_distributions.items():
        kind = distribution.get("distribution")
        if kind == "uniform":
            low = float(distribution.get("low", float("nan")))
            high = float(distribution.get("high", float("nan")))
            if not np.isfinite([low, high]).all() or low >= high:
                raise ValueError("INVALID_PARAMETER_DISTRIBUTION")
            normalized_distributions[name] = {"distribution": "uniform", "low": low, "high": high}
        elif kind == "normal":
            mean = float(distribution.get("mean", float("nan")))
            standard_deviation = float(distribution.get("std", float("nan")))
            if not np.isfinite([mean, standard_deviation]).all() or standard_deviation < 0:
                raise ValueError("INVALID_PARAMETER_DISTRIBUTION")
            normalized_distributions[name] = {
                "distribution": "normal",
                "mean": mean,
                "std": standard_deviation,
            }
        else:
            raise ValueError("UNSUPPORTED_PARAMETER_DISTRIBUTION")

    random = np.random.default_rng(seed)
    output_samples: list[list[float]] = []
    for _ in range(sample_count):
        parameters: dict[str, float] = {}
        for name, distribution in normalized_distributions.items():
            if distribution["distribution"] == "uniform":
                parameters[name] = float(random.uniform(float(distribution["low"]), float(distribution["high"])))
            else:
                parameters[name] = float(random.normal(float(distribution["mean"]), float(distribution["std"])))

        output = np.asarray(simulator(parameters), dtype=float).reshape(-1)
        if output.size == 0 or output.size > MAX_OUTPUT_DIMENSIONS or not np.isfinite(output).all():
            raise ValueError("INVALID_SIMULATION_OUTPUT")
        if output_samples and output.size != len(output_samples[0]):
            raise ValueError("INCONSISTENT_SIMULATION_OUTPUT_SHAPE")
        output_samples.append(output.tolist())

    samples = np.asarray(output_samples, dtype=float)
    summaries = [
        {
            "dimension": index,
            "mean": float(np.mean(samples[:, index])),
            "standard_deviation": float(np.std(samples[:, index], ddof=0)),
            "lower_quantile": float(np.quantile(samples[:, index], 0.025)),
            "upper_quantile": float(np.quantile(samples[:, index], 0.975)),
            "interval_type": "SIMULATION_QUANTILES_NOT_CONFIDENCE_INTERVALS",
        }
        for index in range(samples.shape[1])
    ]
    return {
        "status": "SIMULATED",
        "result_type": "SIMULATED",
        "random_seed": seed,
        "sample_count": sample_count,
        "parameter_distributions": normalized_distributions,
        "output_summaries": summaries,
        "output_samples": samples.T.tolist(),
        "limitations": ["Monte Carlo outputs are simulated, not observed city outcomes."],
    }