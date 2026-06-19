from app.database.connection import SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

ROLE_PERMISSION_MAPPING = {

    "viewer": ["view_transactions", "view_inventory",
               "view_products", "view_reservations",
               "view_dispatches"],

    "recruiter": ["create_transactions", "view_transactions",
                  "view_inventory", "reserve_inventory",
                  "view_products", "view_reservations",
                  "view_dispatches"],

    "support": ["view_users", "view_transactions",
                "view_inventory", "view_products",
                "view_reservations", "view_dispatches"],

    "auditor": ["view_transactions", "view_inventory",
                "view_products", "view_reservations",
                "view_dispatches"],

    "manager": ["create_transactions", "view_transactions",
                "update_transactions", "view_inventory",
                "reserve_inventory", "dispatch_inventory",
                "view_products", "view_reservations",
                "view_dispatches", "process_events",
                "view_users", "view_roles"],

    "admin": ["create_transactions", "view_transactions",
              "update_transactions", "view_inventory",
              "reserve_inventory", "view_products",
              "view_reservations", "dispatch_inventory",
              "view_dispatches", "process_events",
              "view_users", "disable_users",
              "view_roles", "create_roles",
              "assign_roles", "view_permissions",
              "create_permissions", "assign_permissions"]
              
}


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