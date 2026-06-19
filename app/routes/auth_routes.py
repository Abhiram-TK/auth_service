from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.logger import logger

from app.database.connection import get_db

from app.models.user import User

from app.schemas.auth_schema import RegisterRequest
from app.schemas.token_schema import TokenValidationRequest

from app.services.auth_service import (register_user_service, login_user_service, validate_token_service)

from app.middleware.auth_middleware import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/register", summary="Register New User", description="""
             Create a new user account.

             Requirements:

             - Unique email
             - Unique username

             New users are assigned the Viewer role by default.""")

def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    return register_user_service(request=request, db=db)


@router.post("/login", summary="Authenticate User", description="""
             Authenticate a user and generate a JWT access token.
             
             Returns:
             
             - Access token
             - Token type
             - User identity claims""")

def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return login_user_service(form_data=form_data, db=db)


@router.get("/me", summary="Get current User Profile", description="""
            Return the currently authenticated user's profile.

            Requires:

            - Valid JWT token

            Returns user identity information.""")

def get_current_profile(current_user = Depends(get_current_user)):

    logger.info(f"PROFILE_ACCESSED | email={current_user['email']}")

    return {"user_id": current_user["user_id"], "email": current_user["email"], "username": current_user["username"],"role": current_user["role"]}

@router.get("/me/permissions", summary="Get Current User Permissions", description="""
            Return permissions assigned to the current user.

            Requires:

            - Valid JWT token

            Returns role and effective permissions.""")

def get_current_user_permissions(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    user = (db.query(User).filter(User.id == current_user["user_id"]).first())

    permissions = sorted(

        permission.name

        for permission in user.role.permissions

    )

    return {"user_id": user.id, "username": user.username, "role": user.role.name, "permissions": permissions}


@router.post("/validate-token", summary="Validate JWT Token", description="""
             Validate a JWT access token.

             Returns token validity and user identity information.""")

def validate_token(request: TokenValidationRequest):

    return validate_token_service(token=request.token)