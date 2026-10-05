from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pandas as pd

from citypulse.validation.backtesting.walk_forward import walk_forward_splits
from citypulse.validation.benchmarking.metrics import regression_metrics


def walk_forward_backtest(
    frame: pd.DataFrame,
    timestamp_column: str,
    target_column: str,
    predictor: Callable[[pd.DataFrame, pd.DataFrame], list[float]],
    initial_train_size: int,
    validation_size: int,
    step_size: int | None = None,
) -> dict[str, Any]:
    if timestamp_column not in frame or target_column not in frame:
        raise ValueError("REQUIRED_COLUMN_NOT_FOUND")
    ordered = frame.sort_values(timestamp_column).reset_index(drop=True)
    splits = walk_forward_splits(len(ordered), initial_train_size, validation_size, step_size)
    fold_results = []
    for fold_id, (train_indices, test_indices) in enumerate(splits, start=1):
        train = ordered.iloc[train_indices]
        test = ordered.iloc[test_indices]
        predictions = predictor(train, test)
        observed = pd.to_numeric(test[target_column], errors="raise").astype(float).tolist()
        metrics = regression_metrics(observed, predictions)
        fold_results.append({"fold": fold_id, "train_end": str(train[timestamp_column].max()), "test_start": str(test[timestamp_column].min()), "test_end": str(test[timestamp_column].max()), "metrics": metrics})
    return {"status": "MEASURED" if fold_results else "VALIDATION_NOT_AVAILABLE", "folds": fold_results, "leakage_controls": ["chronological ordering", "train indices strictly precede validation indices", "predictor receives train and validation partitions separately"]}
