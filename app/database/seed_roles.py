from app.database.connection import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission

ROLES = [
    {"name": "viewer", "description": "Can view system resources"},
    {"name": "recruiter", "description": "Can create and manage business operations"},
    {"name": "admin", "description": "Full system access"}
]

def seed_roles():

    db = SessionLocal()

    try:

        for role_data in ROLES:

            existing_role = (db.query(Role).filter(Role.name == role_data["name"]).first())

            if not existing_role:

                existing_role.description = role_data["description"]

            else:    

                db.add(Role(**role_data))

        db.commit()

        print("Roles seeded successfully!")

    finally:

        db.close()

if __name__ == "__main__":

    seed_roles()