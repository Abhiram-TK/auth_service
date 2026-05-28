from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.models.role import Role

from app.schemas.auth_schema import RegisterRequest

from app.core.security import hash_password


router = APIRouter()

@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(User.email == request.email).first()

    if existing_email:

        raise HTTPException(status_code=400, detail="email already exists")

    existing_username = db.query(User).filter(User.username == request.username).first()

    if existing_username:

        raise HTTPException(status_code=400, detail="username already exists")

    default_role = db.query(Role).filter(Role.name == "viewer").first()

    if not default_role:

        default_role = Role(name="viewer")

        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    hashed_password = hash_password(request.password)

    new_user = User(email=request.email, username=request.username, password_hash=hashed_password, role_id=default_role.id, is_active=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "user created"}