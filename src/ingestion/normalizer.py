from __future__ import annotations

import pandas as pd

from src.common.paths import ensure_dir, project_path


def normalize_signals(signals: pd.DataFrame, catalog: pd.DataFrame, incidents: pd.DataFrame) -> dict[str, pd.DataFrame]:
    normalized = signals.merge(catalog[["data_product_id", "name", "domain", "business_criticality"]], on="data_product_id", how="left")
    sla = normalized.loc[normalized["metric_name"].str.contains("sla|freshness", regex=True)].copy()
    governance = normalized.loc[normalized["metric_name"].str.contains("governance|policy|least|trust|conflict", regex=True)].copy()
    ai = normalized.loc[normalized["metric_name"].str.contains("ai|rag|hallucination|citation|mlops|model", regex=True)].copy()
    out = ensure_dir(project_path("data/normalized"))
    outputs = {
        "normalized_platform_signals": normalized,
        "normalized_sla_status": sla,
        "normalized_governance_risk": governance,
        "normalized_ai_readiness": ai,
        "normalized_incidents": incidents,
        "normalized_lineage_dependencies": normalized[["system_name", "data_product_id", "name"]].drop_duplicates(),
    }
    for name, frame in outputs.items():
        frame.to_csv(out / f"{name}.csv", index=False)
    return outputs
