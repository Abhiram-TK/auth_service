from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role

from app.core.logger import logger

def get_all_users(db: Session):

    return db.query(User).all()

def get_user_by_id(user_id: int, db: Session):

    user = (db.query(User).filter(User.id == user_id).first())

    if not user:

        raise HTTPException(status_code=404, detail="User not found")

    return user

def update_user_role(user_id: int, role_name: str, db: Session):

    user = (db.query(User).filter(User.id == user_id).first())

    if not user:

        raise HTTPException(status_code=404, detail="User not found")

    role = (db.query(Role).filter(Role.name == role_name).first())

    if not role:

        raise HTTPException(status_code=404, detail="Role not found")

    old_role = user.role.name

    user.role_id = role.id

    logger.warning(f"ROLE_CHANGED | user_id={user.id} | email={user.email} | old_role={old_role} | new_role={role.name}")

    db.commit()
    db.refresh(user)

    return user


def deactivate_user(user_id: int, db: Session):

    user = (db.query(User).filter(User.id == user_id).first())

    if not user:

        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False

    db.commit()
    db.refresh(user)

    logger.warning(f"USER_DISABLED | id={user.id} | email={user.email}")

    return {"message": "User deactivated successfully"}