from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.services.rbac_service import RoleChecker

from app.schemas.role_permission_schema import (AssignPermissionRequest, RolePermissionResponse)

from app.services.role_permission_service import (get_role_permissions, assign_permission_to_role, remove_permission_from_role)

router = APIRouter(tags=["Role Permissions Management"])

@router.get("/roles/{role_id}/permissions", summary="Get Role Permissions", description="""
            Retrieve all permissions assigned to a role.

            Requires:

            - Valid JWT
            - Admin role""", response_model=RolePermissionResponse)

def fetch_role_permissions(role_id: int, db: Session = Depends(get_db), current_user=Depends(RoleChecker(["admin"]))):

    return get_role_permissions(role_id=role_id, db=db)


@router.post("/roles/{role_id}/permissions", summary="Assign Permission To Role", description="""
             Assign a permission to a role.

             Requires:

             - Valid JWT
             - Admin role""")

def assign_permission(role_id: int, request: AssignPermissionRequest, db: Session = Depends(get_db), current_user=Depends(RoleChecker(["admin"]))):

    return assign_permission_to_role(role_id=role_id, permission_name=request.permission, db=db)


@router.delete("/roles/{role_id}/permissions/{permission_name}", summary="Remove Permission From Role", description="""
               Remove a permission from a role.
               
               Requires:
               
               - Valid JWT
               - Admin role""")

def remove_permission(role_id: int, permission_name: str, db: Session = Depends(get_db), current_user=Depends(RoleChecker(["admin"]))):

    return remove_permission_from_role(role_id=role_id, permission_name=permission_name, db=db)