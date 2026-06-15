from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.role import Role

from app.core.logger import logger

def get_all_roles(db: Session):

    return db.query(Role).all()


def create_role(name: str, description: str, db: Session):

    existing_role = (db.query(Role).filter(Role.name == name).first())

    if existing_role:

        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(name=name, description=description)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    logger.info(f"ROLE_CREATED | id={new_role.id} | name={new_role.name}")

    return new_role