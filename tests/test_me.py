from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)


def login_and_get_token() -> str:

    response = client.post("/login",
                           data={"username": settings.DEMO_ADMIN_EMAIL,
                                 "password": settings.DEMO_ADMIN_PASSWORD})

    assert response.status_code == 200

    return response.json()["access_token"]


def test_get_me_returns_authenticated_user_profile():

    access_token = login_and_get_token()

    response = client.get("/me",
                          headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == settings.DEMO_ADMIN_EMAIL
    assert body["username"] == settings.DEMO_ADMIN_USERNAME
    assert body["role"] == "admin"
    assert body["permissions"]
    assert body["user_id"]


def test_get_me_rejects_missing_jwt():

    response = client.get("/me")

    assert response.status_code == 401
    assert response.json()["detail"] == ("JWT missing from Authorization: Bearer header. Use Swagger's Authorize control.")


def test_get_me_rejects_invalid_jwt():

    response = client.get("/me",
                          headers={"Authorization": "Bearer invalid.jwt.token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid or expired token"