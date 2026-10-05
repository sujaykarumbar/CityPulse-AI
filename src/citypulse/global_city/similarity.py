from __future__ import annotations

import math
from typing import Any


def city_similarity(left: dict[str, float], right: dict[str, float]) -> dict[str, Any]:
    keys = sorted(set(left) | set(right))
    if not keys:
        return {"status": "NOT_AVAILABLE", "score": 0.0, "method": "feature_overlap"}

    left_values = [float(left.get(key, 0.0)) for key in keys]
    right_values = [float(right.get(key, 0.0)) for key in keys]
    numerator = sum(a * b for a, b in zip(left_values, right_values))
    left_norm = math.sqrt(sum(a * a for a in left_values))
    right_norm = math.sqrt(sum(a * a for a in right_values))
    if left_norm == 0.0 or right_norm == 0.0:
        return {"status": "NOT_AVAILABLE", "score": 0.0, "method": "feature_overlap"}

    score = numerator / (left_norm * right_norm)
    return {
        "status": "MEASURED",
        "score": max(0.0, min(1.0, score)),
        "method": "cosine_similarity",
        "features_used": keys,
    }
