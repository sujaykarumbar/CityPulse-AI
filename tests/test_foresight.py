from citypulse.foresight.engine import UrbanEvolutionEngine, generate_future_scenarios
from citypulse.foresight.pathways import AdaptivePathwayEngine, evaluate_trigger
from citypulse.foresight.robustness import regret_analysis, robustness_analysis


def test_generate_future_scenarios_creates_valid_futures() -> None:
    scenarios = generate_future_scenarios(
        city_id="alpha-city",
        horizon_years=10,
        seed=123,
        policy_assumptions={"transit_investment": 1.15},
    )

    assert len(scenarios) >= 3
    assert scenarios[0].scenario_id
    assert scenarios[0].horizon_years == 10
    assert scenarios[0].provenance["status"] == "SCENARIO_ESTIMATE"


def test_urban_evolution_engine_simulates_future_state() -> None:
    engine = UrbanEvolutionEngine(seed=7)
    result = engine.simulate_future(
        baseline={"population": 100000, "mobility": 1.0, "energy": 0.9},
        policy={"transit_investment": 1.1},
        horizon_years=5,
    )

    assert result["status"] == "SCENARIO_ESTIMATE"
    assert len(result["states"]) >= 2
    assert result["states"][-1]["population"] >= result["states"][0]["population"]


def test_evaluate_trigger_identifies_pathway_transition() -> None:
    signal = evaluate_trigger(
        metric_name="transit_ridership",
        current_value=85,
        threshold=80,
        direction="above",
    )

    assert signal["triggered"] is True
    assert signal["signal"] == "TRANSIT_EXPANSION_REVIEW"


def test_pathway_engine_generates_adaptive_strategy() -> None:
    engine = AdaptivePathwayEngine()
    pathway = engine.build_pathway(
        initial_strategy="Transit investment",
        monitors=["transit_ridership", "traffic_volume"],
        thresholds={"transit_ridership": 80, "traffic_volume": 120},
        alternative_strategy="Demand management",
    )

    assert pathway["initial_strategy"] == "Transit investment"
    assert pathway["next_action"] == "MONITOR"
    assert len(pathway["monitoring"]) == 2


def test_robustness_and_regret_metrics_are_numeric() -> None:
    robustness = robustness_analysis(strategy_scores={"A": 0.8, "B": 0.7, "C": 0.6})
    regret = regret_analysis(strategy_scores={"A": 0.8, "B": 0.7, "C": 0.6}, best_score=0.9)

    assert robustness["status"] == "MODEL_DERIVED"
    assert regret["regret_total"] >= 0.0
    assert regret["strategy_regret"]["A"] >= 0.0
