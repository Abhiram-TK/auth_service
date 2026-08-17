from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.database.connection import SessionLocal
from app.main import app
from app.models.user import User


client = TestClient(app)


def create_registration_payload():

    unique_id = uuid4().hex

    return {"first_name": "Test",
            "last_name": "Registration",
            "email": f"test.registration.{unique_id}@example.com",
            "username": f"test_user_{unique_id[:12]}",
            "password": "TestPassword123",}


def cleanup_user(email: str):

    db = SessionLocal()

    try:

        user = db.query(User).filter(User.email == email).first()

        if user:

            db.delete(user)
            db.commit()

    finally:

        db.close()


def test_register_creates_user():

    payload = create_registration_payload()

    try:

        response = client.post("/register", json=payload)

        assert response.status_code == 200
        assert response.json()["message"] == "user created"

        db = SessionLocal()

        try:

            user = db.query(User).filter(User.email == payload["email"]).first()

            assert user is not None
            assert user.username == payload["username"]
            assert user.first_name == payload["first_name"]
            assert user.last_name == payload["last_name"]
            assert user.is_active is True
            assert user.role.name == "viewer"
            assert user.password_hash != payload["password"]
            assert user.password_hash

        finally:

            db.close()

    finally:

        cleanup_user(payload["email"])


def test_register_rejects_duplicate_email():

    payload = create_registration_payload()

    try:

        first_response = client.post("/register", json=payload)

        assert first_response.status_code == 200

        duplicate_payload = payload.copy()
        duplicate_payload["username"] = (f"duplicate_email_{uuid4().hex[:12]}")

        duplicate_response = client.post("/register",
                                         json=duplicate_payload)

        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "email already exists"

    finally:

        cleanup_user(payload["email"])


def test_register_rejects_duplicate_username():

    payload = create_registration_payload()

    try:

        first_response = client.post("/register", json=payload)

        assert first_response.status_code == 200

        duplicate_payload = payload.copy()
        duplicate_payload["email"] = (f"duplicate.username.{uuid4().hex}@example.com")

        duplicate_response = client.post("/register",
                                         json=duplicate_payload)

        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "username already exists"

    finally:
        
        cleanup_user(payload["email"])