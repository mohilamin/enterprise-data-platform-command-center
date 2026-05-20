from __future__ import annotations

import json

import pandas as pd

from src.common.logging import get_logger
from src.common.paths import ensure_dir, project_path

LOGGER = get_logger(__name__)

PRODUCTS = [
    ("DP-001", "customer_360", "customer", "Customer Platform", "tier_1", "critical"),
    ("DP-002", "revenue_metrics", "finance", "Finance Analytics", "tier_1", "critical"),
    ("DP-003", "fraud_detection_features", "risk", "Fraud MLOps", "tier_1", "critical"),
    ("DP-004", "payment_risk_scoring", "risk", "Payments Risk", "tier_1", "critical"),
    ("DP-005", "enterprise_rag_search", "ai_platform", "GenAI Platform", "tier_2", "high"),
    ("DP-006", "support_intelligence", "operations", "Support Analytics", "tier_2", "high"),
    ("DP-007", "ai_governance_gateway", "governance", "AI Governance", "tier_1", "critical"),
    ("DP-008", "semantic_metrics_layer", "governance", "Analytics Engineering", "tier_1", "critical"),
    ("DP-009", "data_quality_certification", "governance", "Data Quality", "tier_1", "critical"),
    ("DP-010", "pipeline_reliability_monitoring", "operations", "Data Platform", "tier_1", "critical"),
    ("DP-011", "supply_chain_risk_monitoring", "operations", "Supply Chain Analytics", "tier_2", "medium"),
    ("DP-012", "executive_reporting_mart", "executive", "Executive Analytics", "tier_1", "critical"),
]


def generate_data_product_catalog() -> pd.DataFrame:
    rows = []
    for product_id, name, domain, owner, tier, criticality in PRODUCTS:
        rows.append(
            {
                "data_product_id": product_id,
                "name": name,
                "domain": domain,
                "owner": owner,
                "tier": tier,
                "business_criticality": criticality,
                "upstream_systems": "data_quality_command_center,pipeline_reliability_incident_lab",
                "downstream_consumers": "executive_dashboard,ai_agents,business_reporting",
                "freshness_sla_hours": 4 if tier == "tier_1" else 12,
                "reliability_sla_percent": 99.0 if tier == "tier_1" else 97.5,
                "ai_consumption_allowed": domain in {"customer", "finance", "risk", "ai_platform", "governance"},
                "governance_required": True,
                "executive_visible": criticality in {"critical", "high"},
            }
        )
    frame = pd.DataFrame(rows)
    out = ensure_dir(project_path("data/data_products"))
    frame.to_csv(out / "data_product_catalog.csv", index=False)
    (out / "data_product_catalog.json").write_text(json.dumps(frame.to_dict(orient="records"), indent=2), encoding="utf-8")
    LOGGER.info("generated data product catalog")
    return frame


def main() -> None:
    generate_data_product_catalog()


if __name__ == "__main__":
    main()
