from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_get_all_companies():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["count"] == 92
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 92


def test_get_tcs():
    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"


def test_invalid_company_returns_404():
    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404