from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from citypulse.decision.optimizer import solve
from citypulse.decision.reporting import write_decision_report
from citypulse.decision.schemas import DecisionProblem


def main() -> None:
    parser = argparse.ArgumentParser(description="Run transparent multi-objective decision analysis.")
    parser.add_argument("--problem", type=Path, required=True)
    parser.add_argument("--report-dir", type=Path, default=Path("reports/decision"))
    args = parser.parse_args()
    raw = yaml.safe_load(args.problem.read_text(encoding="utf-8"))
    problem = DecisionProblem.model_validate(raw.get("decision_problem", raw))
    result = solve(problem)
    print(write_decision_report(result, args.report_dir))


if __name__ == "__main__":
    main()
