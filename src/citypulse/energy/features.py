from __future__ import annotations

import numpy as np
import pandas as pd


def create_energy_features(
    df: pd.DataFrame,
    target: str,
    timestamp_column: str = "timestamp",
    entity_column: str | None = None,
    lags: list[int] | None = None,
    rolling_windows: list[int] | None = None,
) -> pd.DataFrame:
    """Create calendar, lag, and strictly past-only rolling energy features."""

    result = df.copy().sort_values([entity_column, timestamp_column] if entity_column else timestamp_column)
    timestamp = pd.to_datetime(result[timestamp_column], errors="coerce", utc=True)
    result[timestamp_column] = timestamp
    result[target] = pd.to_numeric(result[target], errors="coerce")
    result["hour"] = timestamp.dt.hour
    result["day_of_week"] = timestamp.dt.dayofweek
    result["day_of_month"] = timestamp.dt.day
    result["month"] = timestamp.dt.month
    result["quarter"] = timestamp.dt.quarter
    result["is_weekend"] = timestamp.dt.dayofweek.isin([5, 6])
    result["hour_sin"] = np.sin(2 * np.pi * result["hour"] / 24)
    result["hour_cos"] = np.cos(2 * np.pi * result["hour"] / 24)
    result["day_sin"] = np.sin(2 * np.pi * result["day_of_week"] / 7)
    result["day_cos"] = np.cos(2 * np.pi * result["day_of_week"] / 7)
    result["month_sin"] = np.sin(2 * np.pi * (result["month"] - 1) / 12)
    result["month_cos"] = np.cos(2 * np.pi * (result["month"] - 1) / 12)

    groups = result.groupby(entity_column, sort=False)[target] if entity_column else None
    for lag in lags or []:
        result[f"{target}_lag_{lag}"] = groups.shift(lag) if groups is not None else result[target].shift(lag)
    for window in rolling_windows or []:
        if groups is None:
            past = result[target].shift(1)
            rolling = past.rolling(window, min_periods=1)
            result[f"{target}_rolling_mean_{window}"] = rolling.mean()
            result[f"{target}_rolling_std_{window}"] = rolling.std()
            result[f"{target}_rolling_min_{window}"] = rolling.min()
            result[f"{target}_rolling_max_{window}"] = rolling.max()
        else:
            past = groups.shift(1)
            grouped_past = past.groupby(result[entity_column], sort=False)
            result[f"{target}_rolling_mean_{window}"] = grouped_past.transform(
                lambda values: values.rolling(window, min_periods=1).mean()
            )
            result[f"{target}_rolling_std_{window}"] = grouped_past.transform(
                lambda values: values.rolling(window, min_periods=2).std()
            )
            result[f"{target}_rolling_min_{window}"] = grouped_past.transform(
                lambda values: values.rolling(window, min_periods=1).min()
            )
            result[f"{target}_rolling_max_{window}"] = grouped_past.transform(
                lambda values: values.rolling(window, min_periods=1).max()
            )
    return result.reset_index(drop=True)


def add_peak_features(df: pd.DataFrame, target: str, quantile: float = 0.95) -> pd.DataFrame:
    if not 0 < quantile < 1:
        raise ValueError("peak quantile must be between 0 and 1")
    result = df.copy()
    threshold = result[target].quantile(quantile)
    result["peak_flag"] = result[target] >= threshold
    result["peak_rank"] = result[target].rank(method="dense", ascending=False).astype("Int64")
    result["distance_from_peak"] = result[target] - threshold
    return result
