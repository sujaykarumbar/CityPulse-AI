from __future__ import annotations

import math
from typing import Any

from citypulse.validation.synthetic.energy_generator import generate_energy
from citypulse.validation.synthetic.mobility_generator import generate_mobility
from citypulse.validation.synthetic.quality import synthetic_quality_report
from citypulse.validation.synthetic.traffic_generator import generate_traffic


def _coerce_numeric(values: list[Any]) -> list[float]:
    return [float(value) for value in values]


def benchmark_run(
    observed: list[float] | list[Any],
    predicted: list[float] | list[Any],
    *,
    task: str = "urban-benchmark",
    domain: str = "urban",
    dataset_version: str | None = None,
    model_version: str | None = None,
    result_type: str = "FORECAST",
) -> dict[str, Any]:
    """Return measured metrics only when real ground truth is available."""
    experiment_id = f"bench-{task.lower().replace(' ', '-')}-{len(observed)}-{len(predicted)}"
    if not observed or not predicted:
        return {
            "experiment_id": experiment_id,
            "task": task,
            "domain": domain,
            "status": "NOT_RUN",
            "ground_truth_status": "GROUND_TRUTH_NOT_AVAILABLE",
            "benchmark_status": "NOT_RUN",
            "metrics": {},
            "dataset_version": dataset_version,
            "model_version": model_version,
            "result_type": result_type,
            "limitations": ["Ground truth is absent, so no benchmark metric is claimed."],
            "metadata": {"data_origin": "NOT_AVAILABLE"},
        }

    if len(observed) != len(predicted):
        raise ValueError("INVALID_INPUT_SHAPE")

    observed_values = _coerce_numeric(observed)
    predicted_values = _coerce_numeric(predicted)
    errors = [o - p for o, p in zip(observed_values, predicted_values)]
    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = math.sqrt(sum(e * e for e in errors) / len(errors))
    metrics = {"MAE": mae, "RMSE": rmse}

    denom = sum(abs(o) for o in observed_values)
    if denom > 0:
        metrics["WAPE"] = sum(abs(e) for e in errors) / denom
    else:
        metrics["WAPE"] = "NOT_MEASURED"

    observed_mean = sum(observed_values) / len(observed_values)
    rss = sum((o - p) ** 2 for o, p in zip(observed_values, predicted_values))
    tss = sum((o - observed_mean) ** 2 for o in observed_values)
    metrics["R2"] = (1 - rss / tss) if tss else "NOT_MEASURED"

    return {
        "experiment_id": experiment_id,
        "task": task,
        "domain": domain,
        "status": "MEASURED",
        "ground_truth_status": "AVAILABLE",
        "benchmark_status": "MEASURED",
        "metrics": metrics,
        "dataset_version": dataset_version,
        "model_version": model_version,
        "result_type": result_type,
        "limitations": ["Metrics describe only the aligned inputs supplied for this benchmark run."],
        "metadata": {"data_origin": "OBSERVED"},
    }


def build_synthetic_scenario(domain: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Create a synthetic evaluation case without using any real ground truth."""
    cfg = dict(config or {})
    generators = {
        "traffic": generate_traffic,
        "mobility": generate_mobility,
        "energy": generate_energy,
    }
    if domain not in generators:
        raise ValueError("UNSUPPORTED_EVALUATION_DOMAIN")

    sample_count = int(cfg.pop("sample_count", 100))
    seed = int(cfg.pop("seed", 0))
    frame = generators[domain]({**cfg, "sample_count": sample_count, "seed": seed})
    quality = synthetic_quality_report(frame)
    result = {
        "experiment_id": f"synthetic-{domain}-{seed}-{sample_count}",
        "task": f"{domain}-synthetic-benchmark",
        "domain": domain,
        "status": "SYNTHETIC_ONLY",
        "ground_truth_status": "GROUND_TRUTH_NOT_AVAILABLE",
        "benchmark_status": "SYNTHETIC_ONLY",
        "metrics": {},
        "rows": frame.to_dict(orient="records"),
        "quality": quality,
        "limitations": ["Synthetic scenario is intentionally not a real-world benchmark."],
        "metadata": {"data_origin": "SYNTHETIC", "seed": seed},
    }
    return result


def run_benchmark(
    observed: list[float] | list[Any],
    predicted: list[float] | list[Any],
    *,
    task: str = "urban-benchmark",
    domain: str = "urban",
    dataset_version: str | None = None,
    model_version: str | None = None,
    result_type: str = "FORECAST",
) -> dict[str, Any]:
    return benchmark_run(
        observed,
        predicted,
        task=task,
        domain=domain,
        dataset_version=dataset_version,
        model_version=model_version,
        result_type=result_type,
    )
