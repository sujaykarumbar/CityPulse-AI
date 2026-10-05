from fastapi.testclient import TestClient

from citypulse.environment.data_contracts import WeatherObservation
from citypulse.environment.weather import analyze_weather_extremes
from citypulse.environment.climate import compute_climate_baseline
from citypulse.main import app


def test_weather_observation_and_extreme_analysis() -> None:
    obs = WeatherObservation(
        timestamp="2025-05-01T12:00:00Z",
        geometry="city-a",
        variable="temperature",
        value=32.5,
        unit="C",
        source="synthetic",
        quality=0.75,
        confidence=0.7,
        provenance={"source_type": "synthetic"},
    )

    result = analyze_weather_extremes(
        city_id="city-a",
        temperatures=[28.0, 30.0, 32.5, 34.0],
        threshold=31.0,
    )

    assert obs.variable == "temperature"
    assert result["city_id"] == "city-a"
    assert result["status"] == "MODEL_DERIVED"


def test_climate_baseline_is_labeled_and_reproducible() -> None:
    baseline = compute_climate_baseline(
        city_id="city-a",
        values=[22.0, 23.0, 24.0, 23.5],
        period="2024",
    )

    assert baseline["city_id"] == "city-a"
    assert baseline["status"] == "MODEL_DERIVED"
    assert baseline["period"] == "2024"


def test_environment_api_exists() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/environment/cities/city-a")
    assert response.status_code == 200
    payload = response.json()
    assert payload["city_id"] == "city-a"
    assert payload["status"] == "MODEL_DERIVED"
