from __future__ import annotations

import pandas as pd


def add_demand_anomaly_flags(
    df: pd.DataFrame,
    demand_column: str = "trip_count",
    group_column: str | None = None,
    window: int = 24,
    threshold: float = 3.0,
) -> pd.DataFrame:
    if demand_column not in df.columns:
        raise ValueError(f"Missing demand column '{demand_column}'")
    result = df.copy()
    values = pd.to_numeric(result[demand_column], errors="coerce")
    if group_column and group_column in result.columns:
        past = result.groupby(group_column, sort=False)[demand_column].shift(1)
        grouped = past.groupby(result[group_column], sort=False)
        mean = grouped.transform(lambda values: values.rolling(window, min_periods=2).mean())
        std = grouped.transform(lambda values: values.rolling(window, min_periods=2).std())
    else:
        past = values.shift(1)
        mean = past.rolling(window, min_periods=2).mean()
        std = past.rolling(window, min_periods=2).std()
    result["anomaly_score"] = ((values - mean) / std).abs()
    result["anomaly_flag"] = result["anomaly_score"] > threshold
    result["anomaly_method"] = "rolling_zscore"
    return result
