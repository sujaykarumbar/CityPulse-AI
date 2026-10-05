from __future__ import annotations

import math

import numpy as np


def regression_metrics(observed: list[float], predicted: list[float]) -> dict[str, float | str]:
    if not observed:
        return {"status": "GROUND_TRUTH_NOT_AVAILABLE"}
    if len(observed) != len(predicted):
        raise ValueError("OBSERVED_PREDICTED_LENGTH_MISMATCH")
    y = np.asarray(observed, dtype=float)
    p = np.asarray(predicted, dtype=float)
    if not np.isfinite(y).all() or not np.isfinite(p).all():
        raise ValueError("NON_FINITE_VALIDATION_VALUES")
    error = y - p
    denom = np.abs(y).sum()
    smape_denom = np.abs(y) + np.abs(p)
    smape = float(np.mean(np.divide(2 * np.abs(error), smape_denom, out=np.zeros_like(error), where=smape_denom != 0)))
    result: dict[str, float | str] = {
        "status": "MEASURED",
        "MAE": float(np.mean(np.abs(error))),
        "RMSE": float(math.sqrt(np.mean(error**2))),
        "WAPE": float(np.abs(error).sum() / denom) if denom else "NOT_MEASURED",
        "sMAPE": smape,
        "bias": float(np.mean(p - y)),
    }
    if len(y) > 1 and float(np.var(y)) > 0:
        result["R2"] = float(1 - np.sum(error**2) / np.sum((y - np.mean(y)) ** 2))
    else:
        result["R2"] = "NOT_MEASURED"
    return result
