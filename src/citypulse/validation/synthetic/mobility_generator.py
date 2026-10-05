from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def generate_mobility(config: dict[str, Any]) -> pd.DataFrame:
    zones = config.get("zones", [])
    count = int(config.get("sample_count", 0))
    seed = int(config.get("seed", 42))
    if not zones:
        raise ValueError("SYNTHETIC_ZONES_REQUIRED")
    if not 1 <= count <= 100_000:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED")
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2000-01-01T00:00:00Z", periods=count, freq="h")
    origins = rng.choice(zones, size=count)
    destinations = rng.choice(zones, size=count)
    trips = rng.poisson(float(config.get("mean_trip_count", 10.0)), size=count)
    return pd.DataFrame({"timestamp": timestamps, "origin_zone": origins, "destination_zone": destinations, "trip_count": trips, "data_origin": "SYNTHETIC", "generator_version": "mobility-synth-0.1.0", "generation_seed": seed, "generation_config": [dict(config)] * count})
