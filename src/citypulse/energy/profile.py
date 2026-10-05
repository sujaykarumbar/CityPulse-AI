from __future__ import annotations

from typing import Any

import pandas as pd

TARGET_CANDIDATES = ("electricity_load", "energy_consumption", "power_demand", "demand", "load")


def resolve_target(df: pd.DataFrame, configured_target: str | None = None) -> str:
    if configured_target:
        if configured_target not in df.columns:
            raise ValueError(f"Configured energy target '{configured_target}' is not present")
        return configured_target
    for candidate in TARGET_CANDIDATES:
        if candidate in df.columns:
            return candidate
    raise ValueError(
        "No energy target found. Configure target to one of the available numeric demand columns."
    )


def resolve_entity_column(df: pd.DataFrame, configured_entity: str | None = None) -> str | None:
    if configured_entity:
        if configured_entity not in df.columns:
            raise ValueError(f"Configured energy entity '{configured_entity}' is not present")
        return configured_entity
    for candidate in ("entity_id", "zone_id", "meter_id", "building_id", "substation_id"):
        if candidate in df.columns:
            return candidate
    return None


def detect_frequency(df: pd.DataFrame, timestamp_column: str = "timestamp") -> dict[str, Any]:
    if timestamp_column not in df.columns:
        raise ValueError(f"Missing timestamp column '{timestamp_column}'")
    timestamps = pd.to_datetime(df[timestamp_column], errors="coerce", utc=True).dropna().sort_values()
    unique = timestamps.drop_duplicates()
    if len(unique) < 3:
        return {"frequency": None, "median_interval_seconds": None, "regular": False}
    deltas = unique.diff().dropna().dt.total_seconds()
    median_seconds = float(deltas.median())
    return {
        "frequency": pd.infer_freq(unique),
        "median_interval_seconds": median_seconds,
        "regular": bool(deltas.nunique() == 1),
    }


def profile_energy(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp",
    target: str | None = None,
    entity_column: str | None = None,
) -> dict[str, Any]:
    target_column = resolve_target(df, target)
    entity = resolve_entity_column(df, entity_column)
    timestamps = pd.to_datetime(df[timestamp_column], errors="coerce", utc=True)
    values = pd.to_numeric(df[target_column], errors="coerce")
    frequency = detect_frequency(df, timestamp_column)
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "columns_by_type": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "target": target_column,
        "entity_column": entity,
        "entity_count": int(df[entity].nunique(dropna=True)) if entity else 1,
        "missing_values": {column: int(value) for column, value in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "timestamp_invalid": int(timestamps.isna().sum()),
        "timestamp_min": timestamps.min().isoformat() if timestamps.notna().any() else None,
        "timestamp_max": timestamps.max().isoformat() if timestamps.notna().any() else None,
        "frequency": frequency,
        "target_statistics": {
            "minimum": float(values.min()) if values.notna().any() else None,
            "maximum": float(values.max()) if values.notna().any() else None,
            "mean": float(values.mean()) if values.notna().any() else None,
            "median": float(values.median()) if values.notna().any() else None,
            "standard_deviation": float(values.std()) if values.notna().any() else None,
        },
    }


def regularize_energy(
    df: pd.DataFrame,
    timestamp_column: str,
    target: str,
    frequency: str | None = None,
    entity_column: str | None = None,
) -> pd.DataFrame:
    """Optionally resample data; no resampling occurs when frequency is unset."""

    result = df.copy()
    result[timestamp_column] = pd.to_datetime(result[timestamp_column], errors="coerce", utc=True)
    result = result.dropna(subset=[timestamp_column]).sort_values(timestamp_column)
    if not frequency:
        return result.reset_index(drop=True)

    result[target] = pd.to_numeric(result[target], errors="coerce")
    if entity_column:
        result = (
            result.set_index(timestamp_column)
            .groupby(entity_column)[target]
            .resample(frequency)
            .mean()
            .rename(target)
            .reset_index()
        )
    else:
        result = result.set_index(timestamp_column)[target].resample(frequency).mean().reset_index()
    return result
