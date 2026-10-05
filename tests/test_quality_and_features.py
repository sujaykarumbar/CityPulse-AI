import pandas as pd

from citypulse.features.leakage import find_leakage_risks
from citypulse.pipelines.features import run_pipeline
from citypulse.features.temporal import create_temporal_features
from citypulse.features.traffic import create_lag_and_rolling_features
from citypulse.quality.cleaning import clean_dataframe
from citypulse.quality.profiling import profile_dataframe
from citypulse.quality.outliers import add_outlier_flags
from citypulse.quality.validation import validate_dataframe


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Timestamp": ["2025-01-01T00:00:00Z", "2025-01-01T01:00:00Z", "2025-01-01T02:00:00Z"],
            "Latitude": [40.7, 40.7, 95.0],
            "Longitude": [-74.0, -74.0, -74.0],
            "road_id": ["r1", "r1", "r1"],
            "vehicle_count": [10, 20, 30],
        }
    )


def test_profile_and_validation_measure_real_rows() -> None:
    frame = sample_frame()
    profile = profile_dataframe(frame)
    validation = validate_dataframe(frame)

    assert profile["rows"] == 3
    assert profile["duplicate_rows"] == 0
    assert validation["valid_rows"] == 2
    assert validation["rejected_rows"] == 1


def test_cleaning_normalizes_columns_and_rejects_invalid_coordinates() -> None:
    cleaned, stats = clean_dataframe(sample_frame())

    assert list(cleaned.columns)[0] == "timestamp"
    assert len(cleaned) == 2
    assert stats["rejected_rows"] == 1


def test_validation_rejects_malformed_numeric_values() -> None:
    frame = pd.DataFrame({"latitude": [40.7, "not-a-number"], "longitude": [-74.0, -74.0]})

    assert validate_dataframe(frame)["valid_rows"] == 1


def test_temporal_features_and_past_only_lag() -> None:
    frame, _ = clean_dataframe(sample_frame())
    frame = create_temporal_features(frame)
    frame = create_lag_and_rolling_features(frame, ["vehicle_count"], [1], [2])

    assert frame.loc[frame.index[0], "hour_sin"] == 0
    assert pd.isna(frame.iloc[0]["vehicle_count_lag_1"])
    assert frame.iloc[1]["vehicle_count_lag_1"] == 10
    assert pd.isna(frame.iloc[0]["vehicle_count_rolling_mean_2"])


def test_leakage_checker_reports_unsorted_timestamps() -> None:
    frame = pd.DataFrame({"timestamp": ["2025-01-02", "2025-01-01"], "target_future": [1, 2]})

    risks = find_leakage_risks(frame, target_column="target")

    assert any(risk["column"] == "timestamp" for risk in risks)
    assert any(risk["column"] == "target_future" for risk in risks)


def test_outlier_flags_do_not_remove_rows() -> None:
    frame = pd.DataFrame({"vehicle_count": [1, 2, 3, 100]})

    flagged = add_outlier_flags(frame, ["vehicle_count"])

    assert len(flagged) == len(frame)
    assert "vehicle_count_outlier_iqr" in flagged


def test_pipeline_writes_features_and_reports(tmp_path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "ml_ready"
    report_dir = tmp_path / "reports"
    input_dir.mkdir()
    (tmp_path / "features.yaml").write_text(
        "lag_windows: [1]\nrolling_windows: [2]\ntarget_columns: [vehicle_count]\n",
        encoding="utf-8",
    )
    sample_frame().iloc[:2].to_csv(input_dir / "traffic.csv", index=False)

    summary = run_pipeline(input_dir, output_dir, report_dir, tmp_path / "features.yaml")

    assert summary["datasets_processed"] == 1
    assert (output_dir / "traffic_features.csv").exists()
    assert (report_dir / "data_quality" / "traffic_quality.json").exists()
    assert (report_dir / "feature_reports" / "traffic_features.json").exists()
