from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DAGEdge:
    source: str
    target: str
    edge_type: str = "causal"
    metadata: dict[str, object] = field(default_factory=dict)
