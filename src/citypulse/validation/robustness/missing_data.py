from __future__ import annotations

import numpy as np
import pandas as pd


def apply_missingness(frame: pd.DataFrame, rate: float, seed: int = 42, mode: str = "MCAR") -> pd.DataFrame:
    if not 0 <= rate < 1:
        raise ValueError("INVALID_MISSINGNESS_RATE")
    if mode not in {"MCAR", "BLOCK"}:
        raise ValueError("UNSUPPORTED_MISSINGNESS_MECHANISM")
    result = frame.copy(deep=True)
    n = len(result)
    count = int(round(n * rate))
    if not count or not n:
        return result
    rng = np.random.default_rng(seed)
    if mode == "MCAR":
        indices = rng.choice(n, size=count, replace=False)
    else:
        start = int(rng.integers(0, max(1, n - count + 1)))
        indices = np.arange(start, start + count)
    if result.shape[1] == 0:
        return result
    result.iloc[indices, :] = np.nan
    return result
