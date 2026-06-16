from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.role_schema import (RoleCreateRequest, RoleResponse)

from app.services.role_service import (get_all_roles, create_role)

from app.services.rbac_service import (RoleChecker)

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleResponse], summary="Get All Roles", dependencies=[Depends(RoleChecker(["admin"]))], description="""
            Retrieve all roles available in the system.

            Requires:

            - Valid JWT token
            - Admin role""")

def fetch_roles(db: Session = Depends(get_db)):

    return get_all_roles(db)


@router.post("/", response_model=RoleResponse, summary="Create Role", dependencies=[Depends(RoleChecker(["admin"]))], description="""
             Create a new role.

             Requires:

             - Valid JWT token
             - Admin role""")

def add_role(request: RoleCreateRequest, db: Session = Depends(get_db)):

    return create_role(name=request.name, description=request.description, db=db)