from fastapi import FastAPI
from app.database import engine, Base

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def test_connection():
    return {"message": "RBAC schema setup successful"}