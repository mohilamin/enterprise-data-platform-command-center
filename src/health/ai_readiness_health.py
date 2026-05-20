from __future__ import annotations

import pandas as pd


def calculate_ai_readiness(signals: pd.DataFrame, data_product_health: pd.DataFrame) -> pd.DataFrame:
    ai = signals.loc[signals["metric_name"].str.contains("ai|rag|mlops|model|hallucination|citation", regex=True)]
    grouped = ai.groupby("data_product_id")["metric_value"].mean().reset_index(name="ai_readiness_score")
    report = data_product_health[["data_product_id", "name", "domain"]].merge(grouped, on="data_product_id", how="left")
    report["ai_readiness_score"] = report["ai_readiness_score"].fillna(data_product_health["data_product_health_score"]).round(2)
    report["ai_ready_status"] = report["ai_readiness_score"].map(lambda score: "ready" if score >= 75 else "not_ready")
    return report
