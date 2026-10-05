from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SpatialFrameSplit:
    train: pd.DataFrame
    test: pd.DataFrame
    metadata: dict[str, Any]


def spatial_frame_holdout(
    frame: pd.DataFrame,
    entity_column: str,
    holdout_fraction: float = 0.2,
    seed: int = 42,
) -> SpatialFrameSplit:
    if entity_column not in frame:
        raise ValueError("REQUIRED_SPATIAL_COLUMN_NOT_FOUND")
    if frame.empty or not 0 < holdout_fraction < 1 or frame[entity_column].isna().any():
        raise ValueError("INVALID_SPATIAL_SPLIT")

    entities = sorted(pd.unique(frame[entity_column]).tolist(), key=repr)
    if len(entities) < 2:
        raise ValueError("INSUFFICIENT_ENTITIES_FOR_SPATIAL_HOLDOUT")
    test_count = max(1, ceil(len(entities) * holdout_fraction))
    if test_count >= len(entities):
        raise ValueError("INSUFFICIENT_ENTITIES_FOR_SPATIAL_HOLDOUT")

    selected_indices = np.random.default_rng(seed).permutation(len(entities))[:test_count]
    test_entities = [entities[index] for index in selected_indices]
    test_mask = frame[entity_column].isin(test_entities)
    train = frame.loc[~test_mask].copy()
    test = frame.loc[test_mask].copy()
    train_entities = pd.unique(train[entity_column]).tolist()
    observed_test_entities = pd.unique(test[entity_column]).tolist()
    if set(train_entities) & set(observed_test_entities):
        raise ValueError("SPATIAL_SPLIT_INVARIANT_FAILED")

    return SpatialFrameSplit(
        train=train,
        test=test,
        metadata={
            "status": "SPLIT_CREATED",
            "entity_column": entity_column,
            "seed": seed,
            "train_entities": sorted(train_entities, key=repr),
            "test_entities": sorted(observed_test_entities, key=repr),
            "leakage_controls": ["entity groups are disjoint between train and test"],
        },
    )