from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EnvironmentalObservation:
    timestamp: str
    geometry: str
    variable: str
    value: float
    unit: str
    source: str
    quality: float = 0.0
    confidence: float = 0.0
    provenance: Dict[str, Any] = field(default_factory=dict)
    status: str = "MODEL_DERIVED"


@dataclass
class WeatherObservation(EnvironmentalObservation):
    pass


@dataclass
class ClimateObservation(EnvironmentalObservation):
    period: str = "synthetic"


@dataclass
class AirQualityObservation(EnvironmentalObservation):
    pollutant: str = "pm25"


@dataclass
class WaterObservation(EnvironmentalObservation):
    metric: str = "flood_depth"


@dataclass
class HeatObservation(EnvironmentalObservation):
    index_type: str = "heat_index"


@dataclass
class HazardObservation:
    hazard_type: str
    intensity: float
    severity: str
    confidence: float
    source: str = "synthetic"
    status: str = "MODEL_DERIVED"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvironmentalExposure:
    city_id: str
    heat_risk: float
    flood_risk: float
    air_quality: float
    resilience_index: float
    status: str = "MODEL_DERIVED"
    indicators: Dict[str, Any] = field(default_factory=dict)
    caveats: List[str] = field(default_factory=list)
