"""Evidence-first evaluation and benchmarking layer for CityPulse."""

from citypulse.evaluation.benchmark import benchmark_run, build_synthetic_scenario, run_benchmark
from citypulse.evaluation.registry import EvaluationRegistry
from citypulse.evaluation.service import EvaluationService

__all__ = [
    "EvaluationRegistry",
    "EvaluationService",
    "benchmark_run",
    "build_synthetic_scenario",
    "run_benchmark",
]
