from __future__ import annotations

from src.common.logging import get_logger
from src.common.paths import ensure_dir, project_path
from src.data_generation.generate_data_product_catalog import generate_data_product_catalog
from src.data_generation.generate_incident_scenarios import generate_incident_scenarios
from src.data_generation.generate_platform_signals import generate_platform_signals
from src.governance.governance_risk import calculate_governance_risk
from src.health.ai_readiness_health import calculate_ai_readiness
from src.health.data_product_health import calculate_data_product_health
from src.health.platform_health import calculate_platform_health
from src.health.sla_health import calculate_sla_health
from src.incidents.impact_assessment import assess_impact
from src.incidents.incident_correlator import correlate_incidents
from src.incidents.incident_timeline import build_incident_timeline
from src.ingestion.loaders import load_catalog, load_incidents, load_platform_signals
from src.ingestion.normalizer import normalize_signals
from src.ingestion.warehouse_loader import load_command_center_warehouse
from src.lineage.graph_exporter import export_graphs
from src.scorecards.ai_readiness_summary import write_ai_readiness_summary
from src.scorecards.data_product_health_report import write_data_product_health_report
from src.scorecards.enterprise_risk_summary import write_enterprise_risk_summary
from src.scorecards.governance_heatmap import write_governance_heatmap
from src.scorecards.incident_report import write_incident_report
from src.scorecards.platform_health_scorecard import write_platform_health_scorecard
from src.scorecards.sla_report import write_sla_report

LOGGER = get_logger(__name__)


def run_pipeline() -> dict[str, object]:
    """Run the command center pipeline."""
    generate_data_product_catalog()
    generate_platform_signals()
    generate_incident_scenarios()
    catalog = load_catalog()
    signals = load_platform_signals()
    incidents = load_incidents()
    normalized = normalize_signals(signals, catalog, incidents)
    health = calculate_data_product_health(signals, catalog)
    platform = calculate_platform_health(health)
    sla = calculate_sla_health(signals)
    ai = calculate_ai_readiness(signals, health)
    governance = calculate_governance_risk(signals, catalog)
    correlated = correlate_incidents(incidents, signals)
    impact = assess_impact(correlated, catalog)
    timeline = build_incident_timeline(correlated)
    nodes, edges = export_graphs(signals, catalog, correlated)
    ensure_dir(project_path("data/incidents"))
    timeline.to_csv(project_path("data/incidents/incident_timeline.csv"), index=False)
    ensure_dir(project_path("data/governance"))
    governance.to_csv(project_path("data/governance/normalized_governance_risk.csv"), index=False)
    ensure_dir(project_path("data/health"))
    ai.to_csv(project_path("data/health/normalized_ai_readiness.csv"), index=False)
    ensure_dir(project_path("data/executive"))
    write_data_product_health_report(health)
    write_platform_health_scorecard(platform)
    write_enterprise_risk_summary(correlated, governance)
    write_governance_heatmap(governance)
    write_ai_readiness_summary(ai)
    write_sla_report(sla)
    write_incident_report(impact)
    platform_summary = {
        **platform,
        "total_data_products": int(len(catalog)),
        "total_incidents": int(len(correlated)),
        "critical_incidents": int((correlated["severity"] == "critical").sum()),
    }
    (project_path("data/executive/executive_summary.json")).write_text(
        __import__("json").dumps(platform_summary, indent=2), encoding="utf-8"
    )
    load_command_center_warehouse(
        {
            "data_products": catalog,
            "platform_signals": signals,
            "data_product_health": health,
            "platform_incidents": correlated,
            "governance_risk": governance,
            "ai_readiness": ai,
            "sla_status": sla,
            "lineage_nodes": nodes,
            "lineage_edges": edges,
            "scorecards": health[["data_product_id", "data_product_health_score", "status"]],
            **normalized,
        }
    )
    LOGGER.info("enterprise command center pipeline complete")
    return platform_summary


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
