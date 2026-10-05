from citypulse.policy.evidence import EvidenceProfile
from citypulse.policy.experiments import PolicyExperimentEngine
from citypulse.policy.registry import PolicyRegistry


def test_policy_registry_tracks_policy_version_and_metadata() -> None:
    registry = PolicyRegistry()
    policy = registry.register(
        policy_id="congestion_pricing",
        name="Congestion Pricing",
        category="transportation",
        version="1.2",
        city_scope="global",
        status="experimental",
        provenance={"source": "synthetic_registry"},
    )

    assert policy["policy_id"] == "congestion_pricing"
    assert policy["version"] == "1.2"
    assert policy["city_scope"] == "global"


def test_policy_experiment_requires_supported_evidence() -> None:
    engine = PolicyExperimentEngine()
    result = engine.evaluate(
        policy_id="congestion_pricing",
        city_id="city-a",
        baseline={"travel_time": 40.0},
        simulation={"travel_time": 35.0},
        evidence={"causal": {"status": "NOT_AVAILABLE"}},
        objectives=[{"metric": "travel_time", "direction": "minimize", "weight": 1.0}],
    )

    assert result["status"] == "REVIEW_REQUIRED"
    assert result["evidence_status"] == "INSUFFICIENT_DATA"


def test_evidence_profile_keeps_sources_separate() -> None:
    profile = EvidenceProfile(
        causal={"status": "NOT_AVAILABLE"},
        simulation={"status": "SIMULATED", "travel_time_delta": -5.0},
        predictive={"status": "NOT_RUN"},
    )

    assert profile.causal["status"] == "NOT_AVAILABLE"
    assert profile.simulation["travel_time_delta"] == -5.0
    assert profile.predictive["status"] == "NOT_RUN"


def test_policy_engine_reports_transferability_unknown_when_insufficient_data() -> None:
    engine = PolicyExperimentEngine()
    result = engine.transferability(source_city="city-a", target_city="city-b", overlap={})

    assert result["status"] == "UNKNOWN"
    assert result["evidence"] == "INSUFFICIENT_DATA"


def test_policy_engine_reports_robustness_when_no_stress_scenario_exists() -> None:
    engine = PolicyExperimentEngine()
    report = engine.robustness(policy_id="congestion_pricing", scenarios=[])

    assert report["status"] == "NOT_RUN"
    assert report["reason"] == "No stress scenarios were supplied."
