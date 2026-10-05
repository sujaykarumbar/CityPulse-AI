from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_validation_config(path: Path = Path("config/validation.yaml")) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
