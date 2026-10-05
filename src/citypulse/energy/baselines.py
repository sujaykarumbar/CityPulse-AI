from __future__ import annotations

import numpy as np
import pandas as pd


def persistence_forecast(values: pd.Series, horizon: int) -> np.ndarray:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if values.dropna().empty:
        raise ValueError("cannot forecast an empty series")
    return np.repeat(float(values.dropna().iloc[-1]), horizon)


def seasonal_naive_forecast(values: pd.Series, horizon: int, season_lag: int) -> np.ndarray:
    if season_lag < 1 or len(values.dropna()) < season_lag:
        raise ValueError("season_lag must be positive and supported by the observed history")
    history = values.dropna().to_numpy()
    return np.resize(history[-season_lag:], horizon).astype(float)


def regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    error = actual_array - predicted_array
    denominator = np.abs(actual_array).sum()
    smape_denominator = np.abs(actual_array) + np.abs(predicted_array)
    smape = np.mean(
        np.divide(2 * np.abs(error), smape_denominator, out=np.zeros_like(error), where=smape_denominator != 0)
    )
    return {
        "MAE": float(np.mean(np.abs(error))),
        "RMSE": float(np.sqrt(np.mean(error**2))),
        "sMAPE": float(smape),
        "WAPE": float(np.abs(error).sum() / denominator) if denominator else float("nan"),
    }
