from __future__ import annotations

import json

import pandas as pd

from src.common.logging import get_logger
from src.common.paths import ensure_dir, project_path
from src.common.time import utc_now_iso

LOGGER = get_logger(__name__)

INCIDENTS = [
    ("INC-001", "ai_agent_using_uncertified_metric", "semantic_metrics_trust_layer,ai_data_governance_gateway", "DP-008", "high"),
    ("INC-002", "rag_hallucination_from_stale_documents", "enterprise_rag_evaluation_lab,data_quality_command_center", "DP-005", "high"),
    ("INC-003", "fraud_model_drift_affecting_risk_scores", "payments_fraud_feature_store_mlops", "DP-003", "critical"),
    ("INC-004", "pipeline_sla_breach_delays_executive_reporting", "pipeline_reliability_incident_lab", "DP-012", "critical"),
    ("INC-005", "data_quality_failure_blocks_ai_consumption", "data_quality_command_center", "DP-009", "high"),
    ("INC-006", "policy_violation_exposes_restricted_columns", "ai_data_governance_gateway", "DP-007", "critical"),
    ("INC-007", "schema_drift_breaks_metric_trust", "pipeline_reliability_incident_lab,semantic_metrics_trust_layer", "DP-008", "high"),
    ("INC-008", "feature_store_quality_drop_impacts_model_score", "payments_fraud_feature_store_mlops", "DP-004", "high"),
]


def generate_incident_scenarios() -> pd.DataFrame:
    rows = []
    for incident_id, incident_type, systems, product_id, severity in INCIDENTS:
        rows.append(
            {
                "incident_id": incident_id,
                "incident_type": incident_type,
                "systems_involved": systems,
                "data_product_id": product_id,
                "severity": severity,
                "status": "open" if severity == "critical" else "contained",
                "detected_at": utc_now_iso(),
                "downstream_impact": "executive reporting and AI consumers impacted",
                "recommended_action": "Escalate to platform owner and remediate upstream signal.",
            }
        )
    frame = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/incidents"))
    frame.to_csv(out / "platform_incidents.csv", index=False)
    (out / "injected_platform_incident_manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    LOGGER.info("generated incident scenarios")
    return frame


def main() -> None:
    generate_incident_scenarios()


if __name__ == "__main__":
    main()
