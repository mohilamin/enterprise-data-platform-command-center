import pandas as pd

from src.data_generation.generate_data_product_catalog import generate_data_product_catalog
from src.data_generation.generate_incident_scenarios import generate_incident_scenarios
from src.data_generation.generate_platform_signals import generate_platform_signals
from src.governance.governance_risk import calculate_governance_risk
from src.health.data_product_health import calculate_data_product_health
from src.health.platform_health import calculate_platform_health
from src.health.sla_health import calculate_sla_health
from src.incidents.impact_assessment import assess_impact
from src.incidents.incident_correlator import correlate_incidents
from src.incidents.severity import severity_score
from src.ingestion.normalizer import normalize_signals
from src.lineage.dependency_graph import build_dependency_edges


def test_generate_catalog_returns_12_rows():
    assert len(generate_data_product_catalog()) == 12


def test_generate_signals_returns_systems():
    assert len(generate_platform_signals()) == 6


def test_generate_incidents_returns_8_rows():
    assert len(generate_incident_scenarios()) == 8


def test_normalizer_outputs_expected_keys():
    catalog = generate_data_product_catalog()
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    incidents = generate_incident_scenarios()
    outputs = normalize_signals(signals, catalog, incidents)
    assert "normalized_platform_signals" in outputs


def test_data_product_health_has_scores():
    catalog = generate_data_product_catalog()
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    report = calculate_data_product_health(signals, catalog)
    assert "data_product_health_score" in report.columns


def test_platform_health_score_range():
    summary = calculate_platform_health(pd.DataFrame({"data_product_health_score": [80, 90]}))
    assert 0 <= summary["platform_health_score"] <= 100


def test_sla_health_has_sla_met():
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    assert "sla_met" in calculate_sla_health(signals).columns


def test_governance_risk_has_band():
    catalog = generate_data_product_catalog()
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    report = calculate_governance_risk(signals, catalog)
    assert "risk_band" in report.columns


def test_incident_correlation_adds_signal_count():
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    incidents = generate_incident_scenarios()
    report = correlate_incidents(incidents, signals)
    assert "related_signal_count" in report.columns


def test_impact_assessment_adds_business_impact():
    catalog = generate_data_product_catalog()
    incidents = generate_incident_scenarios()
    report = assess_impact(incidents, catalog)
    assert "business_impact" in report.columns


def test_severity_score_critical():
    assert severity_score("critical") == 95


def test_dependency_graph_has_nodes_and_edges():
    catalog = generate_data_product_catalog()
    signals = pd.read_csv("data/raw_signals/system_health_signals.csv")
    nodes, edges = build_dependency_edges(signals, catalog)
    assert not nodes.empty
    assert not edges.empty
