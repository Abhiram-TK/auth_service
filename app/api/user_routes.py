from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.user_schema import (UserResponse, RoleUpdateRequest)

from app.services.user_service import (get_all_users, get_user_by_id, update_user_role, deactivate_user)
from app.services.permission_checker import PermissionChecker

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse],summary="Get All Users", dependencies=[Depends(PermissionChecker(["view_users"]))], description="""
            Retrieve all registered users.

            Requires:

            - view_users permission

            Returns a list of users with role and account status.""")

def fetch_all_users(db: Session = Depends(get_db)):

    users = get_all_users(db)

    response = []

    for user in users:

        response.append({"id": user.id, "first_name": user.first_name, "last_name": user.last_name,"email": user.email, "username": user.username, "role": user.role.name, "is_active": user.is_active})

    return response


@router.get("/{user_id}", response_model=UserResponse,summary="Get User By ID", dependencies=[Depends(PermissionChecker(["view_users"]))], description="""
            Retrieve details for a specific user.

            Requires:

            - view_users permission

            Returns user profile information.""")

def fetch_user(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id(user_id, db)

    return {"id": user.id, "first_name": user.first_name, "last_name": user.last_name,"email": user.email, "username": user.username, "role": user.role.name, 
            "is_active": user.is_active}


@router.put("/{user_id}/role", summary="Change User Role", description="""
            Assign a role to a user.

            Requires:
            
            - assign_roles permission
            
            Updates the user's assigned role.""")

def change_user_role(user_id: int, request: RoleUpdateRequest, db: Session = Depends(get_db), current_user = Depends(PermissionChecker(["assign_roles"]))):

    user = update_user_role(user_id=user_id, role_name=request.role, current_admin_id=current_user["user_id"], db=db)

    return {"message": "Role updated successfully", "user_id": user.id, "new_role": user.role.name}


@router.delete("/{user_id}", summary="Disable User Account", description="""
               Disable a user account.
               
               Requires:

               - disable_users permission
               
               Disabled users cannot access protected endpoints.""")

def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(PermissionChecker(["disable_users"]))):

    return deactivate_user(user_id=user_id, current_admin_id=current_user["user_id"], db=db)