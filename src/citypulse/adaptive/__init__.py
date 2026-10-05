"""Adaptive urban intelligence and closed-loop decision support."""

from .assumptions import check_assumption
from .change_detection import detect_change
from .engine import AdaptiveUrbanIntelligenceEngine
from .state import UrbanStrategyState
from .strategy import StrategyLifecycle, compute_strategy_health, generate_alternatives

__all__ = [
    "AdaptiveUrbanIntelligenceEngine",
    "StrategyLifecycle",
    "UrbanStrategyState",
    "check_assumption",
    "compute_strategy_health",
    "detect_change",
    "generate_alternatives",
]
