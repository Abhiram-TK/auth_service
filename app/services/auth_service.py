from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role

from app.core.logger import logger
from app.core.security import hash_password, verify_password

from app.services.jwt_service import (create_access_token, decode_access_token)


def register_user_service(request, db: Session):

    existing_email = (db.query(User).filter(User.email == request.email).first())

    if existing_email:

        raise HTTPException(status_code=400, detail="email already exists")

    existing_username = (db.query(User).filter(User.username == request.username).first())

    if existing_username:

        raise HTTPException(status_code=400, detail="username already exists")

    default_role = (db.query(Role).filter(Role.name == "viewer").first())

    if not default_role:

        raise HTTPException(status_code=500, detail="Default viewer role not found")

    hashed_password = hash_password(request.password)

    new_user = User(first_name=request.first_name, last_name=request.last_name, email=request.email, username=request.username, password_hash=hashed_password,
                    role_id=default_role.id, is_active=True)

    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as error:

        logger.error(f"DATABASE_FAILURE | registration | {str(error)}")

        raise HTTPException(status_code=500, detail="Database operation failed")

    logger.info(f"USER_CREATED | id={new_user.id} | email={new_user.email}")

    return {"message": "user created"}


def login_user_service(form_data, db: Session):

    user = (db.query(User).filter(User.email == form_data.username).first())

    if not user:

        logger.error(f"LOGIN_FAILED | reason=email_not_found | email={form_data.username}")

        raise HTTPException(status_code=401, detail="invalid email or password")

    if not user.is_active:

        logger.error(f"LOGIN_BLOCKED | reason=inactive_account | email={user.email}")

        raise HTTPException(status_code=403, detail="User account is disabled")

    password_valid = verify_password(form_data.password, user.password_hash)

    if not password_valid:

        logger.error(f"LOGIN_FAILED | reason=invalid_password | email={user.email}")

        raise HTTPException(status_code=401, detail="invalid email or password")

    user.last_login = datetime.utcnow()

    db.commit()
    db.refresh(user)

    access_token = create_access_token({"user_id": user.id, "email": user.email, "username": user.username,"role": user.role.name, "is_active": user.is_active})

    logger.info(f"TOKEN_ISSUED | user_id={user.id} | email={user.email} | role={user.role.name}")

    return {"access_token": access_token, "token_type": "bearer"}


def validate_token_service(token: str):

    payload = decode_access_token(token)

    if not payload:

        return {"valid": False}

    logger.info(f"TOKEN_VALIDATED | email={payload.get('email')}")

    return {"valid": True, "user_id": payload.get("user_id"), "email": payload.get("email"), "role": payload.get("role"), "is_active": payload.get("is_active")}