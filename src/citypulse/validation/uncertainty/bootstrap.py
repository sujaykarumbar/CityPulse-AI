from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np


def bootstrap_interval(
    values: list[float],
    statistic: Callable[[np.ndarray], float] = np.mean,
    samples: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict[str, Any]:
    if not values:
        return {"status": "UNCERTAINTY_NOT_ESTIMATED", "reason": "NO_VALUES"}
    if not 100 <= samples <= 20_000 or not 0 < confidence < 1:
        raise ValueError("INVALID_BOOTSTRAP_CONFIGURATION")
    array = np.asarray(values, dtype=float)
    if not np.isfinite(array).all():
        raise ValueError("NON_FINITE_BOOTSTRAP_VALUES")
    rng = np.random.default_rng(seed)
    estimates = np.fromiter((statistic(rng.choice(array, size=array.size, replace=True)) for _ in range(samples)), dtype=float)
    tail = (1 - confidence) / 2
    return {"status": "MEASURED", "method": "NONPARAMETRIC_BOOTSTRAP_PERCENTILE", "estimate": float(statistic(array)), "lower": float(np.quantile(estimates, tail)), "upper": float(np.quantile(estimates, 1 - tail)), "confidence_level": confidence, "samples": samples, "seed": seed, "interpretation": "Interval over the supplied sample statistic; not a guarantee about future city states."}
