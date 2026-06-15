from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.permission_schema import (PermissionCreateRequest, PermissionResponse)

from app.services.permission_service import (get_all_permissions, create_permission)
from app.services.rbac_service import RoleChecker

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/", response_model=list[PermissionResponse], summary="Get All Permissions", description="""
            Return all permissions in the system.

            Requires:

            - Valid JWT
            - Admin role""")

def fetch_permissions(db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):

    return get_all_permissions(db)


@router.post("/", response_model=PermissionResponse, summary="Create Permission", description="""
             Create a new permission.

             Requires:

             - Valid JWT
             - Admin role

             Permission names must be unique.""")

def add_permission(request: PermissionCreateRequest, db: Session = Depends(get_db), current_user = Depends(RoleChecker(["admin"]))):

    return create_permission(request=request, db=db)