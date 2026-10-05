from __future__ import annotations

from typing import Any

import pandas as pd

ORIGIN_CANDIDATES = ("origin_zone", "origin_id", "origin", "from_zone")
DESTINATION_CANDIDATES = ("destination_zone", "destination_id", "destination", "to_zone")
DEMAND_CANDIDATES = ("trip_count", "passenger_count", "demand", "count")


def _first_present(df: pd.DataFrame, candidates: tuple[str, ...]) -> str | None:
    return next((column for column in candidates if column in df.columns), None)


def resolve_mobility_columns(df: pd.DataFrame) -> dict[str, str | None]:
    return {
        "timestamp": "timestamp" if "timestamp" in df.columns else None,
        "origin": _first_present(df, ORIGIN_CANDIDATES),
        "destination": _first_present(df, DESTINATION_CANDIDATES),
        "demand": _first_present(df, DEMAND_CANDIDATES),
        "duration": _first_present(df, ("duration", "trip_duration", "travel_time")),
        "distance": _first_present(df, ("distance", "trip_distance")),
        "mode": _first_present(df, ("mode", "transport_mode")),
    }


def profile_mobility(df: pd.DataFrame) -> dict[str, Any]:
    columns = resolve_mobility_columns(df)
    timestamp = (
        pd.to_datetime(df[columns["timestamp"]], errors="coerce", utc=True)
        if columns["timestamp"]
        else pd.Series(dtype="datetime64[ns, UTC]")
    )
    report: dict[str, Any] = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "columns_by_type": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "resolved_columns": columns,
        "missing_values": {column: int(value) for column, value in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_timestamps": int(timestamp.isna().sum()) if columns["timestamp"] else None,
        "timestamp_min": timestamp.min().isoformat() if timestamp.notna().any() else None,
        "timestamp_max": timestamp.max().isoformat() if timestamp.notna().any() else None,
        "origin_count": int(df[columns["origin"]].nunique(dropna=True)) if columns["origin"] else None,
        "destination_count": int(df[columns["destination"]].nunique(dropna=True)) if columns["destination"] else None,
        "unique_od_pairs": int(
            df[[columns["origin"], columns["destination"]]].dropna().drop_duplicates().shape[0]
        )
        if columns["origin"] and columns["destination"]
        else None,
        "mode_distribution": (
            {str(key): int(value) for key, value in df[columns["mode"]].value_counts(dropna=False).items()}
            if columns["mode"]
            else None
        ),
    }
    for label, column in (("duration", columns["duration"]), ("distance", columns["distance"])):
        if column:
            values = pd.to_numeric(df[column], errors="coerce")
            report[f"{label}_statistics"] = {
                "minimum": float(values.min()) if values.notna().any() else None,
                "median": float(values.median()) if values.notna().any() else None,
                "mean": float(values.mean()) if values.notna().any() else None,
                "maximum": float(values.max()) if values.notna().any() else None,
            }
        else:
            report[f"{label}_statistics"] = None
    return report


def validate_mobility_records(df: pd.DataFrame) -> pd.DataFrame:
    """Add quality flags without deleting legitimate extreme observations."""

    result = df.copy()
    columns = resolve_mobility_columns(result)
    valid = pd.Series(True, index=result.index)
    if columns["timestamp"]:
        parsed = pd.to_datetime(result[columns["timestamp"]], errors="coerce", utc=True)
        valid &= parsed.notna()
    for field in ("duration", "distance"):
        column = columns[field]
        if column:
            values = pd.to_numeric(result[column], errors="coerce")
            valid &= values.notna() & (values >= 0)
    if columns["origin"]:
        valid &= result[columns["origin"]].notna()
    if columns["destination"]:
        valid &= result[columns["destination"]].notna()
    result["quality_flag"] = valid.map({True: "valid", False: "invalid"})
    return result
