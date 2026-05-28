from fastapi import HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer

from app.services.jwt_service import (decode_access_token)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(status_code=401, detail="invalid or expired token")

    return payload