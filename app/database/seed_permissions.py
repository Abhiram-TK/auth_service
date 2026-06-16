from app.database.connection import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission

PERMISSIONS = [
    # Transactions
    {"name": "view_transactions", "description": "View transaction records"},
    {"name": "create_transactions", "description": "Create new transactions"},
    {"name": "update_transactions", "description": "Update existing transactions"},
    {"name": "delete_transactions", "description": "Delete transaction records"},
    {"name": "approve_transactions", "description": "Approve pending transactions"},
    {"name": "cancel_transactions", "description": "Cancel transactions"},
    {"name": "export_transactions", "description": "Export transaction data"},
    # Inventory
    {"name": "view_inventory", "description": "View inventory records"},
    {"name": "reserve_inventory", "description": "Reserve inventory stock"},
    {"name": "dispatch_inventory", "description": "Dispatch reserved inventory"},
    {"name": "receive_inventory", "description": "Receive inventory stock"},
    {"name": "adjust_inventory", "description": "Adjust inventory quantities"},
    {"name": "audit_inventory", "description": "Audit inventory records"},
    # Users
    {"name": "view_users", "description": "View user accounts"},
    {"name": "create_users", "description": "Create user accounts"},
    {"name": "update_users", "description": "Update user accounts"},
    {"name": "disable_users", "description": "Disable user accounts"},
    # Roles
    {"name": "view_roles", "description": "View available roles"},
    {"name": "assign_roles", "description": "Assign roles to users"},
    # Permissions
    {"name": "view_permissions", "description": "View permissions"},
    {"name": "assign_permissions", "description": "Assign permissions to roles"}
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