from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

SUPPORTED_FIELDS = {"temperature", "precipitation", "humidity", "wind_speed", "pressure"}


def generate_weather(config: dict[str, Any]) -> pd.DataFrame:
    count = int(config.get("sample_count", 24))
    seed = int(config.get("seed", 42))
    if not 1 <= count <= 100_000:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED")
    fields = config.get("fields", ["temperature", "precipitation"])
    if not set(fields).issubset(SUPPORTED_FIELDS):
        raise ValueError("UNSUPPORTED_WEATHER_FIELD")
    rng = np.random.default_rng(seed)
    result: dict[str, Any] = {"timestamp": pd.date_range("2000-01-01T00:00:00Z", periods=count, freq="h")}
    defaults = {"temperature": (18.0, 5.0), "precipitation": (0.0, 1.5), "humidity": (60.0, 10.0), "wind_speed": (3.0, 1.0), "pressure": (1013.0, 4.0)}
    for name in fields:
        mean, std = defaults[name]
        result[name] = np.clip(rng.normal(float(config.get(f"{name}_mean", mean)), float(config.get(f"{name}_std", std)), count), 0, None) if name != "temperature" else rng.normal(float(config.get(f"{name}_mean", mean)), float(config.get(f"{name}_std", std)), count)
    result.update({"data_origin": "SYNTHETIC", "generator_version": "weather-synth-0.1.0", "generation_seed": seed, "generation_config": [dict(config)] * count})
    return pd.DataFrame(result)
