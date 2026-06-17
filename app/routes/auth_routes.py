from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.logger import logger

from app.database.connection import get_db

from app.schemas.auth_schema import RegisterRequest
from app.schemas.token_schema import TokenValidationRequest

from app.services.rbac_service import (RoleChecker)
from app.services.auth_service import (register_user_service, login_user_service, validate_token_service)

from app.middleware.auth_middleware import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/register", summary="Register New User", description="""
             Create a new user account.

             Requirements:

             - Unique email
             - Unique username
             - Password minimum 8 characters

             New users are assigned the Viewer role by default.""")

def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    return register_user_service(request=request, db=db)


@router.post("/login", summary="Authenticate User", description="""
             Authenticate a user using email and password.
             
             Returns:

             - JWT access token
             - Token type

             Use the returned token to access protected endpoints.""")

def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return login_user_service(form_data=form_data, db=db)


@router.get("/me", summary="Get current User Profile", description="""
            Return information about the currently authenticated user.

            Requires:

            - Valid JWT token

            Returns:

            - User ID
            - Email
            - Role
            - Active status""")

def get_current_profile(current_user = Depends(get_current_user)):

    logger.info(f"PROFILE_ACCESSED | email={current_user['email']}")

    return {"email": current_user["email"], "username": current_user["username"],"role": current_user["role"]}


@router.get("/admin/dashboard", summary="Access Admin Dashboard", description="""
            Administrative endpoint.

            Requires:

            - Valid JWT
            - Admin role

            Non-admin users receive 403 Forbidden.""")

def admin_dashboard(current_user = Depends(RoleChecker(["admin"]))):

    return {"message": "Admin dashboard access granted","user": current_user}


@router.post("/validate-token", summary="Validate JWT Token", description="""
             Validate a JWT token.

             Used by external services to verify:

             - Token validity
             - User identity
             - User role
             - Account status

             Returns validation result and user information.""")

def validate_token(request: TokenValidationRequest):

    return validate_token_service(token=request.token)