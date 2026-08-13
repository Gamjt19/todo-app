import os

os.environ["TESTING"] = "true"

from app.app import app  # noqa: E402


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
