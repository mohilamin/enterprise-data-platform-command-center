from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_data_product_health_report(report: pd.DataFrame) -> pd.DataFrame:
    out = ensure_dir(project_path("data/scorecards"))
    report.to_csv(out / "data_product_health_report.csv", index=False)
    payload = {"total_data_products": int(len(report)), "products": report.to_dict(orient="records")}
    (out / "data_product_health_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return report
