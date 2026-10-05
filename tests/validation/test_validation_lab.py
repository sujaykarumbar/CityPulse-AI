import numpy as np
import pandas as pd
import pytest

from citypulse.validation.backtesting.walk_forward import walk_forward_splits
from citypulse.validation.benchmarking.metrics import regression_metrics
from citypulse.validation.robustness.missing_data import apply_missingness
from citypulse.validation.robustness.noise import add_gaussian_noise
from citypulse.validation.simulation_validation.observed_vs_simulated import compare_observed_simulated
from citypulse.validation.synthetic.traffic_generator import generate_traffic


def test_walk_forward_splits_are_ordered_and_disjoint() -> None:
    splits = walk_forward_splits(20, initial_train_size=10, validation_size=3, step_size=3)

    assert splits
    for train, validation in splits:
        assert max(train) < min(validation)
        assert len(set(train) & set(validation)) == 0


def test_regression_metrics_are_computed_from_values() -> None:
    result = regression_metrics([1.0, 2.0, 3.0], [1.0, 3.0, 2.0])

    assert result["status"] == "MEASURED"
    assert result["MAE"] == pytest.approx(2 / 3)
    assert result["RMSE"] == pytest.approx(np.sqrt(2 / 3))


def test_metrics_do_not_claim_when_truth_missing() -> None:
    assert regression_metrics([], []) == {"status": "GROUND_TRUTH_NOT_AVAILABLE"}


def test_undefined_metrics_are_not_reported_as_nan() -> None:
    result = regression_metrics([0.0, 0.0], [0.0, 1.0])

    assert result["WAPE"] == "NOT_MEASURED"
    assert result["R2"] == "NOT_MEASURED"


def test_synthetic_traffic_is_labeled_and_seeded() -> None:
    config = {"sample_count": 24, "seed": 17, "base_volume": 100.0, "peak_multiplier": 1.5, "noise_std": 0.0}
    first = generate_traffic(config)
    second = generate_traffic(config)

    assert first.equals(second)
    assert set(first["data_origin"]) == {"SYNTHETIC"}
    assert first["generator_version"].nunique() == 1


def test_synthetic_sample_limit_is_enforced() -> None:
    with pytest.raises(ValueError, match="RESOURCE_LIMIT_EXCEEDED"):
        generate_traffic({"sample_count": 100_001, "seed": 1})


def test_missingness_and_noise_are_reproducible_and_non_destructive() -> None:
    frame = pd.DataFrame({"speed": np.arange(100, dtype=float)})
    dropped = apply_missingness(frame, rate=0.2, seed=5)
    noisy = add_gaussian_noise(frame, columns=["speed"], std=0.5, seed=5)

    assert dropped["speed"].isna().sum() == 20
    assert frame["speed"].isna().sum() == 0
    pd.testing.assert_frame_equal(noisy, add_gaussian_noise(frame, ["speed"], 0.5, 5))


def test_simulation_comparison_reports_measured_residuals() -> None:
    result = compare_observed_simulated([10, 12, 14], [9, 13, 14])

    assert result["result_type"] == "SIMULATED"
    assert result["metrics"]["MAE"] == pytest.approx(2 / 3)
    assert result["residuals"] == [1.0, -1.0, 0.0]
