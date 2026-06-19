from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.permission_schema import (PermissionCreateRequest, PermissionResponse)

from app.services.permission_service import (get_all_permissions, create_permission)
from app.services.permission_checker import PermissionChecker

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/", response_model=list[PermissionResponse], dependencies=[Depends(PermissionChecker(["view_permissions"]))],summary="Get All Permissions", description="""
            Retrieve all available permissions.

            Requires:

            - view_permissions permission
            
            Returns the permission catalog.""")

def fetch_permissions(db: Session = Depends(get_db)):

    return get_all_permissions(db)


@router.post("/", response_model=PermissionResponse, summary="Create Permission", dependencies=[Depends(PermissionChecker(["create_permissions"]))],description="""
             Create a new permission.

             Requires:

             - create_permissions permission

             Permission names must be unique.""")

def add_permission(request: PermissionCreateRequest, db: Session = Depends(get_db)):

    return create_permission(request=request, db=db)