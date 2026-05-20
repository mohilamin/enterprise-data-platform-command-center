from __future__ import annotations

import pandas as pd


def calculate_governance_risk(signals: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    gov = signals.loc[signals["metric_name"].str.contains("governance|policy|trust|conflict|least", regex=True)]
    grouped = gov.groupby("data_product_id")["metric_value"].mean().reset_index(name="governance_risk_score")
    report = catalog[["data_product_id", "name", "domain", "owner"]].merge(grouped, on="data_product_id", how="left")
    report["governance_risk_score"] = report["governance_risk_score"].fillna(0).round(2)
    report["risk_band"] = report["governance_risk_score"].map(
        lambda score: "critical" if score >= 75 else "high" if score >= 50 else "medium" if score >= 25 else "low"
    )
    return report
