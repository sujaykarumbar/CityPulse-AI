from __future__ import annotations

import pandas as pd


def _group_columns(df: pd.DataFrame) -> list[str]:
    return [column for column in ("road_id", "zone_id") if column in df.columns]


def create_lag_and_rolling_features(
    df: pd.DataFrame,
    target_columns: list[str],
    lags: list[int],
    rolling_windows: list[int],
    timestamp_column: str = "timestamp",
) -> pd.DataFrame:
    """Create past-only lag and rolling features, grouped by road or zone when available."""

    result = df.copy()
    groups = _group_columns(result)
    order = result.sort_values(timestamp_column).index if timestamp_column in result.columns else result.index
    for target in target_columns:
        if target not in result.columns:
            continue
        if groups:
            grouped = result.loc[order].groupby(groups, sort=False)[target]
            for lag in lags:
                result.loc[order, f"{target}_lag_{lag}"] = grouped.shift(lag).to_numpy()
            for window in rolling_windows:
                shifted = grouped.shift(1)
                result.loc[order, f"{target}_rolling_mean_{window}"] = (
                    shifted.groupby([result.loc[order, group] for group in groups], sort=False)
                    .transform(lambda values: values.rolling(window, min_periods=1).mean())
                    .to_numpy()
                )
        else:
            series = result.loc[order, target]
            for lag in lags:
                result.loc[order, f"{target}_lag_{lag}"] = series.shift(lag)
            for window in rolling_windows:
                result.loc[order, f"{target}_rolling_mean_{window}"] = (
                    series.shift(1).rolling(window, min_periods=1).mean().to_numpy()
                )
    return result


def create_traffic_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add domain features only when their source measurements exist."""

    result = df.copy()
    groups = _group_columns(result)
    if "vehicle_count" in result.columns:
        if groups:
            result["traffic_change_rate"] = result.groupby(groups, sort=False)["vehicle_count"].pct_change()
        else:
            result["traffic_change_rate"] = result["vehicle_count"].pct_change()
    if "average_speed" in result.columns and "speed_limit" in result.columns:
        result["speed_ratio_to_limit"] = result["average_speed"] / result["speed_limit"].replace(0, pd.NA)
    return result
