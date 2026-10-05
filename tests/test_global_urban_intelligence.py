from citypulse.global_city.registry import CityRegistry
from citypulse.global_city.similarity import city_similarity
from citypulse.knowledge_graph.graph import KnowledgeGraph
from citypulse.transfer.learning import negative_transfer_status, transfer_experiment


def test_city_registry_tracks_city_and_domain_availability() -> None:
    registry = CityRegistry()
    city = registry.register_city(
        "city-a",
        {
            "city_name": "City A",
            "country": "Country X",
            "timezone": "UTC",
            "domains": {"traffic": True, "mobility": True, "energy": False},
        },
    )

    assert city["city_id"] == "city-a"
    assert city["domains"]["traffic"] is True
    assert city["domains"]["energy"] is False


def test_city_similarity_uses_measured_features_only() -> None:
    result = city_similarity({"traffic": 10.0, "mobility": 8.0}, {"traffic": 12.0, "mobility": 9.0})

    assert result["status"] == "MEASURED"
    assert 0.0 < result["score"] <= 1.0


def test_negative_transfer_is_detected_when_transfer_underperforms_local_baseline() -> None:
    status = negative_transfer_status(local_mae=2.0, transferred_mae=3.0)

    assert status == "NEGATIVE_TRANSFER"


def test_transfer_experiment_handles_missing_ground_truth() -> None:
    result = transfer_experiment("city-a", "city-b", {"local_mae": 1.0}, {})

    assert result["status"] == "TRANSFER_NOT_EVALUATED"
    assert result["ground_truth_status"] == "GROUND_TRUTH_NOT_AVAILABLE"


def test_knowledge_graph_tracks_provenance() -> None:
    graph = KnowledgeGraph()
    edge = graph.add_relationship("city-a", "traffic-pattern", "HAS_PATTERN", "city-b", provenance={"source": "observed", "confidence": 0.8})

    assert edge["provenance"]["source"] == "observed"
    assert edge["relationship"] == "HAS_PATTERN"
