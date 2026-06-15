from fastapi import FastAPI

from sqlalchemy import text

from app.database.connection import engine, Base, SessionLocal

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.role_routes import router as role_router

from app.core.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication Service", description="""
              Authentication and Authorization Service.

              Features:

              - User Registration
              - User Authentication
              - JWT Token Management
              - Role-Based Access Control (RBAC)
              - User Management
              - Token Validation
              
              Used by:
              
              - Project 1 Transaction Processing API
              - Project 4 Inventory Reservation API""", version="1.0.0")

logger.info("Auth service started")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)

@app.get("/", tags=["System"], summary="Home")
def home():

    return {"message": "Authentication service running"}

@app.get("/health", tags=["System"], summary="Health Check", description="""
         Verify service availability and database connectivity.

         Used by:

         - Docker health checks
         - Kubernetes readiness probes
         - Monitoring systems""")

def health_check():

    db = SessionLocal()

    try:

        db.execute(text("SELECT 1"))

        return {"status": "healthy", "database": "connected"}

    except Exception:

        return {"status": "unhealthy", "database": "disconnected"}

    finally:

        db.close()