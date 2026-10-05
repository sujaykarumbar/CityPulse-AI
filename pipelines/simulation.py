from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from citypulse.simulation.reporting import write_report
from citypulse.simulation.scenario_engine import run_scenario
from citypulse.simulation.schemas import Scenario, UrbanState


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a validated CityPulse counterfactual scenario.")
    parser.add_argument("--scenario", type=Path, required=False)
    parser.add_argument("--baseline", type=Path, required=False)
    parser.add_argument("--report-dir", type=Path, default=Path("reports/simulation"))
    args = parser.parse_args()
    if not args.scenario or not args.baseline:
        raise SystemExit("DATA NOT AVAILABLE: provide --scenario and --baseline JSON files")
    scenario = Scenario.model_validate(yaml.safe_load(args.scenario.read_text(encoding="utf-8")))
    baseline = UrbanState.model_validate_json(args.baseline.read_text(encoding="utf-8"))
    result = run_scenario(scenario, baseline)
    print(write_report(result, args.report_dir))


if __name__ == "__main__":
    main()
