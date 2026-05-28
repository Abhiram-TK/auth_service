from fastapi import FastAPI

from app.database import engine, Base

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.core.security import (hash_password, verify_password)


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():

    password = "mypassword123"
    hashed_password = hash_password(password)
    verified = verify_password(password, hashed_password)

    return {"plain_password": password, "hashed_password": hashed_password, "verified": verified}