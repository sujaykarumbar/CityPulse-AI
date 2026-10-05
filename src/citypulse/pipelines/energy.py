from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from citypulse.energy.anomaly import add_rolling_zscore_flags
from citypulse.energy.baselines import regression_metrics
from citypulse.energy.features import add_peak_features, create_energy_features
from citypulse.energy.profile import (
    profile_energy,
    regularize_energy,
    resolve_entity_column,
    resolve_target,
)

logger = logging.getLogger(__name__)
ENERGY_FEATURE_VERSION = "0.1.0"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _profile_row(profile: dict[str, Any]) -> dict[str, Any]:
    row = {
        key: value
        for key, value in profile.items()
        if not isinstance(value, (dict, list))
    }
    row.update({f"target_{key}": value for key, value in profile["target_statistics"].items()})
    row["frequency_detected"] = profile["frequency"].get("frequency")
    row["median_interval_seconds"] = profile["frequency"].get("median_interval_seconds")
    row["regular_frequency"] = profile["frequency"].get("regular")
    row.pop("target_statistics", None)
    row.pop("frequency", None)
    return row


def _evaluate_baselines(values: pd.Series, test_start: int, season_lag: int) -> list[dict[str, Any]]:
    numeric = pd.to_numeric(values, errors="coerce").reset_index(drop=True)
    rows: list[dict[str, Any]] = []
    actual: list[float] = []
    persistence: list[float] = []
    seasonal: list[float] = []
    for index in range(test_start, len(numeric)):
        history = numeric.iloc[:index].dropna()
        if history.empty:
            continue
        current = numeric.iloc[index]
        if pd.isna(current):
            continue
        actual.append(float(current))
        persistence.append(float(history.iloc[-1]))
        if len(history) >= season_lag:
            seasonal.append(float(history.iloc[-season_lag]))
        else:
            seasonal.append(float(history.iloc[-1]))
    if actual:
        rows.extend(
            [
                {"model": "persistence", **regression_metrics(actual, persistence)},
                {"model": "seasonal_naive", **regression_metrics(actual, seasonal)},
            ]
        )
    return rows


def process_energy_csv(
    input_path: Path,
    output_dir: Path,
    report_dir: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    source = pd.read_csv(input_path)
    data_config = config.get("data", {})
    timestamp_column = str(data_config.get("timestamp_column", "timestamp"))
    target = resolve_target(source, data_config.get("target"))
    entity = resolve_entity_column(source, data_config.get("entity_column"))
    profile_before = profile_energy(source, timestamp_column, target, entity)
    regularized = regularize_energy(
        source,
        timestamp_column,
        target,
        data_config.get("resample_frequency"),
        entity,
    )
    featured = create_energy_features(
        regularized,
        target,
        timestamp_column,
        entity,
        [int(value) for value in data_config.get("lags", [])],
        [int(value) for value in data_config.get("rolling_windows", [])],
    )
    featured = add_peak_features(
        featured,
        target,
        float(config.get("peak_detection", {}).get("quantile", 0.95)),
    )
    featured = add_rolling_zscore_flags(
        featured,
        target,
        int(config.get("anomaly", {}).get("rolling_window", 24)),
        float(config.get("anomaly", {}).get("zscore_threshold", 3.0)),
    )

    values = featured[target].dropna().reset_index(drop=True)
    test_start = max(1, int(len(values) * 0.8))
    baseline_rows = _evaluate_baselines(
        values,
        test_start,
        int(config.get("forecast", {}).get("seasonal_lag", 24)),
    )
    output_path = output_dir / f"{input_path.stem}_energy_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    profile_path = report_dir / "energy" / "profile.json"
    profile_csv_path = report_dir / "energy" / "profile.csv"
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(profile_path, profile_before)
    pd.DataFrame([_profile_row(profile_before)]).to_csv(profile_csv_path, index=False)
    pd.DataFrame(baseline_rows).to_csv(report_dir / "energy" / "model_comparison.csv", index=False)
    featured.loc[featured["anomaly_flag"]].to_csv(report_dir / "energy" / "anomalies.csv", index=False)
    report = {
        "dataset": input_path.name,
        "feature_version": ENERGY_FEATURE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": target,
        "entity_column": entity,
        "input_rows": int(len(source)),
        "output_rows": int(len(featured)),
        "peak_rows": int(featured["peak_flag"].sum()),
        "rolling_anomaly_rows": int(featured["anomaly_flag"].sum()),
        "baseline_metrics": baseline_rows,
        "output_path": str(output_path),
        "status": "measured" if baseline_rows else "profiled_only",
    }
    _write_json(report_dir / "energy" / "pipeline_report.json", report)
    return report


def run_pipeline(input_dir: Path, output_dir: Path, report_dir: Path, config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    input_files = sorted(input_dir.glob("*.csv")) if input_dir.exists() else []
    reports = [process_energy_csv(path, output_dir, report_dir, config) for path in input_files]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "datasets_discovered": len(input_files),
        "datasets_processed": len(reports),
        "reports": reports,
    }
    _write_json(report_dir / "energy" / "pipeline_summary.json", summary)
    logger.info("Energy pipeline complete: datasets=%s", len(reports))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile and prepare real energy datasets.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed/energy"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/energy_ml_ready"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--config", type=Path, default=Path("config/energy.yaml"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    run_pipeline(args.input_dir, args.output_dir, args.report_dir, args.config)


if __name__ == "__main__":
    main()
