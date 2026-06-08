from app.database.connection import SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

ROLE_PERMISSION_MAPPING = {

    "viewer": ["view_transactions", "view_inventory"],

    "recruiter": ["view_transactions", "create_transactions", "view_inventory", "reserve_inventory"],

    "admin": ["view_transactions", "create_transactions", "update_transactions", "view_inventory", "reserve_inventory", "dispatch_inventory"]}

def seed_role_permissions():

    db = SessionLocal()

    try:

        for role_name, permission_names in ROLE_PERMISSION_MAPPING.items():

            role = (db.query(Role).filter(Role.name == role_name).first())

            if not role:

                print(f"Role not found: {role_name}")

                continue

            for permission_name in permission_names:

                permission = (db.query(Permission).filter(Permission.name == permission_name).first())

                if not permission:

                    print(f"Permission not found: {permission_name}")

                    continue

                if permission not in role.permissions:

                    role.permissions.append(permission)

        db.commit()

        print("Role permissions seeded successfully!")

    except Exception as error:

        db.rollback()

        print(f"Seeding failed: {error}")

    finally:

        db.close()

if __name__ == "__main__":

    seed_role_permissions()