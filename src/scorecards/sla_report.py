from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_sla_report(sla: pd.DataFrame) -> dict[str, object]:
    summary = {"total_sla_signals": int(len(sla)), "sla_compliance_rate": round(float(sla["sla_met"].mean() * 100), 2) if len(sla) else 0.0}
    out = ensure_dir(project_path("data/scorecards"))
    sla.to_csv(out / "platform_sla_report.csv", index=False)
    (out / "platform_sla_report.json").write_text(
        json.dumps({"summary": summary, "rows": sla.to_dict(orient="records")}, indent=2), encoding="utf-8"
    )
    return summary
