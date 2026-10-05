from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SplitIndices:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray
    status: str = "MEASURED"


def chronological_split(sample_count: int, train_fraction: float = 0.7, validation_fraction: float = 0.15) -> SplitIndices:
    if sample_count < 1 or not 0 < train_fraction < 1 or not 0 < validation_fraction < 1 or train_fraction + validation_fraction >= 1:
        raise ValueError("INVALID_CHRONOLOGICAL_SPLIT")
    train_end = int(sample_count * train_fraction)
    validation_end = train_end + int(sample_count * validation_fraction)
    if train_end < 1 or validation_end <= train_end or validation_end >= sample_count:
        raise ValueError("INSUFFICIENT_SAMPLES_FOR_SPLIT")
    return SplitIndices(np.arange(0, train_end), np.arange(train_end, validation_end), np.arange(validation_end, sample_count))


def spatial_holdout(entity_ids: list[str], holdout_fraction: float = 0.2, seed: int = 42) -> tuple[list[str], list[str]]:
    if not 0 < holdout_fraction < 1 or len(set(entity_ids)) < 2:
        raise ValueError("INSUFFICIENT_ENTITIES_FOR_SPATIAL_HOLDOUT")
    unique = np.array(sorted(set(entity_ids)), dtype=object)
    rng = np.random.default_rng(seed)
    rng.shuffle(unique)
    n_test = max(1, int(len(unique) * holdout_fraction))
    test = set(unique[:n_test].tolist())
    return [item for item in entity_ids if item not in test], [item for item in entity_ids if item in test]
