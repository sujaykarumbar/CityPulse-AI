from __future__ import annotations

import logging

import pandas as pd

from citypulse.quality.validation import validation_mask

logger = logging.getLogger(__name__)


def normalize_column_name(column: str) -> str:
    return "_".join(str(column).strip().lower().replace("-", "_").split())


def clean_dataframe(df: pd.DataFrame, drop_duplicates: bool = False) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize columns, parse timestamps, and remove only demonstrably invalid rows."""

    cleaned = df.copy()
    cleaned.columns = [normalize_column_name(column) for column in cleaned.columns]
    timestamp_columns = [
        column
        for column in cleaned.columns
        if "timestamp" in column or column in {"datetime", "date", "time"}
    ]
    for column in timestamp_columns[:1]:
        cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce", utc=True)

    before = len(cleaned)
    valid = validation_mask(cleaned)
    cleaned = cleaned.loc[valid].copy()
    rejected = before - len(cleaned)
    duplicate_count = int(cleaned.duplicated().sum())
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates().copy()
    logger.info("Cleaned rows: input=%s output=%s rejected=%s", before, len(cleaned), rejected)
    return cleaned, {"input_rows": before, "rejected_rows": rejected, "duplicate_rows": duplicate_count}
