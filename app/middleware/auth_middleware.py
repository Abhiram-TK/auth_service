from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.user import User

from app.services.jwt_service import (decode_access_token)

from app.core.logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    if not token:

        logger.warning("AUTHENTICATION FAILED | reason=missing_authorization_header")

        raise HTTPException(status_code=401, detail="Authorization token missing. Use Authorize and provide a valid JWT")

    payload = decode_access_token(token)

    if not payload:

        logger.error("JWT validation failed")

        raise HTTPException(status_code=401, detail="invalid or expired token")
    
    user_id = payload.get("user_id")

    user = (db.query(User).filter(User.id == user_id).first())

    if not user:

        logger.warning(f"AUTHENTICATION_FAILED | reason=user_not_found | user_id={user_id}")

        raise HTTPException(status_code=401, detail="User no longer exists")

    if not user.is_active:

        logger.warning(f"AUTHENTICATION_FAILED | reason=user_disabled | user_id={user.id}")

        raise HTTPException(status_code=401, detail="User account disabled")

    return payload