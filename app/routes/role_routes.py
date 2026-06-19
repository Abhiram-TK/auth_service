from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.role_schema import (RoleCreateRequest, RoleResponse)

from app.services.role_service import (get_all_roles, create_role)

from app.services.permission_checker import PermissionChecker

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleResponse], summary="Get All Roles", dependencies=[Depends(PermissionChecker(["view_roles"]))], description="""
            Retrieve all available roles.

            Requires:

            - view_roles permission
            
            Returns role definition.""")

def fetch_roles(db: Session = Depends(get_db)):

    return get_all_roles(db)


@router.post("/", response_model=RoleResponse, summary="Create Role", dependencies=[Depends(PermissionChecker(["create_roles"]))], description="""
             Create a new role.

             Requires:

             - create_roles permission
             
             Role names must be unique.""")

def add_role(request: RoleCreateRequest, db: Session = Depends(get_db)):

    return create_role(name=request.name, description=request.description, db=db)