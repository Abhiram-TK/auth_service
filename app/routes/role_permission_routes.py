from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.services.permission_checker import PermissionChecker

from app.schemas.role_permission_schema import (AssignPermissionRequest, RolePermissionResponse)

from app.services.role_permission_service import (get_role_permissions, assign_permission_to_role, remove_permission_from_role)

router = APIRouter(tags=["Role Permissions"])

@router.get("/roles/{role_id}/permissions", summary="Get Role Permissions", dependencies=[Depends(PermissionChecker(["view_permissions"]))], description="""
            Retrieve permissions assigned to a role.

            Requires:

            - view_permissions permission
            
            Returns role-permission mappings.""", response_model=RolePermissionResponse)

def fetch_role_permissions(role_id: int, db: Session = Depends(get_db)):

    return get_role_permissions(role_id=role_id, db=db)


@router.post("/roles/{role_id}/permissions", summary="Assign Permission To Role", dependencies=[Depends(PermissionChecker(["assign_permissions"]))],description="""
             Assign a permission to a role.

             Requires:

             - assign_permissions permission
             
             Updates role access privileges.""")

def assign_permission(role_id: int, request: AssignPermissionRequest, db: Session = Depends(get_db)):

    return assign_permission_to_role(role_id=role_id, permission_name=request.permission, db=db)


@router.delete("/roles/{role_id}/permissions/{permission_name}", summary="Remove Permission From Role", dependencies=[Depends(PermissionChecker(["assign_permissions"]))],description="""
               Remove a permission from a role.
               
               Requires:
               
               - assign_permissions permission
               
               Updates role access privileges.""")

def remove_permission(role_id: int, permission_name: str, db: Session = Depends(get_db)):

    return remove_permission_from_role(role_id=role_id, permission_name=permission_name, db=db)