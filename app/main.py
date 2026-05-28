from fastapi import FastAPI

from app.database import engine, Base

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.routes.auth_routes import router as auth_router

from app.services.jwt_service import (create_access_token, decode_access_token)


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():

    payload = {"sub": "user@test.com", "role": "admin"}

    token = create_access_token(payload)

    decoded = decode_access_token(token)

    return {"jwt_token": token, "decoded_payload": decoded}
