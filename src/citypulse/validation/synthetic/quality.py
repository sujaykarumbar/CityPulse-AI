from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def synthetic_quality_report(frame: pd.DataFrame, timestamp_column: str = "timestamp") -> dict[str, Any]:
    if "data_origin" not in frame.columns or not (frame["data_origin"] == "SYNTHETIC").all():
        raise ValueError("SYNTHETIC_PROVENANCE_REQUIRED")
    report: dict[str, Any] = {
        "data_origin": "SYNTHETIC",
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "missing_values": {key: int(value) for key, value in frame.isna().sum().items()},
        "duplicate_rows": int(
            frame.drop(columns=[column for column in ("generation_config",) if column in frame]).duplicated().sum()
        ),
        "finite_numeric_columns": {},
    }
    for column in frame.select_dtypes(include="number"):
        report["finite_numeric_columns"][column] = bool(np.isfinite(frame[column].to_numpy(dtype=float)).all())
    if timestamp_column in frame:
        parsed = pd.to_datetime(frame[timestamp_column], errors="coerce", utc=True)
        report["invalid_timestamps"] = int(parsed.isna().sum())
        report["timestamp_min"] = parsed.min().isoformat() if parsed.notna().any() else None
        report["timestamp_max"] = parsed.max().isoformat() if parsed.notna().any() else None
    report["status"] = "MEASURED" if len(frame) else "NO_DATA_AVAILABLE"
    return report
