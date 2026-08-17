from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.main import app
from app.models.role import Role
from app.models.user import User


client = TestClient(app)


def login(email: str, password: str) -> str:

    response = client.post("/login",
                           data={"username": email,
                                 "password": password})

    assert response.status_code == 200

    return response.json()["access_token"]


def create_test_user(role_name: str = "viewer") -> tuple[User, str]:

    unique_id = uuid4().hex

    email = f"user.management.{unique_id}@example.com"
    username = f"user_management_{unique_id[:12]}"
    password = "TestPassword123"

    db = SessionLocal()

    try:

        role = db.query(Role).filter(Role.name == role_name).first()

        assert role is not None

        user = User(first_name="User",
                    last_name="Management",
                    email=email,
                    username=username,
                    password_hash=hash_password(password),
                    role_id=role.id,
                    is_active=True)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user, password

    finally:

        db.close()


def cleanup_user(user_id: int):

    db = SessionLocal()

    try:

        user = db.query(User).filter(User.id == user_id).first()

        if user:

            db.delete(user)
            db.commit()

    finally:

        db.close()


def get_user_state(user_id: int) -> User:

    db = SessionLocal()

    try:

        user = db.query(User).filter(User.id == user_id).first()

        assert user is not None

        return user

    finally:

        db.close()


def test_get_users_returns_users_for_authorized_admin():

    admin_token = login(settings.DEMO_ADMIN_EMAIL,
                        settings.DEMO_ADMIN_PASSWORD)

    test_user, _ = create_test_user()

    try:

        response = client.get("/users/",
                              headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200

        users = response.json()

        matching_users = [user for user in users if user["id"] == test_user.id]

        assert len(matching_users) == 1

        returned_user = matching_users[0]

        assert returned_user["email"] == test_user.email
        assert returned_user["username"] == test_user.username
        assert returned_user["role"] == "viewer"
        assert returned_user["is_active"] is True

    finally:

        cleanup_user(test_user.id)


def test_get_users_rejects_missing_jwt():

    response = client.get("/users/")

    assert response.status_code == 401
    assert response.json()["detail"] == ("JWT missing from Authorization: Bearer header. Use Swagger's Authorize control.")


def test_get_users_rejects_user_without_view_users_permission():

    test_user, password = create_test_user(role_name="viewer")

    try:

        viewer_token = login(test_user.email,
                             password)

        response = client.get("/users/",
                              headers={"Authorization": f"Bearer {viewer_token}"})

        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"

    finally:

        cleanup_user(test_user.id)


def test_disable_user_deactivates_account_and_blocks_login():

    admin_token = login(settings.DEMO_ADMIN_EMAIL,
                        settings.DEMO_ADMIN_PASSWORD)

    test_user, password = create_test_user()

    try:

        response = client.delete(f"/users/{test_user.id}",
                                 headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        assert response.json()["message"] == "User deactivated successfully"

        disabled_user = get_user_state(test_user.id)

        assert disabled_user.is_active is False

        login_response = client.post("/login",
                                     data={"username": test_user.email,
                                           "password": password})

        assert login_response.status_code == 403
        assert login_response.json()["detail"] == "User account is disabled"

    finally:

        cleanup_user(test_user.id)


def test_admin_cannot_disable_own_account():

    admin_token = login(settings.DEMO_ADMIN_EMAIL,
                        settings.DEMO_ADMIN_PASSWORD)

    db = SessionLocal()

    try:

        admin_user = (db.query(User).filter(User.email == settings.DEMO_ADMIN_EMAIL).first())

        assert admin_user is not None

        admin_user_id = admin_user.id

    finally:

        db.close()

    response = client.delete(f"/users/{admin_user_id}",
                             headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 400
    assert response.json()["detail"] == ("Administrators cannot disable their own account.")