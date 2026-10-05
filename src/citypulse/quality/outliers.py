from __future__ import annotations

import pandas as pd


def add_outlier_flags(
    df: pd.DataFrame,
    columns: list[str],
    iqr_multiplier: float = 1.5,
    zscore_threshold: float = 3.0,
) -> pd.DataFrame:
    """Add non-destructive IQR and z-score flags for selected numeric columns."""

    result = df.copy()
    for column in columns:
        if column not in result.columns or not pd.api.types.is_numeric_dtype(result[column]):
            continue
        series = result[column]
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - iqr_multiplier * iqr, q3 + iqr_multiplier * iqr
        result[f"{column}_outlier_iqr"] = (series < lower) | (series > upper)
        standard_deviation = series.std()
        if pd.isna(standard_deviation) or standard_deviation == 0:
            result[f"{column}_outlier_zscore"] = False
        else:
            result[f"{column}_outlier_zscore"] = (
                (series - series.mean()).abs() / standard_deviation > zscore_threshold
            )
    return result
