from __future__ import annotations

import argparse
import json
from pathlib import Path

from citypulse.mlops.registry import ModelRegistry


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the CITYPULSE local MLOps registry.")
    parser.add_argument("command", choices=["registry", "experiments", "monitor", "drift", "performance", "lineage", "retrain", "report", "health"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--root", type=Path, default=Path("artifacts/mlops"))
    args = parser.parse_args()
    registry = ModelRegistry(args.root)
    if args.command in {"registry", "experiments", "lineage"}:
        payload = {"models": [model.model_dump(mode="json") for model in registry.list(args.model)]}
    elif args.command == "retrain":
        payload = {"jobs": [job.model_dump(mode="json") for job in registry.retraining_jobs(args.model)]}
    else:
        payload = {"status": "NO_DATA_AVAILABLE", "command": args.command, "model": args.model}
    if args.command == "report":
        output = Path("reports/mlops/final_report.md")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# CITYPULSE MLOps Report\n\nNo registered models or measured production monitoring records are present in this checkout.\n", encoding="utf-8")
        print(output)
        return
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()
