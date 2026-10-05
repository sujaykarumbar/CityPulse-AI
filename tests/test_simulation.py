import pytest

from citypulse.simulation.scenario_engine import run_scenario
from citypulse.simulation.scenario_validator import ScenarioValidationError
from citypulse.simulation.schemas import Scenario, ScenarioChange, UrbanState


def baseline() -> UrbanState:
    return UrbanState(
        traffic_state={"volume": 100.0, "average_speed": 40.0},
        energy_state={"demand": 200.0},
        graph_state={"segment_ids": ["SEG001"], "edges": [{"segment_id": "SEG001", "active": True}]},
    )


def test_demand_transformation_and_delta() -> None:
    scenario = Scenario(
        scenario_id="traffic_30",
        name="traffic increase",
        changes=[ScenarioChange(type="traffic_demand_change", parameters={"multiplier": 1.3})],
    )

    result = run_scenario(scenario, baseline())

    assert result.status == "completed"
    assert result.scenario.traffic_state["volume"] == 130.0
    assert result.baseline.traffic_state["volume"] == 100.0
    assert any(delta.metric == "traffic.volume" and delta.absolute_delta == 30 for delta in result.deltas)


def test_road_closure_does_not_mutate_baseline() -> None:
    scenario = Scenario(
        scenario_id="closure",
        name="closure",
        changes=[ScenarioChange(type="road_closure", parameters={"segment_ids": ["SEG001"]})],
    )

    result = run_scenario(scenario, baseline())

    assert result.scenario.graph_state["edges"][0]["active"] is False
    assert result.baseline.graph_state["edges"][0]["active"] is True
    assert result.affected_regions == ["SEG001"]


def test_unknown_segment_is_rejected() -> None:
    scenario = Scenario(
        scenario_id="invalid",
        name="invalid",
        changes=[ScenarioChange(type="road_closure", parameters={"segment_ids": ["UNKNOWN"]})],
    )

    with pytest.raises(ScenarioValidationError):
        run_scenario(scenario, baseline())
