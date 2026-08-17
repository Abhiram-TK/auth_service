from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)


def test_login_returns_access_token():

    response = client.post("/login",
                           data={
                               "username": settings.DEMO_ADMIN_EMAIL,
                               "password": settings.DEMO_ADMIN_PASSWORD})

    assert response.status_code == 200

    body = response.json()

    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_rejects_invalid_credentials():

    response = client.post("/login",
                           data={
                               "username": settings.DEMO_ADMIN_EMAIL,
                               "password": "DefinitelyWrongPassword123!"})

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid email or password"


def test_validate_token_accepts_login_token():

    login_response = client.post("/login",
                                 data={"username": settings.DEMO_ADMIN_EMAIL,
                                       "password": settings.DEMO_ADMIN_PASSWORD})

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    validation_response = client.post("/validate-token",
                                      json={"token": access_token})

    assert validation_response.status_code == 200
    assert validation_response.json()["valid"] is True


def test_validate_token_rejects_altered_token():

    login_response = client.post("/login",
                                 data={"username": settings.DEMO_ADMIN_EMAIL,
                                       "password": settings.DEMO_ADMIN_PASSWORD})

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    altered_token = access_token[:-1] + ( "A" if access_token[-1] != "A" else "B")

    validation_response = client.post("/validate-token",
                                      json={"token": altered_token})

    assert validation_response.status_code == 200
    assert validation_response.json()["valid"] is False