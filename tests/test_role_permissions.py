from fastapi.testclient import TestClient

from app.core.config import settings
from app.database.connection import SessionLocal
from app.main import app
from app.models.permission import Permission
from app.models.role import Role


client = TestClient(app)


def get_admin_token() -> str:

    response = client.post("/login",
                           data={"username": settings.DEMO_ADMIN_EMAIL,
                                 "password": settings.DEMO_ADMIN_PASSWORD})

    assert response.status_code == 200

    return response.json()["access_token"]


def get_admin_role_and_target_permission():

    db = SessionLocal()

    try:

        role = db.query(Role).filter(Role.name == "admin").first()
        permission = (db.query(Permission).filter(Permission.name == "view_permissions").first())

        assert role is not None
        assert permission is not None

        return role.id, permission.id, permission.name

    finally:

        db.close()


def set_permission_assignment(role_id: int, permission_id: int, assigned: bool):

    db = SessionLocal()

    try:

        role = db.query(Role).filter(Role.id == role_id).first()
        permission = (db.query(Permission).filter(Permission.id == permission_id).first())

        assert role is not None
        assert permission is not None

        is_assigned = permission in role.permissions

        if assigned and not is_assigned:

            role.permissions.append(permission)

        elif not assigned and is_assigned:

            role.permissions.remove(permission)

        db.commit()

    finally:

        db.close()


def is_permission_assigned(role_id: int, permission_id: int) -> bool:

    db = SessionLocal()

    try:

        role = db.query(Role).filter(Role.id == role_id).first()
        permission = (db.query(Permission).filter(Permission.id == permission_id).first())

        assert role is not None
        assert permission is not None

        return permission in role.permissions

    finally:

        db.close()


def test_assign_permission_to_role():

    token = get_admin_token()

    role_id, permission_id, permission_name = (get_admin_role_and_target_permission())

    set_permission_assignment(role_id=role_id,
                              permission_id=permission_id,
                              assigned=False)

    try:

        response = client.post(f"/roles/{role_id}/permissions",
                               json={"permission": permission_name},
                               headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.json()["message"] == "Permission assigned successfully"

        assert is_permission_assigned(role_id=role_id,
                                      permission_id=permission_id) is True

    finally:

        set_permission_assignment(role_id=role_id,
                                  permission_id=permission_id,
                                  assigned=True)


def test_assign_permission_rejects_duplicate_assignment():

    token = get_admin_token()

    role_id, permission_id, permission_name = (get_admin_role_and_target_permission())

    set_permission_assignment(role_id=role_id,
                              permission_id=permission_id,
                              assigned=True)

    try:

        response = client.post(f"/roles/{role_id}/permissions",
                               json={"permission": permission_name},
                               headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.json()["detail"] == "Permission already assigned"

    finally:

        set_permission_assignment(role_id=role_id,
                                  permission_id=permission_id,
                                  assigned=True)


def test_remove_permission_from_role():

    token = get_admin_token()

    role_id, permission_id, permission_name = (get_admin_role_and_target_permission())

    set_permission_assignment(role_id=role_id,
                              permission_id=permission_id,
                              assigned=True)

    try:

        response = client.delete(f"/roles/{role_id}/permissions/{permission_name}",
                                 headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.json()["message"] == "Permission removed successfully"

        assert is_permission_assigned(role_id=role_id,
                                      permission_id=permission_id) is False

    finally:

        set_permission_assignment(role_id=role_id,
                                  permission_id=permission_id,
                                  assigned=True)


def test_assign_permission_rejects_missing_role():

    token = get_admin_token()

    _, _, permission_name = get_admin_role_and_target_permission()

    response = client.post("/roles/999999/permissions",
                            json={"permission": permission_name},
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"


def test_assign_permission_rejects_missing_permission():

    token = get_admin_token()

    role_id, _, _ = get_admin_role_and_target_permission()

    response = client.post(f"/roles/{role_id}/permissions",
                           json={"permission": "permission_that_does_not_exist"},
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Permission not found"