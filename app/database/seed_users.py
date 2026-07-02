from faker import Faker

from random import randint, random, choice

from datetime import datetime, timedelta

from app.database.connection import SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.core.security import hash_password

fake = Faker("en_IN")

EMAIL_PROVIDERS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

ROLE_USER_COUNTS = {"viewer": 25, "recruiter": 10, "manager": 5, "admin": 3, "support": 2, "auditor": 2}

TOTAL_EXPECTED_USERS = sum(ROLE_USER_COUNTS.values())

def create_fake_user(db, role_id):

    first_name = fake.first_name()
    last_name = fake.last_name()

    username = (f"{first_name.lower()}"f"{last_name.lower()}"f"{randint(100,999)}")

    random_number = randint(100, 999)
    provider = choice(EMAIL_PROVIDERS)
    email = (f"{first_name.lower()}"f"{last_name.lower()}"f"{random_number}"f"@{provider}")

    password_hash = hash_password("Password123")

    is_active = random() > 0.07

    last_login = datetime.utcnow() - timedelta(days=randint(0, 30))

    user = User(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password_hash, role_id=role_id, is_active=is_active,
                last_login=last_login)

    db.add(user)

    return 1

def seed_users():
    """
    Seed demo users for every role.

    Safe to call from:
    - seed.py
    - startup event
    - command line
    """

    db = SessionLocal()

    created_users = 0
    existing_users = 0

    try:

        roles = {role.name: role 
                 for role in db.query(Role).all()}

        missing_roles = [
            role_name
            for role_name in ROLE_USER_COUNTS
            if role_name not in roles
        ]

        if missing_roles:

            raise Exception(f"Required roles not found: {', '.join(missing_roles)}")

        for role_name, target_count in ROLE_USER_COUNTS.items():

            role = roles[role_name]

            existing_count = (db.query(User).filter(User.role_id == role.id).count())

            if existing_count >= target_count:

                print(f"{role_name}: {existing_count}/{target_count} users already exist. Skipping.")

                existing_users += existing_count

                continue

            existing_users += existing_count

            missing_users = target_count - existing_count

            print(f"{role_name}: creating {missing_users} missing users.")

            for _ in range(missing_users):

                created_users += create_fake_user(db, role.id)

        db.commit()

        print("\n========== User Seed Summary ==========")

        print(f"Users expected : {TOTAL_EXPECTED_USERS}")
        print(f"Users existing : {existing_users}")
        print(f"Users created  : {created_users}")

        print("=======================================\n")

    except Exception as error:

        db.rollback()

        print(f"Seeder failed: {error}")

        raise

    finally:

        db.close()

if __name__ == "__main__":
    seed_users()