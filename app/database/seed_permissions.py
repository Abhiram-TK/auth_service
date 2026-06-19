from app.database.connection import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission

PERMISSIONS = [

    # Transactions
    {"name": "create_transactions", "description": "Create new financial transactions."},
    {"name": "view_transactions", "description": "View transaction records and transaction details."},
    {"name": "update_transactions", "description": "Modify existing transaction information."},

    # Inventory
    {"name": "view_inventory", "description": "View inventory batches and stock availability."},
    {"name": "reserve_inventory", "description": "Create inventory reservations from available stock."},

    # Products
    {"name": "view_products", "description": "View product catalog information."},

    # Reservations
    {"name": "view_reservations", "description": "View inventory reservation records."},

    # Dispatch
    {"name": "dispatch_inventory", "description": "Dispatch reserved inventory for shipment."},
    {"name": "view_dispatches", "description": "View dispatch and shipment records."},

    # Events
    {"name": "process_events", "description": "Process inbound system integration events."},

    # Users
    {"name": "view_users", "description": "View user accounts and profile information."},
    {"name": "disable_users", "description": "Disable user accounts and revoke access."},

    # Roles
    {"name": "view_roles", "description": "View available roles and role definition."},
    {"name": "create_roles", "description": "Create new roles in the RBAC system."},
    {"name": "assign_roles", "description": "Assign roles to users."},

    # Permissions
    {"name": "view_permissions", "description": "View permission catalog and permission assignments."},
    {"name": "create_permissions", "description": "Create new permissions in the RBAC system."},
    {"name": "assign_permissions", "description": "Assign permissions to roles."}
    
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