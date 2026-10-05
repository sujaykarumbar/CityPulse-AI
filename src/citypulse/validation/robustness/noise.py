from __future__ import annotations

import numpy as np
import pandas as pd


def add_gaussian_noise(frame: pd.DataFrame, columns: list[str], std: float, seed: int = 42) -> pd.DataFrame:
    if std < 0 or not np.isfinite(std):
        raise ValueError("INVALID_NOISE_SCALE")
    result = frame.copy(deep=True)
    rng = np.random.default_rng(seed)
    for column in columns:
        if column not in result:
            raise ValueError(f"FEATURE_NOT_FOUND:{column}")
        values = pd.to_numeric(result[column], errors="raise").to_numpy(dtype=float)
        result[column] = values + rng.normal(0.0, std, size=len(values))
    return result
