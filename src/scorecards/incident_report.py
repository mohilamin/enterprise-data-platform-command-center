from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_incident_report(incidents: pd.DataFrame) -> pd.DataFrame:
    out = ensure_dir(project_path("data/scorecards"))
    incidents.to_csv(out / "cross_platform_incident_report.csv", index=False)
    payload = {"total_incidents": int(len(incidents)), "incidents": incidents.to_dict(orient="records")}
    (out / "cross_platform_incident_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return incidents
