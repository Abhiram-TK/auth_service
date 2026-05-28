from fastapi import FastAPI

from app.database import engine, Base

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.routes.auth_routes import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():

    return {"message": "Authentication service running"}

