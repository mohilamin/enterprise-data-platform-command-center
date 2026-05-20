from pathlib import Path

import pandas as pd


def test_full_pipeline_execution(built_platform):
    assert built_platform["total_data_products"] == 12


def test_catalog_csv_exists(built_platform):
    assert Path("data/data_products/data_product_catalog.csv").exists()


def test_catalog_json_exists(built_platform):
    assert Path("data/data_products/data_product_catalog.json").exists()


def test_catalog_row_count(built_platform):
    assert len(pd.read_csv("data/data_products/data_product_catalog.csv")) == 12


def test_platform_signals_exist(built_platform):
    assert Path("data/raw_signals/system_health_signals.csv").exists()


def test_signal_files_exist(built_platform):
    for name in [
        "data_quality_signals.csv",
        "rag_quality_signals.csv",
        "fraud_mlops_signals.csv",
        "pipeline_reliability_signals.csv",
        "semantic_metrics_signals.csv",
        "ai_governance_signals.csv",
    ]:
        assert Path(f"data/raw_signals/{name}").exists()


def test_platform_signal_schema(built_platform):
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    expected = {"signal_id", "system_name", "data_product_id", "metric_name", "metric_value", "status", "severity"}
    assert expected.issubset(signals.columns)


def test_incident_manifest_exists(built_platform):
    assert Path("data/incidents/injected_platform_incident_manifest.json").exists()


def test_platform_incidents_exist(built_platform):
    assert len(pd.read_csv("data/incidents/platform_incidents.csv")) == 8


def test_normalized_platform_signals_exist(built_platform):
    assert Path("data/normalized/normalized_platform_signals.csv").exists()


def test_normalized_incidents_exist(built_platform):
    assert Path("data/normalized/normalized_incidents.csv").exists()


def test_normalized_sla_status_exists(built_platform):
    assert Path("data/normalized/normalized_sla_status.csv").exists()


def test_normalized_governance_exists(built_platform):
    assert Path("data/normalized/normalized_governance_risk.csv").exists()


def test_normalized_ai_exists(built_platform):
    assert Path("data/normalized/normalized_ai_readiness.csv").exists()


def test_data_product_health_output_exists(built_platform):
    assert Path("data/health/normalized_data_product_health.csv").exists()


def test_data_product_health_score_range(built_platform):
    report = pd.read_csv("data/health/normalized_data_product_health.csv")
    assert report["data_product_health_score"].between(0, 100).all()


def test_ai_readiness_score_range(built_platform):
    report = pd.read_csv("data/health/normalized_ai_readiness.csv")
    assert report["ai_readiness_score"].between(0, 100).all()


def test_governance_risk_score_range(built_platform):
    report = pd.read_csv("data/governance/normalized_governance_risk.csv")
    assert report["governance_risk_score"].between(0, 100).all()


def test_platform_health_scorecard_exists(built_platform):
    assert Path("data/scorecards/platform_health_scorecard.json").exists()


def test_enterprise_risk_summary_exists(built_platform):
    assert Path("data/scorecards/enterprise_risk_summary.json").exists()


def test_data_product_health_report_exists(built_platform):
    assert Path("data/scorecards/data_product_health_report.json").exists()


def test_governance_heatmap_exists(built_platform):
    assert Path("data/scorecards/governance_heatmap.json").exists()


def test_ai_readiness_summary_exists(built_platform):
    assert Path("data/scorecards/ai_readiness_summary.json").exists()


def test_sla_report_exists(built_platform):
    assert Path("data/scorecards/platform_sla_report.json").exists()


def test_incident_report_exists(built_platform):
    assert Path("data/scorecards/cross_platform_incident_report.json").exists()


def test_incident_report_has_business_impact(built_platform):
    report = pd.read_csv("data/scorecards/cross_platform_incident_report.csv")
    assert "business_impact" in report.columns


def test_lineage_nodes_exist(built_platform):
    assert Path("data/lineage/dependency_nodes.csv").exists()


def test_lineage_edges_exist(built_platform):
    assert Path("data/lineage/dependency_edges.csv").exists()


def test_lineage_graph_json_exists(built_platform):
    assert Path("data/lineage/system_dependency_graph.json").exists()


def test_lineage_impact_json_exists(built_platform):
    assert Path("data/lineage/lineage_impact_graph.json").exists()


def test_executive_summary_exists(built_platform):
    assert Path("data/executive/executive_summary.json").exists()


def test_duckdb_warehouse_exists(built_platform):
    assert Path("data/warehouse/enterprise_command_center.duckdb").exists()


def test_sla_signals_have_boolean(built_platform):
    sla = pd.read_csv("data/scorecards/platform_sla_report.csv")
    assert "sla_met" in sla.columns


def test_governance_heatmap_has_domains(built_platform):
    heatmap = pd.read_csv("data/scorecards/governance_heatmap.csv")
    assert heatmap["domain"].notna().all()


def test_health_status_values(built_platform):
    report = pd.read_csv("data/scorecards/data_product_health_report.csv")
    assert set(report["status"]).issubset({"healthy", "watch", "degraded", "critical"})
