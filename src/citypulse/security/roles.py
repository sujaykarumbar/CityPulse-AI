from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    VIEWER = "VIEWER"
    ANALYST = "ANALYST"
    RESEARCHER = "RESEARCHER"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"

    @classmethod
    def from_value(cls, value: str | None) -> "Role":
        if value is None:
            return cls.VIEWER
        try:
            return cls(value.upper())
        except ValueError:
            return cls.VIEWER
