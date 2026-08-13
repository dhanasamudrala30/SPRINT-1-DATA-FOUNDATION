from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "db_row_counts" in data

    # Required database tables
    required_tables = {
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "sectors",
        "documents",
        "analysis",
    }

    assert required_tables.issubset(
        set(data["db_row_counts"].keys())
    )


def test_health_has_uptime():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0


def test_health_has_version():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert "version" in data
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0