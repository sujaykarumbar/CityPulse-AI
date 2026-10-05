from __future__ import annotations

from collections.abc import Mapping


def mode_choice_probability(scores: Mapping[str, float] | None) -> dict[str, float]:
    """Convert utility-like scores into normalized mode-choice probabilities."""

    if not scores:
        return {}

    total = sum(float(value) for value in scores.values())
    if total == 0:
        return {mode: 0.0 for mode in scores}

    return {mode: float(value) / float(total) for mode, value in scores.items()}
