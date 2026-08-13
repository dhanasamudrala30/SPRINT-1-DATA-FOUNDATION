from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_screener_min_roe():
    response = client.get(
        "/api/v1/screener",
        params={"min_roe": 15},
    )

    assert response.status_code == 200

    data = response.json()

    # Support the API's response envelope
    companies = data["data"] if isinstance(data, dict) and "data" in data else data

    assert isinstance(companies, list)

    for company in companies:
        roe = company.get("roe_pct")

        if roe is not None:
            assert roe >= 15


def test_screener_invalid_parameter():
    response = client.get(
        "/api/v1/screener",
        params={"min_roe": "invalid"},
    )

    assert response.status_code == 400