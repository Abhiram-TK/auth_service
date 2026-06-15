from faker import Faker

from random import randint, random

from datetime import datetime, timedelta

from app.database.connection import SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.core.security import hash_password

fake = Faker("en_IN")

db = SessionLocal()

def create_fake_user(role_id):

    first_name = fake.first_name()

    last_name = fake.last_name()

    username = fake.unique.user_name()

    email = fake.unique.email()

    password_hash = hash_password("Password123")

    is_active = random() > 0.07

    last_login = datetime.utcnow() - timedelta(days=randint(0, 30))

    user = User(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password_hash, role_id=role_id, is_active=is_active,
                last_login=last_login)

    db.add(user)

if __name__ == "__main__":

    try:

        viewer_role = (db.query(Role).filter(Role.name == "viewer").first())

        recruiter_role = (db.query(Role).filter(Role.name == "recruiter").first())

        manager_role = (db.query(Role).filter(Role.name == "manager").first())

        admin_role = (db.query(Role).filter(Role.name == "admin").first())

        support_role = (db.query(Role).filter(Role.name == "support").first())

        if not all([viewer_role, recruiter_role, manager_role, admin_role, support_role]):

            raise Exception("Required roles not found. Verify viewer, recruiter, manager, admin, and support roles exist.")

        for _ in range(25):
            create_fake_user(viewer_role.id)

        for _ in range(10):
            create_fake_user(recruiter_role.id)

        for _ in range(5):
            create_fake_user(manager_role.id)

        for _ in range(3):
            create_fake_user(admin_role.id)

        for _ in range(2):
            create_fake_user(support_role.id)

        db.commit()

        print("45 users seeded successfully")

    except Exception as error:

        db.rollback()

        print(f"Seeder failed: {error}")

    finally:

        db.close()