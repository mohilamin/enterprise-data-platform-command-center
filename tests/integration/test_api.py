from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_api_platform_summary(built_platform):
    response = client.get("/platform-summary")
    assert response.status_code == 200
    assert "platform_health_score" in response.json()


def test_api_data_products(built_platform):
    response = client.get("/data-products")
    assert response.status_code == 200
    assert len(response.json()) == 12


def test_api_data_product_detail(built_platform):
    response = client.get("/data-products/DP-001")
    assert response.status_code == 200


def test_api_incidents(built_platform):
    response = client.get("/incidents")
    assert response.status_code == 200
    assert len(response.json()) == 8


def test_api_incident_detail(built_platform):
    response = client.get("/incidents/INC-001")
    assert response.status_code == 200


def test_api_governance_heatmap(built_platform):
    response = client.get("/governance-heatmap")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_api_ai_readiness(built_platform):
    response = client.get("/ai-readiness")
    assert response.status_code == 200
    assert "summary" in response.json()


def test_api_sla_report(built_platform):
    response = client.get("/sla-report")
    assert response.status_code == 200
    assert "summary" in response.json()


def test_api_lineage_impact(built_platform):
    response = client.get("/lineage-impact")
    assert response.status_code == 200
    assert "nodes" in response.json()


def test_api_executive_summary(built_platform):
    response = client.get("/executive-summary")
    assert response.status_code == 200
    assert "total_incidents" in response.json()


def test_api_scorecards(built_platform):
    response = client.get("/scorecards")
    assert response.status_code == 200
    assert "platform_health" in response.json()


def test_api_simulate_incident():
    response = client.post("/simulate-incident", json={"incident_type": "demo", "data_product_id": "DP-001", "severity": "high"})
    assert response.status_code == 200
    assert response.json()["status"] == "simulated"


def test_api_refresh_platform_health():
    response = client.post("/refresh-platform-health")
    assert response.status_code == 200
    assert "platform_health_score" in response.json()
