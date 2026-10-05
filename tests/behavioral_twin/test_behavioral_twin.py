from citypulse.behavior.demand import demand_response
from citypulse.behavior.feedback import feedback_loop
from citypulse.behavior.mode_choice import mode_choice_probability
from citypulse.behavior.state import BehaviorState, UrbanSystemState


def test_urban_system_state_tracks_components() -> None:
    state = UrbanSystemState(
        timestamp="2024-01-01T00:00:00Z",
        geography="zone-a",
        population={"count": 1000},
        mobility={"transit_ridership": 120},
        traffic={"volume": 250},
        energy={"demand": 80},
        infrastructure={"roads": 14},
        environment={"weather": "clear"},
        risk={"incident_risk": 0.1},
        policy={"pricing": "none"},
        economic_context={"gdp_growth": 0.02},
        technology_adoption={"ev_share": 0.12},
    )

    assert state.geography == "zone-a"
    assert state.traffic["volume"] == 250


def test_behavior_state_supports_mode_choice_data() -> None:
    behavior = BehaviorState(
        mode_choice={"car": 0.4, "bus": 0.3, "walk": 0.3},
        route_choice={"route-a": 0.6, "route-b": 0.4},
        departure_time={"peak": 0.5, "off_peak": 0.5},
        trip_frequency={"daily": 1.0},
        vehicle_usage={"car_trips": 0.4},
        transit_usage={"bus_trips": 0.3},
    )

    assert behavior.mode_choice["bus"] == 0.3


def test_mode_choice_probability_normalizes() -> None:
    probs = mode_choice_probability({"car": 2.0, "bus": 1.0, "walk": 1.0})

    assert abs(sum(probs.values()) - 1.0) < 1e-9
    assert probs["car"] > probs["bus"]


def test_demand_response_returns_modeled_response() -> None:
    outcome = demand_response(policy_change={"fare": 1.5}, baseline_demand={"transit": 100}, elasticity={"transit": -0.2})

    assert outcome["status"] == "SIMULATED"
    assert outcome["transit"]["delta"] < 0


def test_feedback_loop_detects_reinforcing_pattern() -> None:
    loop = feedback_loop("road_congestion", "mode_shift", "travel_time", "road_congestion")

    assert loop["loop_type"] == "reinforcing"
    assert loop["status"] == "GRAPHED"
