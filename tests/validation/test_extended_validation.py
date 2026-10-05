import networkx as nx
import pandas as pd
import pytest

from citypulse.validation.datasets.spatial_split import spatial_frame_holdout
from citypulse.validation.datasets.temporal_split import chronological_frame_split
from citypulse.validation.robustness.distribution_shift import shift_numeric_distribution
from citypulse.validation.robustness.graph_perturbation import remove_edges
from citypulse.validation.robustness.modality_dropout import drop_modalities
from citypulse.validation.simulation_validation.calibration import grid_search_calibration
from citypulse.validation.synthetic.comparison import compare_real_synthetic
from citypulse.validation.synthetic.energy_generator import generate_energy
from citypulse.validation.synthetic.graph_generator import generate_synthetic_graph
from citypulse.validation.synthetic.mobility_generator import generate_mobility
from citypulse.validation.synthetic.quality import synthetic_quality_report
from citypulse.validation.uncertainty.monte_carlo import run_monte_carlo


def test_temporal_frame_split_orders_rows_and_keeps_tied_timestamps_together() -> None:
    frame = pd.DataFrame({"time": ["2025-01-04", "2025-01-01", "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-05"], "value": range(6)})

    split = chronological_frame_split(frame, "time", train_fraction=0.5, validation_fraction=0.25)

    assert split.train["time"].max() < split.validation["time"].min()
    assert split.validation["time"].max() < split.test["time"].min()
    assert len(split.train[split.train["time"] == "2025-01-01"]) == 2
    assert split.metadata["status"] == "SPLIT_CREATED"


def test_temporal_frame_split_rejects_unparseable_timestamps() -> None:
    with pytest.raises(ValueError, match="INVALID_OR_MISSING_TIMESTAMP"):
        chronological_frame_split(pd.DataFrame({"time": ["not-a-time"]}), "time")


def test_spatial_frame_holdout_has_disjoint_reproducible_entities() -> None:
    frame = pd.DataFrame({"zone": ["a", "a", "b", "b", "c", "c", "d", "d"], "value": range(8)})

    first = spatial_frame_holdout(frame, "zone", holdout_fraction=0.25, seed=12)
    second = spatial_frame_holdout(frame, "zone", holdout_fraction=0.25, seed=12)

    assert set(first.train["zone"]).isdisjoint(first.test["zone"])
    assert first.metadata["test_entities"] == second.metadata["test_entities"]
    assert len(first.test) == 2


def test_other_generators_mark_synthetic_and_quality_checks() -> None:
    energy = generate_energy({"sample_count": 8, "seed": 9})
    mobility = generate_mobility({"sample_count": 8, "zones": ["z1", "z2"], "seed": 9})
    assert set(energy["data_origin"]) == {"SYNTHETIC"}
    assert set(mobility["data_origin"]) == {"SYNTHETIC"}
    assert synthetic_quality_report(energy)["status"] == "MEASURED"


def test_modality_dropout_marks_absence() -> None:
    result = drop_modalities({"traffic": [1, 2], "weather": [3]}, ["weather"])

    assert "weather" not in result
    assert result["modality_available"]["weather"] is False


def test_distribution_shift_is_explicitly_synthetic() -> None:
    values, metadata = shift_numeric_distribution([1, 2], additive_shift=5)

    assert values == [6.0, 7.0]
    assert metadata["data_origin"] == "SYNTHETIC_ROBUSTNESS_TEST"


def test_graph_perturbation_is_seeded_and_does_not_mutate_source() -> None:
    graph = nx.path_graph(10)
    perturbed, metadata = remove_edges(graph, 0.3, seed=2)

    assert graph.number_of_edges() == 9
    assert perturbed.number_of_edges() == 7
    assert metadata["data_origin"] == "SYNTHETIC_ROBUSTNESS_TEST"


def test_grid_calibration_uses_only_measured_observed_values() -> None:
    result = grid_search_calibration([2.0, 4.0], {"offset": [0.0, 1.0]}, lambda params: [2.0 + params["offset"], 4.0 + params["offset"]])

    assert result["status"] == "MEASURED"
    assert result["best_candidate"]["parameters"]["offset"] == 0.0
    assert result["identifiability"] == "IDENTIFIABILITY_NOT_ESTABLISHED"


def test_calibration_rejects_unbounded_grid() -> None:
    with pytest.raises(ValueError, match="RESOURCE_LIMIT_EXCEEDED"):
        grid_search_calibration([1.0], {"p": list(map(float, range(10)))}, lambda _: [1.0], max_evaluations=5)


def test_monte_carlo_is_seeded_and_labeled_simulated() -> None:
    distributions = {"demand": {"distribution": "uniform", "low": 1.0, "high": 3.0}}
    simulator = lambda parameters: parameters["demand"] * 2

    first = run_monte_carlo(simulator, distributions, sample_count=20, seed=13)
    second = run_monte_carlo(simulator, distributions, sample_count=20, seed=13)

    assert first == second
    assert first["result_type"] == "SIMULATED"
    assert first["random_seed"] == 13
    assert len(first["output_samples"][0]) == 20


def test_monte_carlo_enforces_sample_limit() -> None:
    with pytest.raises(ValueError, match="RESOURCE_LIMIT_EXCEEDED"):
        run_monte_carlo(lambda _: 1.0, {"p": {"distribution": "uniform", "low": 0.0, "high": 1.0}}, sample_count=5_001)


def test_synthetic_real_comparison_requires_real_reference() -> None:
    assert compare_real_synthetic([], [1, 2])["status"] == "VALIDATION_NOT_AVAILABLE"
