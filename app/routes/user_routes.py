from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.user_schema import (UserResponse, RoleUpdateRequest)

from app.services.user_service import (get_all_users, get_user_by_id, update_user_role, deactivate_user)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def fetch_all_users(db: Session = Depends(get_db)):

    users = get_all_users(db)

    response = []

    for user in users:

        response.append({

            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.name,
            "is_active": user.is_active
        })

    return response

@router.get("/{user_id}")
def fetch_user(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id(user_id, db)

    return {

        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role.name,
        "is_active": user.is_active
    }

@router.put("/{user_id}/role")
def change_user_role(user_id: int, request: RoleUpdateRequest, db: Session = Depends(get_db)):

    user = update_user_role(user_id=user_id, role_name=request.role, db=db)

    return {

        "message": "Role updated successfully",
        "user_id": user.id,
        "new_role": user.role.name
    }


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    return deactivate_user(user_id=user_id, db=db)