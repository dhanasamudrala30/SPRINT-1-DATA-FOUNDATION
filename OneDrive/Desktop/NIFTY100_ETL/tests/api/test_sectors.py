from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_get_all_sectors():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["count"] == 10
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 10

    for sector in data["data"]:
        assert "broad_sector" in sector
        assert "company_count" in sector
        assert "median_roe" in sector
        assert "median_pe" in sector
        assert "median_de" in sector


def test_information_technology_sector():
    response = client.get(
        "/api/v1/sectors/Information%20Technology/companies"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sector"] == "Information Technology"
    assert "data" in data
    assert isinstance(data["data"], list)

    for company in data["data"]:
        assert company["broad_sector"] == "Information Technology"


def test_unknown_sector_returns_404():
    response = client.get(
        "/api/v1/sectors/UNKNOWN_SECTOR/companies"
    )

    assert response.status_code == 404