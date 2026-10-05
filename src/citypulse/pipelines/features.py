from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from citypulse.features.leakage import find_leakage_risks
from citypulse.features.spatial import create_spatial_features
from citypulse.features.temporal import create_temporal_features
from citypulse.features.traffic import create_lag_and_rolling_features, create_traffic_features
from citypulse.quality.cleaning import clean_dataframe
from citypulse.quality.outliers import add_outlier_flags
from citypulse.quality.profiling import profile_dataframe
from citypulse.quality.validation import validate_dataframe

logger = logging.getLogger(__name__)
FEATURE_VERSION = "0.1.0"


def load_feature_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def process_csv(
    input_path: Path,
    output_dir: Path,
    report_dir: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    source = pd.read_csv(input_path)
    profile_before = profile_dataframe(
        source, correlation_threshold=float(config.get("correlation_threshold", 0.9))
    )
    validation_before = validate_dataframe(source)
    cleaned, cleaning_stats = clean_dataframe(source)
    timestamp_column = str(config.get("timestamp_column", "timestamp"))
    featured = create_temporal_features(cleaned, timestamp_column)
    featured = create_lag_and_rolling_features(
        featured,
        target_columns=list(config.get("target_columns", [])),
        lags=[int(value) for value in config.get("lag_windows", [])],
        rolling_windows=[int(value) for value in config.get("rolling_windows", [])],
        timestamp_column=timestamp_column,
    )
    featured = create_traffic_features(featured)
    featured = create_spatial_features(featured)
    featured = add_outlier_flags(featured, list(config.get("target_columns", [])))
    leakage_risks = find_leakage_risks(featured, timestamp_column=timestamp_column)

    output_path = output_dir / f"{input_path.stem}_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    report = {
        "dataset": input_path.name,
        "feature_version": FEATURE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "processing_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "input_rows": int(len(source)),
        "output_rows": int(len(featured)),
        "rejected_rows": cleaning_stats["rejected_rows"],
        "duplicate_rows_before_cleaning": cleaning_stats["duplicate_rows"],
        "missing_values_before": profile_before["missing_values"],
        "missing_values_after": {key: int(value) for key, value in featured.isna().sum().items()},
        "quality": validation_before,
        "generated_features": [column for column in featured.columns if column not in source.columns],
        "leakage_risks": leakage_risks,
        "output_path": str(output_path),
    }
    _write_json(report_dir / "data_quality" / f"{input_path.stem}_quality.json", report)
    _write_json(report_dir / "feature_reports" / f"{input_path.stem}_features.json", report)
    return report


def run_pipeline(
    input_dir: Path,
    output_dir: Path,
    report_dir: Path,
    config_path: Path,
) -> dict[str, Any]:
    config = load_feature_config(config_path)
    input_files = sorted(input_dir.glob("*.csv")) if input_dir.exists() else []
    reports = [process_csv(path, output_dir, report_dir, config) for path in input_files]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_directory": str(input_dir),
        "datasets_discovered": len(input_files),
        "datasets_processed": len(reports),
        "reports": reports,
    }
    _write_json(report_dir / "feature_pipeline_summary.json", summary)
    logger.info("Feature pipeline complete: datasets=%s", len(reports))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build profiled, validated ML-ready CSV datasets.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed/input"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/ml_ready"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--config", type=Path, default=Path("config/features.yaml"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    run_pipeline(args.input_dir, args.output_dir, args.report_dir, args.config)


if __name__ == "__main__":
    main()
