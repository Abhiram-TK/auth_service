from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.jwt_service import (decode_access_token)

from app.core.logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_current_user(token: str | None = Depends(oauth2_scheme)):

    if not token:

        logger.warning("AUTHENTICATION FAILED | reason=missing_authorization_header")

        raise HTTPException(status_code=401, detail="Authorization token missing. Use Authorize and provide a valid JWT")

    payload = decode_access_token(token)

    if not payload:

        logger.error("JWT validation failed")

        raise HTTPException(status_code=401, detail="invalid or expired token")

    return payload