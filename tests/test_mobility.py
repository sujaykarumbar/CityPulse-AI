import pandas as pd

from citypulse.mobility.anomaly import add_demand_anomaly_flags
from citypulse.mobility.features import create_mobility_features
from citypulse.mobility.graph import build_mobility_graph, graph_statistics
from citypulse.mobility.od import build_od_matrix
from citypulse.mobility.profile import profile_mobility, validate_mobility_records
from citypulse.pipelines.mobility import run_pipeline


def mobility_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2025-01-01", periods=4, freq="h", tz="UTC"),
            "origin_zone": ["a", "a", "b", "b"],
            "destination_zone": ["b", "b", "a", "a"],
            "trip_count": [2, 3, 4, 5],
            "duration": [0.5, 0.6, 0.7, 0.8],
            "distance": [5, 6, 7, 8],
        }
    )


def test_profile_and_validation() -> None:
    frame = mobility_frame()
    profile = profile_mobility(frame)
    validated = validate_mobility_records(frame)

    assert profile["origin_count"] == 2
    assert profile["unique_od_pairs"] == 2
    assert (validated["quality_flag"] == "valid").all()


def test_temporal_features_are_created() -> None:
    featured = create_mobility_features(mobility_frame())

    assert featured.loc[0, "hour"] == 0
    assert "hour_sin" in featured
    assert "is_weekend" in featured


def test_od_flow_and_zone_balance() -> None:
    od, zone_flow = build_od_matrix(
        mobility_frame(), "timestamp", "origin_zone", "destination_zone", "trip_count", "h"
    )

    assert od["trip_count"].sum() == 14
    assert set(zone_flow["zone_id"]) == {"a", "b"}
    assert "net_flow" in zone_flow


def test_mobility_graph_preserves_direction() -> None:
    od, _ = build_od_matrix(
        mobility_frame(), "timestamp", "origin_zone", "destination_zone", "trip_count", "h"
    )
    graph = build_mobility_graph(od)

    assert graph.is_directed()
    assert graph_statistics(graph)["nodes"] == 2
    assert graph_statistics(graph)["edges"] == 2


def test_anomaly_flags_use_past_values() -> None:
    values = pd.DataFrame({"zone_id": ["a"] * 5, "inflow": [1, 1, 1, 1, 100]})

    result = add_demand_anomaly_flags(values, "inflow", "zone_id", window=3, threshold=2)

    assert not bool(result.iloc[0]["anomaly_flag"])
    assert bool(result.iloc[-1]["anomaly_flag"])


def test_pipeline_generates_aggregated_outputs(tmp_path) -> None:
    input_dir = tmp_path / "mobility"
    input_dir.mkdir()
    (tmp_path / "mobility.yaml").write_text(
        "data:\n  frequency: h\n  origin_column: origin_zone\n  destination_column: destination_zone\n  demand_column: trip_count\nanomaly:\n  window: 2\n  zscore_threshold: 2\n",
        encoding="utf-8",
    )
    mobility_frame().to_csv(input_dir / "trips.csv", index=False)

    summary = run_pipeline(input_dir, tmp_path / "output", tmp_path / "reports", tmp_path / "mobility.yaml", "all")

    assert summary["datasets_processed"] == 1
    assert (tmp_path / "reports" / "mobility" / "od_flows.csv").exists()
    assert (tmp_path / "reports" / "mobility" / "graph_statistics.json").exists()
