from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_governance_heatmap(governance: pd.DataFrame) -> pd.DataFrame:
    heatmap = governance.groupby("domain")["governance_risk_score"].mean().reset_index()
    heatmap["risk_band"] = heatmap["governance_risk_score"].map(
        lambda score: "critical" if score >= 75 else "high" if score >= 50 else "medium" if score >= 25 else "low"
    )
    out = ensure_dir(project_path("data/scorecards"))
    heatmap.to_csv(out / "governance_heatmap.csv", index=False)
    (out / "governance_heatmap.json").write_text(json.dumps(heatmap.to_dict(orient="records"), indent=2), encoding="utf-8")
    return heatmap
