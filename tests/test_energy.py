import pandas as pd

from citypulse.energy.anomaly import add_rolling_zscore_flags
from citypulse.energy.features import add_peak_features, create_energy_features
from citypulse.energy.profile import detect_frequency, profile_energy
from citypulse.pipelines.energy import run_pipeline


def energy_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2025-01-01", periods=12, freq="h", tz="UTC"),
            "entity_id": ["zone-a"] * 12,
            "demand": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 100],
        }
    )


def test_profile_detects_hourly_series_and_target() -> None:
    frame = energy_frame()
    profile = profile_energy(frame)

    assert profile["target"] == "demand"
    assert profile["entity_count"] == 1
    assert profile["frequency"]["median_interval_seconds"] == 3600


def test_energy_features_are_past_only() -> None:
    featured = create_energy_features(energy_frame(), "demand", entity_column="entity_id", lags=[1], rolling_windows=[3])

    assert pd.isna(featured.iloc[0]["demand_lag_1"])
    assert featured.iloc[1]["demand_lag_1"] == 10
    assert pd.isna(featured.iloc[0]["demand_rolling_mean_3"])
    assert featured.iloc[1]["demand_rolling_mean_3"] == 10


def test_peak_and_anomaly_flags_are_measured() -> None:
    featured = add_peak_features(energy_frame(), "demand", quantile=0.9)
    flagged = add_rolling_zscore_flags(featured, "demand", window=3, threshold=2)

    assert int(featured["peak_flag"].sum()) >= 1
    assert "anomaly_score" in flagged
    assert "anomaly_flag" in flagged


def test_pipeline_writes_energy_reports(tmp_path) -> None:
    input_dir = tmp_path / "energy"
    input_dir.mkdir()
    (tmp_path / "energy.yaml").write_text(
        "data:\n  target: demand\n  entity_column: entity_id\n  lags: [1]\n  rolling_windows: [3]\npeak_detection:\n  quantile: 0.9\nanomaly:\n  rolling_window: 3\n  zscore_threshold: 2\nforecast:\n  seasonal_lag: 3\n",
        encoding="utf-8",
    )
    energy_frame().to_csv(input_dir / "energy.csv", index=False)

    summary = run_pipeline(input_dir, tmp_path / "output", tmp_path / "reports", tmp_path / "energy.yaml")

    assert summary["datasets_processed"] == 1
    assert (tmp_path / "output" / "energy_energy_features.csv").exists()
    assert (tmp_path / "reports" / "energy" / "profile.json").exists()
    assert (tmp_path / "reports" / "energy" / "model_comparison.csv").exists()
