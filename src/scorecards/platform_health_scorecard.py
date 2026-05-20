from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_platform_health_scorecard(summary: dict[str, object]) -> dict[str, object]:
    out = ensure_dir(project_path("data/scorecards"))
    pd.DataFrame([summary]).to_csv(out / "platform_health_scorecard.csv", index=False)
    (out / "platform_health_scorecard.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
