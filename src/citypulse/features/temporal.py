from __future__ import annotations

import numpy as np
import pandas as pd


def create_temporal_features(df: pd.DataFrame, timestamp_column: str = "timestamp") -> pd.DataFrame:
    """Add calendar and cyclical features from a UTC-normalized timestamp."""

    if timestamp_column not in df.columns:
        return df.copy()
    result = df.copy()
    timestamp = pd.to_datetime(result[timestamp_column], errors="coerce", utc=True)
    result[timestamp_column] = timestamp
    result["year"] = timestamp.dt.year
    result["month"] = timestamp.dt.month
    result["day"] = timestamp.dt.day
    result["hour"] = timestamp.dt.hour
    result["minute"] = timestamp.dt.minute
    result["day_of_week"] = timestamp.dt.dayofweek
    result["week_of_year"] = timestamp.dt.isocalendar().week.astype("Int64")
    result["quarter"] = timestamp.dt.quarter
    result["is_weekend"] = timestamp.dt.dayofweek.isin([5, 6])
    result["hour_sin"] = np.sin(2 * np.pi * result["hour"] / 24)
    result["hour_cos"] = np.cos(2 * np.pi * result["hour"] / 24)
    result["day_sin"] = np.sin(2 * np.pi * result["day_of_week"] / 7)
    result["day_cos"] = np.cos(2 * np.pi * result["day_of_week"] / 7)
    result["month_sin"] = np.sin(2 * np.pi * (result["month"] - 1) / 12)
    result["month_cos"] = np.cos(2 * np.pi * (result["month"] - 1) / 12)
    return result
