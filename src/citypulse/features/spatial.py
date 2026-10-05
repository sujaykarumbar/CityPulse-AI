from __future__ import annotations

import numpy as np
import pandas as pd


def haversine_km(latitude: pd.Series, longitude: pd.Series, ref_latitude: float, ref_longitude: float) -> pd.Series:
    """Calculate great-circle distance to an explicitly supplied reference point."""

    lat1, lon1, lat2, lon2 = map(
        np.radians, [latitude.astype(float), longitude.astype(float), ref_latitude, ref_longitude]
    )
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    value = np.sin(delta_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2
    return 6371.0088 * 2 * np.arcsin(np.sqrt(value))


def create_spatial_features(
    df: pd.DataFrame,
    reference_points: dict[str, tuple[float, float]] | None = None,
) -> pd.DataFrame:
    """Add spatial features without embedding city-specific coordinates."""

    result = df.copy()
    latitude = "latitude" if "latitude" in result.columns else "lat" if "lat" in result.columns else None
    longitude = "longitude" if "longitude" in result.columns else "lon" if "lon" in result.columns else None
    if latitude and longitude and reference_points:
        for name, (ref_latitude, ref_longitude) in reference_points.items():
            result[f"distance_to_{name}_km"] = haversine_km(
                result[latitude], result[longitude], ref_latitude, ref_longitude
            )
    if "length" in result.columns:
        result["road_length_km"] = pd.to_numeric(result["length"], errors="coerce") / 1000
    return result
