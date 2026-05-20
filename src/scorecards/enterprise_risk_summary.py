from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_enterprise_risk_summary(incidents: pd.DataFrame, governance: pd.DataFrame) -> dict[str, object]:
    critical = int((incidents["severity"] == "critical").sum())
    high_risk_products = int(governance["risk_band"].isin(["high", "critical"]).sum())
    summary = {"total_incidents": int(len(incidents)), "critical_incidents": critical, "high_governance_risk_products": high_risk_products}
    out = ensure_dir(project_path("data/scorecards"))
    pd.DataFrame([summary]).to_csv(out / "enterprise_risk_summary.csv", index=False)
    (out / "enterprise_risk_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
