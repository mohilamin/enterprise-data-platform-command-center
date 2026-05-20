from __future__ import annotations

import pandas as pd

from src.common.paths import ensure_dir, project_path


def _status(score: float) -> str:
    if score >= 85:
        return "healthy"
    if score >= 70:
        return "watch"
    if score >= 50:
        return "degraded"
    return "critical"


def calculate_data_product_health(signals: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    grouped = signals.groupby("data_product_id")["metric_value"].mean().reset_index(name="data_product_health_score")
    report = catalog.merge(grouped, on="data_product_id", how="left")
    report["data_product_health_score"] = report["data_product_health_score"].fillna(0).round(2)
    report["status"] = report["data_product_health_score"].map(_status)
    report["drivers"] = report["status"].map(lambda value: "No major drivers." if value == "healthy" else "Signal degradation detected.")
    report["recommended_action"] = report["status"].map(lambda value: "Monitor." if value in {"healthy", "watch"} else "Escalate to owner.")
    ensure_dir(project_path("data/health"))
    report.to_csv(project_path("data/health/normalized_data_product_health.csv"), index=False)
    return report
