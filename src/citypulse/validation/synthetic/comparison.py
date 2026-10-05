from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance


def compare_real_synthetic(real_values: list[float], synthetic_values: list[float]) -> dict[str, Any]:
    if not real_values:
        return {"status": "VALIDATION_NOT_AVAILABLE", "reason": "REAL_REFERENCE_DATA_NOT_AVAILABLE"}
    if not synthetic_values:
        return {"status": "VALIDATION_NOT_AVAILABLE", "reason": "SYNTHETIC_DATA_NOT_AVAILABLE"}
    real = np.asarray(real_values, dtype=float)
    synthetic = np.asarray(synthetic_values, dtype=float)
    if not np.isfinite(real).all() or not np.isfinite(synthetic).all():
        raise ValueError("NON_FINITE_COMPARISON_VALUES")
    ks = ks_2samp(real, synthetic)
    return {
        "status": "MEASURED",
        "reference_origin": "REAL_INPUT_SUPPLIED",
        "candidate_origin": "SYNTHETIC",
        "ks_statistic": float(ks.statistic),
        "ks_pvalue": float(ks.pvalue),
        "wasserstein_distance": float(wasserstein_distance(real, synthetic)),
        "sample_sizes": {"real": int(real.size), "synthetic": int(synthetic.size)},
        "interpretation": "Distribution comparison only; does not establish realism or synthetic training utility.",
    }
