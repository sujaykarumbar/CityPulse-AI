from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class TemporalFrameSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame
    metadata: dict[str, Any]


def chronological_frame_split(
    frame: pd.DataFrame,
    timestamp_column: str,
    train_fraction: float = 0.7,
    validation_fraction: float = 0.15,
) -> TemporalFrameSplit:
    if timestamp_column not in frame:
        raise ValueError("REQUIRED_TIMESTAMP_COLUMN_NOT_FOUND")
    if frame.empty or not 0 < train_fraction < 1 or not 0 < validation_fraction < 1:
        raise ValueError("INVALID_CHRONOLOGICAL_SPLIT")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("INVALID_CHRONOLOGICAL_SPLIT")

    timestamps = pd.Series(pd.to_datetime(frame[timestamp_column], errors="coerce", utc=True).array)
    if timestamps.isna().any():
        raise ValueError("INVALID_OR_MISSING_TIMESTAMP")

    order = timestamps.sort_values(kind="stable").index
    ordered = frame.iloc[order].reset_index(drop=True)
    ordered_timestamps = timestamps.iloc[order].reset_index(drop=True)
    unique_timestamps = ordered_timestamps.drop_duplicates().tolist()
    train_end = int(len(unique_timestamps) * train_fraction)
    validation_end = train_end + int(len(unique_timestamps) * validation_fraction)
    if train_end < 1 or validation_end <= train_end or validation_end >= len(unique_timestamps):
        raise ValueError("INSUFFICIENT_TIMESTAMPS_FOR_SPLIT")

    train_cutoff = unique_timestamps[train_end - 1]
    validation_cutoff = unique_timestamps[validation_end - 1]
    train_mask = ordered_timestamps <= train_cutoff
    validation_mask = (ordered_timestamps > train_cutoff) & (ordered_timestamps <= validation_cutoff)
    test_mask = ordered_timestamps > validation_cutoff
    train = ordered.loc[train_mask].copy()
    validation = ordered.loc[validation_mask].copy()
    test = ordered.loc[test_mask].copy()
    train_timestamps = ordered_timestamps.loc[train_mask]
    validation_timestamps = ordered_timestamps.loc[validation_mask]
    test_timestamps = ordered_timestamps.loc[test_mask]

    if not (train_timestamps.max() < validation_timestamps.min() < test_timestamps.min()):
        raise ValueError("CHRONOLOGICAL_SPLIT_INVARIANT_FAILED")

    return TemporalFrameSplit(
        train=train,
        validation=validation,
        test=test,
        metadata={
            "status": "SPLIT_CREATED",
            "timestamp_column": timestamp_column,
            "train_end": train_timestamps.max().isoformat(),
            "validation_start": validation_timestamps.min().isoformat(),
            "validation_end": validation_timestamps.max().isoformat(),
            "test_start": test_timestamps.min().isoformat(),
            "leakage_controls": [
                "rows sorted by parsed UTC timestamp",
                "records with identical timestamps remain in one partition",
                "training and validation partitions contain no later timestamps",
            ],
        },
    )