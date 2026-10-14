def test_health_is_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "up"


def test_feature_routes_are_wired(client):
    paths = client.get("/openapi.json").json()["paths"]

    assert "/api/v1/accounts/{account_number}/mini-statement" in paths
    assert "/api/v1/accounts/{account_number}/minimum-balance-check" in paths
