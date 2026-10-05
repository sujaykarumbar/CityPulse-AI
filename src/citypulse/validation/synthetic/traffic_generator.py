from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

GENERATOR_VERSION = "traffic-synth-0.1.0"
MAX_SAMPLES = 100_000


def generate_traffic(config: dict[str, Any]) -> pd.DataFrame:
    sample_count = int(config.get("sample_count", 24))
    seed = int(config.get("seed", 42))
    if sample_count < 1 or sample_count > MAX_SAMPLES:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED")
    base_volume = float(config.get("base_volume", 100.0))
    peak_multiplier = float(config.get("peak_multiplier", 1.5))
    noise_std = float(config.get("noise_std", 5.0))
    if base_volume < 0 or peak_multiplier <= 0 or noise_std < 0:
        raise ValueError("INVALID_GENERATOR_CONFIGURATION")
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2000-01-01T00:00:00Z", periods=sample_count, freq="h")
    hour = timestamps.hour.to_numpy()
    peak = ((hour >= 7) & (hour <= 9)) | ((hour >= 16) & (hour <= 18))
    volume = base_volume * np.where(peak, peak_multiplier, 1.0) + rng.normal(0, noise_std, sample_count)
    volume = np.clip(volume, 0, None)
    free_speed = float(config.get("free_speed", 50.0))
    speed = np.clip(free_speed * np.exp(-volume / float(config.get("volume_scale", 1000.0))), 0, free_speed)
    return pd.DataFrame({
        "timestamp": timestamps,
        "traffic_volume": volume,
        "average_speed": speed,
        "peak_period_assumption": peak,
        "data_origin": "SYNTHETIC",
        "generator_version": GENERATOR_VERSION,
        "generation_seed": seed,
        "generation_config": [dict(config)] * sample_count,
        "correlation_basis": "ASSUMED_CONFIGURABLE_NOT_ESTIMATED",
    })
