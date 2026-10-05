from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: Path = Path("config/mlops.yaml")) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
