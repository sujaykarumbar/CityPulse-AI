from __future__ import annotations

import pandas as pd


def add_rolling_zscore_flags(
    df: pd.DataFrame,
    target: str,
    window: int = 24,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """Flag potential anomalies; flags are not claims of real-world events."""

    if window < 2 or threshold <= 0:
        raise ValueError("window must be at least 2 and threshold must be positive")
    result = df.copy()
    past = result[target].shift(1)
    mean = past.rolling(window, min_periods=2).mean()
    std = past.rolling(window, min_periods=2).std()
    result["anomaly_score"] = ((result[target] - mean) / std).abs()
    result["anomaly_flag"] = result["anomaly_score"] > threshold
    result["anomaly_method"] = "rolling_zscore"
    return result


def add_isolation_forest_flags(
    df: pd.DataFrame,
    target: str,
    contamination: float = "auto",
    random_state: int = 42,
) -> pd.DataFrame:
    """Optionally add an ML anomaly flag using only the observed target."""

    from sklearn.ensemble import IsolationForest

    result = df.copy()
    values = result[[target]].astype(float)
    valid = values[target].notna()
    result["isolation_forest_score"] = float("nan")
    result["isolation_forest_flag"] = False
    if valid.any():
        model = IsolationForest(contamination=contamination, random_state=random_state)
        model.fit(values.loc[valid])
        result.loc[valid, "isolation_forest_score"] = -model.score_samples(values.loc[valid])
        result.loc[valid, "isolation_forest_flag"] = model.predict(values.loc[valid]) == -1
    return result
