from __future__ import annotations

import argparse

from citypulse.adaptive.assumptions import check_assumption
from citypulse.adaptive.change_detection import detect_change
from citypulse.adaptive.engine import AdaptiveUrbanIntelligenceEngine
from citypulse.adaptive.strategy import StrategyLifecycle, compute_strategy_health


def main() -> None:
    parser = argparse.ArgumentParser(description="Run adaptive intelligence monitoring checks.")
    parser.add_argument("--mode", choices=["assumption", "change", "monitor", "health", "transition"], default="monitor")
    parser.add_argument("--city-id", default="demo-city")
    parser.add_argument("--strategy-id", default="strategy-demo")
    args = parser.parse_args()

    if args.mode == "assumption":
        print(check_assumption(
            assumption_id="population-growth",
            description="population growth remains in the 2-4% range",
            variable="population_growth",
            expected_range=(2.0, 4.0),
            observed_value=5.2,
        ))
        return

    if args.mode == "change":
        print(detect_change(metric_name="transit_ridership", previous_value=60.0, current_value=90.0, threshold=20.0))
        return

    if args.mode == "health":
        print(compute_strategy_health({"performance": 0.6, "robustness": 0.7, "assumption_validity": 0.5}))
        return

    if args.mode == "transition":
        print({"status": StrategyLifecycle().advance("ACTIVE", "review")})
        return

    print(AdaptiveUrbanIntelligenceEngine().monitor_strategy(
        city_id=args.city_id,
        strategy_id=args.strategy_id,
        observed_metrics={"performance": 0.6, "robustness": 0.7, "assumption_validity": 0.5},
        expected_metrics={"performance": 0.8, "robustness": 0.8, "assumption_validity": 0.8},
    ))


if __name__ == "__main__":
    main()
