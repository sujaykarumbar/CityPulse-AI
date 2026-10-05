from __future__ import annotations

import numpy as np


def summarize_robustness(values: list[float]) -> dict[str, float | str]:
    if not values:
        return {"status": "NOT_RUN"}
    array = np.asarray(values, dtype=float)
    return {
        "status": "measured",
        "minimum": float(array.min()),
        "median": float(np.median(array)),
        "maximum": float(array.max()),
        "standard_deviation": float(array.std()),
    }
