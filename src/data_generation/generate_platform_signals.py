from __future__ import annotations

import numpy as np
import pandas as pd

from src.common.logging import get_logger
from src.common.paths import ensure_dir, project_path
from src.common.time import utc_now_iso
from src.data_generation.generate_data_product_catalog import generate_data_product_catalog

LOGGER = get_logger(__name__)
SEED = 42

SYSTEM_FILES = {
    "data_quality_command_center": "data_quality_signals.csv",
    "enterprise_rag_evaluation_lab": "rag_quality_signals.csv",
    "payments_fraud_feature_store_mlops": "fraud_mlops_signals.csv",
    "pipeline_reliability_incident_lab": "pipeline_reliability_signals.csv",
    "semantic_metrics_trust_layer": "semantic_metrics_signals.csv",
    "ai_data_governance_gateway": "ai_governance_signals.csv",
}

METRIC_BY_SYSTEM = {
    "data_quality_command_center": ["quality_score", "freshness_status", "quarantine_rate", "ai_readiness_score"],
    "enterprise_rag_evaluation_lab": ["retrieval_accuracy", "citation_coverage", "hallucination_risk", "rag_trust_score"],
    "payments_fraud_feature_store_mlops": ["mlops_health_score", "model_drift", "feature_store_quality", "reason_code_coverage"],
    "pipeline_reliability_incident_lab": ["reliability_score", "sla_compliance", "schema_drift_count", "backfill_safety"],
    "semantic_metrics_trust_layer": ["semantic_trust_score", "metric_conflicts", "lineage_completeness", "ai_agent_metric_readiness"],
    "ai_data_governance_gateway": ["governance_risk_score", "policy_violations", "least_privilege_score", "blocked_request_rate"],
}


def _status(value: float, metric: str) -> tuple[str, str]:
    if "risk" in metric or "violations" in metric or "drift_count" in metric or "conflicts" in metric:
        if value >= 75:
            return "critical", "critical"
        if value >= 50:
            return "degraded", "high"
        if value >= 25:
            return "watch", "medium"
        return "healthy", "low"
    if value >= 85:
        return "healthy", "low"
    if value >= 70:
        return "watch", "medium"
    if value >= 50:
        return "degraded", "high"
    return "critical", "critical"


def generate_platform_signals() -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    catalog = generate_data_product_catalog()
    out = ensure_dir(project_path("data/raw_signals"))
    all_rows = []
    for system_name, file_name in SYSTEM_FILES.items():
        rows = []
        for product in catalog.itertuples(index=False):
            for metric in METRIC_BY_SYSTEM[system_name]:
                base = float(rng.normal(82, 12))
                if product.name in {"executive_reporting_mart", "semantic_metrics_layer"} and metric in {
                    "metric_conflicts",
                    "schema_drift_count",
                }:
                    base = float(rng.normal(45, 10))
                if "risk" in metric or "violations" in metric or "conflicts" in metric:
                    base = float(rng.normal(24, 18))
                value = round(float(np.clip(base, 0, 100)), 2)
                status, severity = _status(value, metric)
                rows.append(
                    {
                        "signal_id": f"SIG-{len(all_rows) + len(rows) + 1:05d}",
                        "system_name": system_name,
                        "data_product_id": product.data_product_id,
                        "metric_name": metric,
                        "metric_value": value,
                        "threshold": 75,
                        "status": status,
                        "severity": severity,
                        "measured_at": utc_now_iso(),
                        "owner": product.owner,
                        "recommended_action": "Investigate and remediate." if status in {"degraded", "critical"} else "Monitor.",
                    }
                )
        frame = pd.DataFrame(rows)
        frame.to_csv(out / file_name, index=False)
        all_rows.extend(rows)
    all_signals = pd.DataFrame(all_rows)
    all_signals.to_csv(out / "system_health_signals.csv", index=False)
    all_signals.loc[all_signals["metric_name"].str.contains("sla|freshness", regex=True)].to_csv(out / "sla_signals.csv", index=False)
    all_signals[["system_name", "data_product_id", "owner"]].drop_duplicates().to_csv(out / "usage_signals.csv", index=False)
    all_signals[["system_name", "data_product_id"]].drop_duplicates().to_csv(out / "lineage_dependency_signals.csv", index=False)
    LOGGER.info("generated platform signals")
    return {name: pd.read_csv(out / file_name) for name, file_name in SYSTEM_FILES.items()}


def main() -> None:
    generate_platform_signals()


if __name__ == "__main__":
    main()
