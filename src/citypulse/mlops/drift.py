from __future__ import annotations

import numpy as np

from citypulse.mlops.schemas import DriftResult


def population_stability_index(reference: list[float], current: list[float], bins: int = 10) -> float:
    if not reference or not current:
        raise ValueError("DRIFT_NOT_MEASURABLE")
    edges = np.histogram_bin_edges(np.asarray(reference, dtype=float), bins=bins)
    if len(edges) < 2:
        return 0.0
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    ref = np.clip(ref_counts / len(reference), 1e-6, None)
    cur = np.clip(cur_counts / len(current), 1e-6, None)
    return float(np.sum((cur - ref) * np.log(cur / ref)))


def calculate_drift(feature: str, reference: list[float], current: list[float], threshold: float | None = None) -> DriftResult:
    if not reference or not current:
        return DriftResult(feature=feature, method="PSI", reference_statistic={}, current_statistic={}, distance=0.0, threshold=threshold, status="NOT_MEASURABLE", sample_size_reference=len(reference), sample_size_current=len(current))
    distance = population_stability_index(reference, current)
    status = "DRIFT" if threshold is not None and distance > threshold else "NO_DRIFT" if threshold is not None else "NOT_MEASURABLE"
    return DriftResult(feature=feature, method="PSI", reference_statistic={"mean": float(np.mean(reference)), "std": float(np.std(reference))}, current_statistic={"mean": float(np.mean(current)), "std": float(np.std(current))}, distance=distance, threshold=threshold, status=status, sample_size_reference=len(reference), sample_size_current=len(current))
