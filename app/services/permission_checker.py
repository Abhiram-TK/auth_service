from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.middleware.auth_middleware import get_current_user

from app.models.user import User

from app.core.logger import logger


class PermissionChecker:

    def __init__(self, required_permissions: list):

        self.required_permissions = required_permissions

    def __call__(self, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

        user = (db.query(User).filter(User.id == current_user["user_id"]).first())

        if not user:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        user_permissions = {

            permission.name

            for permission in user.role.permissions

        }

        has_permission = any(

            permission in user_permissions

            for permission in self.required_permissions
    
        )

        if not has_permission:

            logger.warning(f"PERMISSION_DENIED | " f"user_id={user.id} | " f"role={user.role.name} | " f"required={self.required_permissions}")

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

        logger.info(f"PERMISSION_GRANTED | " f"user_id={user.id} | " f"role={user.role.name}")

        return current_user