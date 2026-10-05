from __future__ import annotations

from typing import Any

import numpy as np


def regression_metrics(actual: list[float], predicted: list[float]) -> dict[str, float | str]:
    if not actual or len(actual) != len(predicted):
        return {"status": "GROUND_TRUTH_NOT_AVAILABLE"}
    errors = np.asarray(actual, dtype=float) - np.asarray(predicted, dtype=float)
    denominator = np.abs(actual).sum()
    return {"status": "measured", "MAE": float(np.mean(np.abs(errors))), "RMSE": float(np.sqrt(np.mean(errors**2))), "WAPE": float(np.abs(errors).sum() / denominator) if denominator else float("nan")}


def prediction_summary(predictions: list[float]) -> dict[str, Any]:
    if not predictions:
        return {"status": "NO_DATA_AVAILABLE"}
    values = np.asarray(predictions, dtype=float)
    return {"status": "measured", "count": len(values), "mean": float(values.mean()), "std": float(values.std()), "minimum": float(values.min()), "maximum": float(values.max())}
