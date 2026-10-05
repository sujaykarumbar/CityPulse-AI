from citypulse.adaptive.assumptions import check_assumption
from citypulse.adaptive.change_detection import detect_change
from citypulse.adaptive.engine import AdaptiveUrbanIntelligenceEngine
from citypulse.adaptive.state import UrbanStrategyState
from citypulse.adaptive.strategy import StrategyLifecycle, compute_strategy_health, generate_alternatives


def test_strategy_state_tracks_status() -> None:
    strategy = UrbanStrategyState(
        strategy_id="s-1",
        city_id="city-a",
        version="v1",
        status="ACTIVE",
        objectives=["mobility"],
        policies=["transit_investment"],
    )

    assert strategy.status == "ACTIVE"
    assert strategy.version == "v1"


def test_assumption_check_detects_drift() -> None:
    result = check_assumption(
        assumption_id="pop-growth",
        description="population growth remains within 2-4%",
        variable="population_growth",
        expected_range=(2.0, 4.0),
        observed_value=5.2,
    )

    assert result["status"] == "DRIFTING"
    assert result["triggered"] is True


def test_change_detection_identifies_regime_shift() -> None:
    event = detect_change(
        metric_name="transit_ridership",
        previous_value=60.0,
        current_value=90.0,
        threshold=20.0,
    )

    assert event["change_type"] == "REGIME_SHIFT"
    assert event["status"] == "MODEL_DERIVED"


def test_strategy_lifecycle_updates_state() -> None:
    lifecycle = StrategyLifecycle()
    state = lifecycle.advance("ACTIVE", "review")

    assert state == "REVIEW_REQUIRED"


def test_adaptive_engine_and_strategy_health_are_consistent() -> None:
    engine = AdaptiveUrbanIntelligenceEngine()
    result = engine.monitor_strategy(
        city_id="city-a",
        strategy_id="s-1",
        observed_metrics={"performance": 0.6, "robustness": 0.7, "assumption_validity": 0.5},
        expected_metrics={"performance": 0.8, "robustness": 0.8, "assumption_validity": 0.8},
    )

    assert result["status"] == "REVIEW_REQUIRED"
    health = compute_strategy_health({"performance": 0.6, "robustness": 0.7, "assumption_validity": 0.5})
    assert health["overall_status"] in {"DEGRADING", "REVIEW_REQUIRED"}
    alternatives = generate_alternatives("s-1", ["continue", "modify", "scale_up"])
    assert len(alternatives) >= 2
