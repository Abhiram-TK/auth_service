from app.database.connection import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission


PERMISSIONS = [
    {"name": "view_transactions", "description": "View transaction records"},
    {"name": "create_transactions", "description": "Create new transactions"},
    {"name": "update_transactions", "description": "Update existing transactions"},
    {"name": "view_inventory", "description": "View inventory records"},
    {"name": "reserve_inventory", "description": "Reserve inventory stock"},
    {"name": "dispatch_inventory", "description": "Dispatch reserved inventory"}
]

def seed_permissions():

    db = SessionLocal()

    try:

        for permission_data in PERMISSIONS:

            existing_permission = (db.query(Permission).filter(Permission.name == permission_data["name"]).first())

            if not existing_permission:

                db.add(Permission(**permission_data))

        db.commit()

        print("Permissions seeded successfully!")

    finally:

        db.close()

if __name__ == "__main__":

    seed_permissions()