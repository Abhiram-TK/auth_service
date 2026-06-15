from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.user_schema import (UserResponse, RoleUpdateRequest)

from app.services.user_service import (get_all_users, get_user_by_id, update_user_role, deactivate_user)
from app.services.rbac_service import RoleChecker

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse],summary="Get All Users", dependencies=[Depends(RoleChecker(["admin"]))], description="""
            Retrieve all registered users.

            Requires:

            - Admin role

            Returns a list of users with role and account status.""")

def fetch_all_users(db: Session = Depends(get_db)):

    users = get_all_users(db)

    response = []

    for user in users:

        response.append({"id": user.id, "email": user.email, "username": user.username, "role": user.role.name, "is_active": user.is_active})

    return response


@router.get("/{user_id}", response_model=UserResponse,summary="Get User By ID", dependencies=[Depends(RoleChecker(["admin"]))], description="""
            Retrieve details for a specific user.

            Requires:

            - Admin role

            Returns user information if found.""")

def fetch_user(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id(user_id, db)

    return {"id": user.id, "email": user.email, "username": user.username, "role": user.role.name, "is_active": user.is_active}


@router.put("/{user_id}/role", summary="Change User Role", dependencies=[Depends(RoleChecker(["admin"]))], description="""
            Assign a new role to a user.

            Available roles:

            - viewer
            - recruiter
            - admin

            Administrators cannot modify their own role.""")

def change_user_role(user_id: int, request: RoleUpdateRequest, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):

    user = update_user_role(user_id=user_id, role_name=request.role, current_admin_id=current_user["user_id"], db=db)

    return {"message": "Role updated successfully", "user_id": user.id, "new_role": user.role.name}


@router.delete("/{user_id}", summary="Disable User Account", dependencies=[Depends(RoleChecker(["admin"]))], description="""
               Soft delete a user account.
               
               The account remains in the database but becomes inactive.
               
               Disabled users:
               
               - Cannot log in
               - Cannot access protected endpoints
               
               Administrators cannot disable their own account.""")

def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):

    return deactivate_user(user_id=user_id, current_admin_id=current_user["user_id"], db=db)