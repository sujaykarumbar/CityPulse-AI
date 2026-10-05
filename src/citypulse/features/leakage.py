from __future__ import annotations

import pandas as pd


def find_leakage_risks(
    df: pd.DataFrame,
    target_column: str | None = None,
    timestamp_column: str = "timestamp",
) -> list[dict[str, str]]:
    """Report suspicious feature names and unsorted temporal inputs for review."""

    risks: list[dict[str, str]] = []
    if target_column:
        for column in df.columns:
            if column != target_column and target_column in column:
                risks.append({"column": column, "reason": "column name contains target name"})
    if timestamp_column in df.columns:
        timestamps = pd.to_datetime(df[timestamp_column], errors="coerce", utc=True)
        if not timestamps.is_monotonic_increasing:
            risks.append({"column": timestamp_column, "reason": "timestamps are not sorted"})
    for column in df.columns:
        if any(token in column.lower() for token in ("future", "post_event", "outcome")):
            risks.append({"column": column, "reason": "name suggests post-observation information"})
    return risks
