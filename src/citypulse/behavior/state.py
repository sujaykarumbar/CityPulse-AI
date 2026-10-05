from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UrbanSystemState:
    """A snapshot of an urban system at a point in time."""

    timestamp: str
    geography: str
    population: dict[str, Any] = field(default_factory=dict)
    mobility: dict[str, Any] = field(default_factory=dict)
    traffic: dict[str, Any] = field(default_factory=dict)
    energy: dict[str, Any] = field(default_factory=dict)
    infrastructure: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, Any] = field(default_factory=dict)
    risk: dict[str, Any] = field(default_factory=dict)
    policy: dict[str, Any] = field(default_factory=dict)
    economic_context: dict[str, Any] = field(default_factory=dict)
    technology_adoption: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "geography": self.geography,
            "population": self.population,
            "mobility": self.mobility,
            "traffic": self.traffic,
            "energy": self.energy,
            "infrastructure": self.infrastructure,
            "environment": self.environment,
            "risk": self.risk,
            "policy": self.policy,
            "economic_context": self.economic_context,
            "technology_adoption": self.technology_adoption,
        }


@dataclass
class BehaviorState:
    """Behavioral response state for agents and travelers."""

    mode_choice: dict[str, float] = field(default_factory=dict)
    route_choice: dict[str, float] = field(default_factory=dict)
    departure_time: dict[str, float] = field(default_factory=dict)
    trip_frequency: dict[str, float] = field(default_factory=dict)
    vehicle_usage: dict[str, float] = field(default_factory=dict)
    transit_usage: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode_choice": self.mode_choice,
            "route_choice": self.route_choice,
            "departure_time": self.departure_time,
            "trip_frequency": self.trip_frequency,
            "vehicle_usage": self.vehicle_usage,
            "transit_usage": self.transit_usage,
        }
