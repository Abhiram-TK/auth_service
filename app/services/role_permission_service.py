from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission

from app.core.logger import logger

def get_role_permissions(role_id: int, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:

        raise HTTPException(status_code=404, detail="Role not found")

    return {"role": role.name,"permissions":
            [permission.name
             for permission in role.permissions]}


def assign_permission_to_role(role_id: int, permission_name: str, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:

        raise HTTPException(status_code=404, detail="Role not found")

    permission = (db.query(Permission).filter(Permission.name == permission_name).first())

    if not permission:

        raise HTTPException(status_code=404, detail="Permission not found")

    if permission in role.permissions:

        raise HTTPException(status_code=400, detail="Permission already assigned")

    role.permissions.append(permission)

    db.commit()

    logger.info(f"PERMISSION_ASSIGNED_TO_ROLE | role={role.name} | permission={permission.name}")

    return {"message": "Permission assigned successfully"}


def remove_permission_from_role(role_id: int, permission_name: str, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:

        raise HTTPException(status_code=404, detail="Role not found")

    permission = (db.query(Permission).filter(Permission.name == permission_name).first())

    if not permission:

        raise HTTPException(status_code=404, detail="Permission not found")

    if permission in role.permissions:

        role.permissions.remove(permission)

    db.commit()

    logger.info(f"PERMISSION_REMOVED_FROM_ROLE | role={role.name} | permission={permission.name}")

    return {"message": "Permission removed successfully"}