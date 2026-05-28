from fastapi import HTTPException, Depends

from app.middleware.auth_middleware import (get_current_user)


class RoleChecker:

    def __init__(self, allowed_roles: list):

        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)):

        user_role = current_user.get("role")

        if user_role not in self.allowed_roles:

            raise HTTPException(status_code=403, detail="forbidden")

        return current_user