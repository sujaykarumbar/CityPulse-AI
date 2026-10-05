from __future__ import annotations

import numpy as np
import pandas as pd


def create_mobility_features(df: pd.DataFrame, timestamp_column: str = "timestamp") -> pd.DataFrame:
    result = df.copy()
    if timestamp_column not in result.columns:
        return result
    timestamp = pd.to_datetime(result[timestamp_column], errors="coerce", utc=True)
    result[timestamp_column] = timestamp
    result["hour"] = timestamp.dt.hour
    result["day_of_week"] = timestamp.dt.dayofweek
    result["day_of_month"] = timestamp.dt.day
    result["month"] = timestamp.dt.month
    result["is_weekend"] = timestamp.dt.dayofweek.isin([5, 6])
    result["hour_sin"] = np.sin(2 * np.pi * result["hour"] / 24)
    result["hour_cos"] = np.cos(2 * np.pi * result["hour"] / 24)
    result["day_sin"] = np.sin(2 * np.pi * result["day_of_week"] / 7)
    result["day_cos"] = np.cos(2 * np.pi * result["day_of_week"] / 7)
    return result


def add_travel_speed_flag(
    df: pd.DataFrame,
    distance_column: str = "distance",
    duration_column: str = "duration",
    max_speed_kmh: float = 200.0,
) -> pd.DataFrame:
    """Flag implausible estimated speeds; units must be km and hours."""

    result = df.copy()
    if distance_column not in result or duration_column not in result:
        return result
    distance = pd.to_numeric(result[distance_column], errors="coerce")
    duration = pd.to_numeric(result[duration_column], errors="coerce")
    result["estimated_speed_kmh"] = distance / duration.replace(0, np.nan)
    result["speed_quality_flag"] = result["estimated_speed_kmh"].le(max_speed_kmh).fillna(False)
    return result
