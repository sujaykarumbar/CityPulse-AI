from __future__ import annotations


def walk_forward_splits(
    sample_count: int,
    initial_train_size: int,
    validation_size: int,
    step_size: int | None = None,
    expanding: bool = True,
) -> list[tuple[list[int], list[int]]]:
    if sample_count < 0 or initial_train_size < 1 or validation_size < 1:
        raise ValueError("INVALID_SPLIT_CONFIGURATION")
    step = step_size or validation_size
    if step < 1:
        raise ValueError("step_size must be positive")
    splits: list[tuple[list[int], list[int]]] = []
    validation_start = initial_train_size
    while validation_start + validation_size <= sample_count:
        train_start = 0 if expanding else max(0, validation_start - initial_train_size)
        train = list(range(train_start, validation_start))
        validation = list(range(validation_start, validation_start + validation_size))
        splits.append((train, validation))
        validation_start += step
    return splits
