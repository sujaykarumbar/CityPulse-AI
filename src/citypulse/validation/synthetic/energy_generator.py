from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def generate_energy(config: dict[str, Any]) -> pd.DataFrame:
    count = int(config.get("sample_count", 24))
    seed = int(config.get("seed", 42))
    if not 1 <= count <= 100_000:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED")
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2000-01-01T00:00:00Z", periods=count, freq="h")
    base_load = float(config.get("base_load", 1.0))
    peak_gain = float(config.get("peak_gain", 0.2))
    if base_load < 0 or peak_gain < 0:
        raise ValueError("INVALID_GENERATOR_CONFIGURATION")
    hour = timestamps.hour.to_numpy()
    profile = np.where((hour >= 17) & (hour <= 21), peak_gain, 0.0)
    load = np.clip(base_load + profile + rng.normal(0, float(config.get("noise_std", 0.02)), count), 0, None)
    return pd.DataFrame({"timestamp": timestamps, "energy_demand": load, "data_origin": "SYNTHETIC", "generator_version": "energy-synth-0.1.0", "generation_seed": seed, "generation_config": [dict(config)] * count, "correlation_basis": "ASSUMED_CONFIGURABLE_NOT_ESTIMATED"})
