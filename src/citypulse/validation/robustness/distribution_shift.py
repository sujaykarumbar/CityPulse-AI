from __future__ import annotations

import numpy as np


def shift_numeric_distribution(values: list[float], additive_shift: float = 0.0, scale: float = 1.0) -> tuple[list[float], dict[str, float | str]]:
    if scale <= 0 or not np.isfinite(scale) or not np.isfinite(additive_shift):
        raise ValueError("INVALID_DISTRIBUTION_SHIFT")
    shifted = (np.asarray(values, dtype=float) * scale + additive_shift).tolist()
    return shifted, {"data_origin": "SYNTHETIC_ROBUSTNESS_TEST", "additive_shift": additive_shift, "scale": scale}
