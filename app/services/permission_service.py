from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.permission import Permission

from app.schemas.permission_schema import PermissionCreateRequest

from app.core.logger import logger

def get_all_permissions(db: Session):

    return db.query(Permission).all()


def create_permission(request: PermissionCreateRequest, db: Session):

    existing_permission = (db.query(Permission).filter(Permission.name == request.name).first())

    if existing_permission:

        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = Permission(name=request.name, description=request.description)

    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    logger.info(f"PERMISSION_CREATED | id={new_permission.id} | name={new_permission.name}")

    return new_permission