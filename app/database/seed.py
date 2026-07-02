"""
Authentication Service Seed Orchestrator

Responsibilities
----------------
1. Execute every seed module.
2. Preserve dependency order.
3. Provide a single entry point for database seeding.
"""

from app.database.seed_roles import seed_roles
from app.database.seed_permissions import seed_permissions
from app.database.seed_role_permissions import seed_role_permissions
from app.database.seed_users import seed_users

def run_all_seeds() -> None:
    """
    Execute all database seeders in dependency order.
    """

    print("\n========== Database Seeding Started ==========\n")

    seed_roles()
    seed_permissions()
    seed_role_permissions()
    seed_users()

    print("\n========== Database Seeding Completed ==========\n")

if __name__ == "__main__":
    run_all_seeds()