from fastapi.testclient import TestClient

from citypulse.economic.data_contracts import EconomicObservation
from citypulse.economic.profiles import build_city_economic_profile
from citypulse.economic.specialization import analyze_specialization
from citypulse.economic.shocks import simulate_economic_shock
from citypulse.main import app


def test_economic_observation_and_profile_are_valid() -> None:
    observation = EconomicObservation(
        geography="city-a",
        time="2025-Q1",
        sector="manufacturing",
        indicator="employment",
        value=1200.0,
        unit="jobs",
        source="synthetic",
        confidence=0.7,
        provenance={"source_type": "synthetic"},
    )

    profile = build_city_economic_profile(
        city_id="city-a",
        profile={
            "employment": 1200.0,
            "industry_mix": {"manufacturing": 0.5, "retail": 0.3},
            "economic_diversity": 0.7,
        },
    )

    assert observation.indicator == "employment"
    assert profile["city_id"] == "city-a"
    assert profile["status"] == "MODEL_DERIVED"


def test_specialization_analysis_reports_sector_signal() -> None:
    signal = analyze_specialization(
        city_id="city-a",
        sector="manufacturing",
        share=0.6,
        reference_share=0.3,
        period="2025-Q1",
    )

    assert signal["city_id"] == "city-a"
    assert signal["sector"] == "manufacturing"
    assert signal["value"] > 0


def test_economic_shock_simulation_is_labeled_and_bounded() -> None:
    result = simulate_economic_shock(
        city_id="city-a",
        shock_type="freight_disruption",
        magnitude=0.6,
        sectors=["manufacturing"],
        duration_days=14,
    )

    assert result["city_id"] == "city-a"
    assert result["status"] == "SIMULATED"
    assert result["magnitude"] == 0.6


def test_economic_api_exists() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/economy/cities/city-a")
    assert response.status_code == 200
    payload = response.json()
    assert payload["city_id"] == "city-a"
    assert payload["status"] == "MODEL_DERIVED"
