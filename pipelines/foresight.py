from __future__ import annotations

import argparse
from pathlib import Path

from citypulse.foresight.engine import UrbanEvolutionEngine, generate_future_scenarios
from citypulse.foresight.pathways import AdaptivePathwayEngine
from citypulse.foresight.robustness import regret_analysis, robustness_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic urban future scenarios and adaptive strategy pathways.")
    parser.add_argument("--city-id", default="demo-city")
    parser.add_argument("--horizon-years", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--scenario-count", type=int, default=3)
    parser.add_argument("--mode", choices=["scenarios", "evolution", "pathway", "robustness", "regret"], default="scenarios")
    args = parser.parse_args()

    if args.mode == "scenarios":
        result = generate_future_scenarios(
            city_id=args.city_id,
            horizon_years=args.horizon_years,
            seed=args.seed,
            scenario_count=args.scenario_count,
        )
        print({"status": "SCENARIO_ESTIMATE", "scenarios": [item.model_dump() for item in result]})
        return

    if args.mode == "evolution":
        result = UrbanEvolutionEngine(seed=args.seed).simulate_future(
            baseline={"population": 100000, "mobility": 1.0, "energy": 0.9},
            policy={"transit_investment": 1.2, "ev_adoption": 0.4},
            horizon_years=args.horizon_years,
        )
        print(result)
        return

    if args.mode == "pathway":
        result = AdaptivePathwayEngine().build_pathway(
            initial_strategy="Transit investment",
            monitors=["transit_ridership", "traffic_volume"],
            thresholds={"transit_ridership": 80, "traffic_volume": 120},
            alternative_strategy="Demand management",
        )
        print(result)
        return

    if args.mode == "robustness":
        print(robustness_analysis(strategy_scores={"A": 0.8, "B": 0.7, "C": 0.6}))
        return

    print(regret_analysis(strategy_scores={"A": 0.8, "B": 0.7, "C": 0.6}, best_score=0.9))


if __name__ == "__main__":
    main()
