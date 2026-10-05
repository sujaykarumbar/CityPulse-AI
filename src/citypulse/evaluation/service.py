from __future__ import annotations

from pathlib import Path
from typing import Any

from citypulse.evaluation.benchmark import benchmark_run, build_synthetic_scenario
from citypulse.evaluation.registry import EvaluationRegistry
from citypulse.evaluation.reproducibility import build_reproducibility_metadata


class EvaluationService:
    def __init__(self, root: Path | str = Path("artifacts/evaluation")) -> None:
        self.registry = EvaluationRegistry(Path(root))

    def status(self) -> dict[str, Any]:
        experiments = self.registry.list()
        benchmark_status = "NOT_RUN" if not experiments else "MEASURED"
        return {
            "status": "EVALUATION_NOT_AVAILABLE" if not experiments else "EVALUATION_AVAILABLE",
            "benchmark_status": benchmark_status,
            "experiments": len(experiments),
            "limitations": [
                "No verified urban benchmark data or model outputs are present in this checkout.",
                "Synthetic scenarios remain synthetic and must not be confused with observed ground truth.",
            ],
            "reproducibility": build_reproducibility_metadata(),
        }

    def benchmark(
        self,
        observed: list[float] | list[Any],
        predicted: list[float] | list[Any],
        *,
        task: str = "urban-benchmark",
        domain: str = "urban",
        dataset_version: str | None = None,
        model_version: str | None = None,
        result_type: str = "FORECAST",
    ) -> dict[str, Any]:
        result = benchmark_run(
            observed,
            predicted,
            task=task,
            domain=domain,
            dataset_version=dataset_version,
            model_version=model_version,
            result_type=result_type,
        )
        self.registry.register(result)
        return result

    def synthetic(self, domain: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
        result = build_synthetic_scenario(domain, config)
        self.registry.register(result)
        return result

    def history(self) -> list[dict[str, Any]]:
        return self.registry.list()
