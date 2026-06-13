from fastapi import APIRouter, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from datetime import datetime

from app.database.connection import get_db

from app.models.user import User
from app.models.role import Role

from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.schemas.token_schema import TokenValidationRequest

from app.core.logger import logger
from app.core.security import hash_password, verify_password

from app.services.rbac_service import (RoleChecker)
from app.services.jwt_service import (create_access_token)

from app.middleware.auth_middleware import (get_current_user, decode_access_token)


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(User.email == request.email).first()

    if existing_email:

        raise HTTPException(status_code=400, detail="email already exists")

    existing_username = db.query(User).filter(User.username == request.username).first()

    if existing_username:

        raise HTTPException(status_code=400, detail="username already exists")

    default_role = db.query(Role).filter(Role.name == "viewer").first()

    if not default_role:

        default_role = Role(name="viewer")

        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    hashed_password = hash_password(request.password)

    new_user = User(email=request.email, username=request.username, password_hash=hashed_password, role_id=default_role.id, is_active=True)

    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:

        logger.error(f"Database failure during registration: {str(e)}")

        raise HTTPException(status_code=500, detail="Database operation failed")

    logger.info(f"User registered: {new_user.email}")

    return {"message": "user created"}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:

        logger.error(f"Login failed - email not found: {form_data.username}")

        raise HTTPException(status_code=401, detail="invalid email or password")

    if not user.is_active:

        logger.error(f"Login blocked - inactive account: {user.email}")

        raise HTTPException(status_code=403, detail="User account is disabled")
    
    password_valid = verify_password(form_data.password, user.password_hash)

    if not password_valid:

        logger.error(f"Login failed - invalid password: {user.email}")

        raise HTTPException(status_code=401, detail="invalid email or password")
    
    user.last_login = datetime.utcnow()

    db.commit()
    db.refresh(user)

    access_token = create_access_token({"user_id": user.id,"email": user.email, "role": user.role.name, "is_active": user.is_active})

    logger.info(f"Token generated for: {user.email}")

    logger.info(f"User login success: {user.email}")

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_profile(current_user = Depends(get_current_user)):

    logger.info(f"Protected route accessed by: {current_user['email']}")

    return {"emial": current_user["email"],"role": current_user["role"]}


@router.get("/admin/dashboard")
def admin_dashboard(current_user = Depends(RoleChecker(["admin"]))):

    return {"message": "Admin dashboarrd access granted","user": current_user}


@router.post("/validate-token")
def validate_token(request: TokenValidationRequest):

    payload = decode_access_token(request.token)

    if not payload:

        return {"valid": False}

    return {"valid": True, "user_id": payload.get("user_id"), "email": payload.get("email"), "role": payload.get("role"), "is_active": payload.get("is_active")}