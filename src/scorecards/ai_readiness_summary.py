from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_ai_readiness_summary(ai_readiness: pd.DataFrame) -> dict[str, object]:
    summary = {
        "total_products": int(len(ai_readiness)),
        "ai_ready_products": int((ai_readiness["ai_ready_status"] == "ready").sum()),
        "average_ai_readiness_score": round(float(ai_readiness["ai_readiness_score"].mean()), 2),
    }
    out = ensure_dir(project_path("data/scorecards"))
    ai_readiness.to_csv(out / "ai_readiness_summary.csv", index=False)
    (out / "ai_readiness_summary.json").write_text(
        json.dumps({"summary": summary, "products": ai_readiness.to_dict(orient="records")}, indent=2), encoding="utf-8"
    )
    return summary
