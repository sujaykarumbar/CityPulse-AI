from __future__ import annotations

from enum import StrEnum


class Topic(StrEnum):
    TRAFFIC_RAW = "citypulse.traffic.raw"
    WEATHER_RAW = "citypulse.weather.raw"
    MOBILITY_RAW = "citypulse.mobility.raw"
    ENERGY_RAW = "citypulse.energy.raw"
    TRANSIT_RAW = "citypulse.transit.raw"
    FEATURES = "citypulse.features"
    PREDICTIONS = "citypulse.predictions"
    ANOMALIES = "citypulse.anomalies"
    RISK = "citypulse.risk"
    DIGITAL_TWIN = "citypulse.digital_twin"
    DEAD_LETTER = "citypulse.dead_letter"
    SYSTEM = "citypulse.system"


ALL_TOPICS = [topic.value for topic in Topic]
