from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from citypulse.mobility.anomaly import add_demand_anomaly_flags
from citypulse.mobility.features import add_travel_speed_flag, create_mobility_features
from citypulse.mobility.graph import build_mobility_graph, graph_metrics, graph_statistics
from citypulse.mobility.od import build_od_matrix
from citypulse.mobility.profile import profile_mobility, resolve_mobility_columns, validate_mobility_records

logger = logging.getLogger(__name__)
MOBILITY_FEATURE_VERSION = "0.1.0"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def process_mobility_csv(input_path: Path, output_dir: Path, report_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    source = pd.read_csv(input_path)
    data_config = config.get("data", {})
    columns = resolve_mobility_columns(source)
    timestamp_column = data_config.get("timestamp_column") or columns["timestamp"]
    if not timestamp_column:
        raise ValueError("Mobility input requires a timestamp column")
    validated = validate_mobility_records(source)
    profiled = profile_mobility(validated)
    featured = create_mobility_features(validated, timestamp_column)
    featured = add_travel_speed_flag(featured)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}_mobility_features.csv"
    featured.to_csv(output_path, index=False)

    result: dict[str, Any] = {
        "dataset": input_path.name,
        "feature_version": MOBILITY_FEATURE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_rows": int(len(source)),
        "valid_rows": int((validated["quality_flag"] == "valid").sum()),
        "invalid_rows": int((validated["quality_flag"] == "invalid").sum()),
        "output_path": str(output_path),
        "profile": profiled,
        "od_status": "NOT AVAILABLE IN DATASET",
        "graph_status": "NOT AVAILABLE IN DATASET",
    }

    origin = data_config.get("origin_column") or columns["origin"]
    destination = data_config.get("destination_column") or columns["destination"]
    demand = data_config.get("demand_column") or columns["demand"]
    if origin and destination:
        od, zone_flow = build_od_matrix(
            validated,
            timestamp_column,
            origin,
            destination,
            demand,
            str(data_config.get("frequency", "h")),
        )
        od_dir = report_dir / "mobility"
        od_dir.mkdir(parents=True, exist_ok=True)
        od.to_csv(od_dir / "od_flows.csv", index=False)
        zone_flow.to_csv(od_dir / "zone_flows.csv", index=False)
        graph = build_mobility_graph(od)
        graph_metrics(graph).to_csv(od_dir / "graph_metrics.csv", index=False)
        _write_json(od_dir / "graph_statistics.json", graph_statistics(graph))
        anomaly_input = zone_flow.sort_values(["zone_id", "time_bucket"])
        anomaly_input = add_demand_anomaly_flags(anomaly_input, "inflow", "zone_id")
        anomaly_input.to_csv(od_dir / "zone_anomalies.csv", index=False)
        result["od_status"] = "measured"
        result["graph_status"] = "measured"
        result["od_rows"] = int(len(od))
        result["graph_nodes"] = int(graph.number_of_nodes())
        result["graph_edges"] = int(graph.number_of_edges())

    report_dir.mkdir(parents=True, exist_ok=True)
    _write_json(report_dir / "mobility" / "profile.json", profiled)
    _write_json(report_dir / "mobility" / "pipeline_report.json", result)
    return result


def run_pipeline(input_dir: Path, output_dir: Path, report_dir: Path, config_path: Path, stage: str) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    input_files = sorted(input_dir.glob("*.csv")) if input_dir.exists() else []
    reports = []
    if stage in {"profile", "features", "od", "graph", "all"}:
        reports = [process_mobility_csv(path, output_dir, report_dir, config) for path in input_files]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "datasets_discovered": len(input_files),
        "datasets_processed": len(reports),
        "reports": reports,
        "forecast_status": "NOT MEASURED",
        "database_status": "NOT IMPLEMENTED IN THIS PHASE SLICE",
    }
    _write_json(report_dir / "mobility" / "pipeline_summary.json", summary)
    logger.info("Mobility pipeline complete: stage=%s datasets=%s", stage, len(reports))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile and aggregate real mobility data.")
    parser.add_argument("--stage", choices=["profile", "features", "od", "graph", "train", "anomaly", "evaluate", "all"], default="all")
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed/mobility"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/mobility_ml_ready"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--config", type=Path, default=Path("config/mobility.yaml"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    if args.stage in {"train", "evaluate"}:
        logger.warning("Mobility forecasting is NOT MEASURED because no real dataset is available")
    run_pipeline(args.input_dir, args.output_dir, args.report_dir, args.config, args.stage)


if __name__ == "__main__":
    main()
