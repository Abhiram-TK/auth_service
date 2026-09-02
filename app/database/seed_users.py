from faker import Faker

from random import randint, random, choice

from datetime import datetime, timedelta, timezone

from app.database.connection import SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.core.config import settings
from app.core.security import hash_password

fake = Faker("en_IN")

EMAIL_PROVIDERS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

ROLE_USER_COUNTS = {"viewer": 25,
                    "recruiter": 10,
                    "manager": 5,
                    "admin": 3,
                    "support": 2,
                    "auditor": 2}

TOTAL_EXPECTED_USERS = sum(ROLE_USER_COUNTS.values())

def create_fake_user(db, role_id):

    first_name = fake.first_name()
    last_name = fake.last_name()

    username = (f"{first_name.lower()}"
                f"{last_name.lower()}"
                f"{randint(100,999)}")

    random_number = randint(100, 999)
    provider = choice(EMAIL_PROVIDERS)

    email = (f"{first_name.lower()}"
             f"{last_name.lower()}"
             f"{random_number}"
             f"@{provider}")

    password_hash = hash_password("Password123")

    is_active = random() > 0.07

    last_login = datetime.now(timezone.utc) - timedelta(days=randint(0, 30))

    user = User(first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password_hash=password_hash,
                role_id=role_id,
                is_active=is_active,
                last_login=last_login)

    db.add(user)

    return 1

def seed_demo_admin(db, admin_role):
    
    demo_admin_created = 0
    demo_admin_existing = 0

    existing_demo_admin = (db.query(User).filter(User.email == settings.DEMO_ADMIN_EMAIL).first())

    if existing_demo_admin:

        print(f"Demo admin already exists: "
              f"{settings.DEMO_ADMIN_EMAIL}. Skipping.")

        demo_admin_existing = 1

        return demo_admin_created, demo_admin_existing

    existing_demo_username = (db.query(User).filter(User.username == settings.DEMO_ADMIN_USERNAME).first())

    if existing_demo_username:

        raise Exception(f"Demo admin username already exists: "
                        f"{settings.DEMO_ADMIN_USERNAME}")

    demo_admin = User(first_name="Demo",
                      last_name="Administrator",
                      username=settings.DEMO_ADMIN_USERNAME,
                      email=settings.DEMO_ADMIN_EMAIL,
                      password_hash=hash_password(settings.DEMO_ADMIN_PASSWORD),
                      role_id=admin_role.id,
                      is_active=True)

    db.add(demo_admin)

    demo_admin_created = 1

    print(f"Demo admin created: "
          f"{settings.DEMO_ADMIN_EMAIL}")

    return demo_admin_created, demo_admin_existing

def seed_users():

    db = SessionLocal()

    created_users = 0
    existing_users = 0

    demo_admin_created = 0
    demo_admin_existing = 0

    try:

        roles = {role.name: role for role in db.query(Role).all()}

        missing_roles = [role_name for role_name in ROLE_USER_COUNTS if role_name not in roles]

        if missing_roles:

            raise Exception(f"Required roles not found: {', '.join(missing_roles)}")

        admin_role = roles.get("admin")

        if not admin_role:

            raise Exception("Required role not found: admin")

        for role_name, target_count in ROLE_USER_COUNTS.items():

            role = roles[role_name]

            existing_count = (db.query(User).filter(User.role_id == role.id).count())

            if existing_count >= target_count:

                print(f"{role_name}: "
                      f"{existing_count}/{target_count} "
                      f"users already exist. Skipping.")

                existing_users += existing_count

                continue

            existing_users += existing_count

            missing_users = target_count - existing_count

            print(f"{role_name}: "
                  f"creating {missing_users} missing users.")

            for _ in range(missing_users):

                created_users += create_fake_user(db, role.id)

        (demo_admin_created, demo_admin_existing) = seed_demo_admin(db=db, admin_role=admin_role)

        db.commit()

        print("\n========== User Seed Summary ==========")

        print(f"Users expected : {TOTAL_EXPECTED_USERS}")
        print(f"Users existing : {existing_users}")
        print(f"Users created  : {created_users}")

        print("\n---------- Demo Admin Summary ----------")

        print("Demo Admin expected : 1")
        print(f"Demo Admin existing : "
              f"{demo_admin_existing}/1")
        print(f"Demo Admin created  : "
              f"{demo_admin_created}")

        print("=======================================\n")

    except Exception as error:

        db.rollback()

        print(f"Seeder failed: {error}")

        raise

    finally:

        db.close()

if __name__ == "__main__":

    seed_users()