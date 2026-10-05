from __future__ import annotations

from typing import Any

import pandas as pd


def _coordinate_columns(df: pd.DataFrame) -> tuple[str, str] | None:
    columns = {str(column).strip().lower(): column for column in df.columns}
    for latitude, longitude in (("latitude", "longitude"), ("lat", "lon")):
        if latitude in columns and longitude in columns:
            return columns[latitude], columns[longitude]
    return None


def validation_mask(df: pd.DataFrame) -> pd.Series:
    """Return rows satisfying generic urban-data validity rules."""

    valid = pd.Series(True, index=df.index)
    coordinates = _coordinate_columns(df)
    if coordinates:
        latitude, longitude = coordinates
        latitude_values = pd.to_numeric(df[latitude], errors="coerce")
        longitude_values = pd.to_numeric(df[longitude], errors="coerce")
        valid &= latitude_values.between(-90, 90, inclusive="both")
        valid &= longitude_values.between(-180, 180, inclusive="both")
        valid &= df[latitude].notna() & df[longitude].notna()

    columns = {str(column).strip().lower(): column for column in df.columns}
    for name in ("speed", "average_speed", "vehicle_count", "energy_consumption", "demand"):
        if name in columns:
            column = columns[name]
            values = pd.to_numeric(df[column], errors="coerce")
            valid &= df[column].isna() | (values.notna() & (values >= 0))

    for name, column in columns.items():
        if "timestamp" in name or name in {"datetime", "date", "time"}:
            parsed = pd.to_datetime(df[column], errors="coerce", utc=True)
            valid &= parsed.notna()
            break

    return valid


def quality_dimensions(df: pd.DataFrame) -> dict[str, float]:
    """Calculate measurable 0-1 quality dimensions for the scoring formula."""

    cells = max(len(df) * max(len(df.columns), 1), 1)
    completeness = float(df.notna().sum().sum() / cells)
    valid = validation_mask(df)
    validity = float(valid.mean()) if len(df) else 1.0
    uniqueness = 1.0 - (float(df.duplicated().sum()) / len(df) if len(df) else 0.0)
    uniqueness = max(0.0, uniqueness)
    consistency = float(
        (df.columns.str.match(r"^[a-z][a-z0-9_]*$").mean()) if len(df.columns) else 1.0
    )
    return {
        "completeness": completeness,
        "validity": validity,
        "uniqueness": uniqueness,
        "consistency": consistency,
    }


def quality_score(dimensions: dict[str, float]) -> float:
    """Weighted quality score; weights are documented in docs/data_quality.md."""

    weights = {"completeness": 0.35, "validity": 0.30, "uniqueness": 0.20, "consistency": 0.15}
    return round(100 * sum(weights[key] * dimensions.get(key, 0.0) for key in weights), 2)


def validate_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    dimensions = quality_dimensions(df)
    return {
        "rows": int(len(df)),
        "valid_rows": int(validation_mask(df).sum()),
        "rejected_rows": int((~validation_mask(df)).sum()),
        "dimensions": dimensions,
        "quality_score": quality_score(dimensions),
    }
