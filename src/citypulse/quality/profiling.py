from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _json_value(value: Any) -> Any:
    if isinstance(value, (pd.Timestamp, pd.Timedelta)):
        return value.isoformat()
    if isinstance(value, np.generic):
        return value.item()
    if pd.isna(value):
        return None
    return value


def _timestamp_column(df: pd.DataFrame) -> str | None:
    for column in df.columns:
        if "timestamp" in column or column in {"datetime", "date", "time"}:
            return column
    return None


def profile_dataframe(df: pd.DataFrame, correlation_threshold: float = 0.9) -> dict[str, Any]:
    """Return JSON-serializable descriptive statistics for a dataframe."""

    numeric = df.select_dtypes(include="number")
    categorical = df.select_dtypes(exclude="number")
    missing_counts = df.isna().sum()
    profile: dict[str, Any] = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "dtypes": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "missing_values": {column: int(value) for column, value in missing_counts.items()},
        "missing_percentages": {
            column: float(value / len(df) * 100) if len(df) else 0.0
            for column, value in missing_counts.items()
        },
        "unique_values": {column: int(df[column].nunique(dropna=True)) for column in df.columns},
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_statistics": {},
        "categorical_statistics": {},
        "timestamp_range": None,
        "geographic_range": {},
        "constant_columns": [column for column in df.columns if df[column].nunique(dropna=False) <= 1],
        "highly_correlated_features": [],
    }

    if not numeric.empty:
        stats = numeric.describe(percentiles=[0.25, 0.5, 0.75]).transpose()
        profile["numeric_statistics"] = {
            column: {key: _json_value(value) for key, value in row.items()}
            for column, row in stats.iterrows()
        }

        correlation = numeric.corr(method="pearson")
        for left_index, left in enumerate(correlation.columns):
            for right in correlation.columns[left_index + 1 :]:
                value = correlation.loc[left, right]
                if pd.notna(value) and abs(value) >= correlation_threshold:
                    profile["highly_correlated_features"].append(
                        {"left": left, "right": right, "correlation": float(value)}
                    )

    if not categorical.empty:
        for column in categorical.columns:
            counts = categorical[column].value_counts(dropna=False)
            profile["categorical_statistics"][column] = {
                "unique_count": int(categorical[column].nunique(dropna=True)),
                "dominant_category": _json_value(counts.index[0]) if not counts.empty else None,
                "frequencies": {
                    str(_json_value(key)): int(value) for key, value in counts.head(20).items()
                },
                "rare_categories": [
                    str(_json_value(key)) for key, value in counts.items() if value == 1
                ][:20],
            }

    timestamp_column = _timestamp_column(df)
    if timestamp_column:
        timestamps = pd.to_datetime(df[timestamp_column], errors="coerce", utc=True).dropna()
        if not timestamps.empty:
            profile["timestamp_range"] = {
                "column": timestamp_column,
                "min": timestamps.min().isoformat(),
                "max": timestamps.max().isoformat(),
            }

    for latitude, longitude in (("latitude", "longitude"), ("lat", "lon")):
        if latitude in df.columns and longitude in df.columns:
            profile["geographic_range"] = {
                "latitude": {"min": _json_value(df[latitude].min()), "max": _json_value(df[latitude].max())},
                "longitude": {"min": _json_value(df[longitude].min()), "max": _json_value(df[longitude].max())},
            }
            break

    return profile
