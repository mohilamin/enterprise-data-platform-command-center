from __future__ import annotations

import pandas as pd


def assess_impact(incidents: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    report = incidents.merge(
        catalog[["data_product_id", "name", "downstream_consumers", "executive_visible"]], on="data_product_id", how="left"
    )
    report["business_impact"] = report["severity"].map(lambda value: "executive escalation" if value == "critical" else "owner remediation")
    return report
