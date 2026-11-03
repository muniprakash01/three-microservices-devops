import app as order_app


def test_health():
    response = order_app.app.test_client().get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["service"] == "order-service"
