from __future__ import annotations

from typing import Any

import yaml

from src.common.paths import project_path


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load(project_path(path).read_text(encoding="utf-8")) or {}
