from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DAGNode:
    name: str
    node_type: str = "variable"
    metadata: dict[str, object] = field(default_factory=dict)
