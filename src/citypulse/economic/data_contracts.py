from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EconomicObservation:
    geography: str
    time: str
    sector: str
    indicator: str
    value: float
    unit: str = "index"
    source: str = "synthetic"
    confidence: float = 0.5
    provenance: dict[str, Any] = field(default_factory=dict)
    status: str = "MODEL_DERIVED"


@dataclass
class IndustryObservation(EconomicObservation):
    pass


@dataclass
class EmploymentObservation(EconomicObservation):
    pass


@dataclass
class IncomeObservation(EconomicObservation):
    pass


@dataclass
class ProductionObservation(EconomicObservation):
    pass


@dataclass
class ConsumptionObservation(EconomicObservation):
    pass


@dataclass
class TradeObservation(EconomicObservation):
    pass


@dataclass
class FreightObservation(EconomicObservation):
    pass


@dataclass
class CommodityObservation(EconomicObservation):
    pass


@dataclass
class ResourceFlowObservation(EconomicObservation):
    pass
