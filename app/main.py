from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from app.database.connection import engine, Base, SessionLocal
from app.database.seed import run_all_seeds

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.api.role_routes import router as role_router
from app.api.permission_routes import router as permission_router
from app.api.role_permission_routes import router as role_permission_router

from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the application before serving requests.
    """

    logger.info("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Running database seed orchestrator...")

    run_all_seeds()

    logger.info("Authentication service startup completed.")

    yield

    logger.info("Authentication service shutting down...")

tags_metadata = [
    
    {"name": "System", "description": "Service information and health monitoring."},

    {"name": "Authentication", "description": "User registration, login, JWT generation and token validation."},

    {"name": "Users", "description": "User administration and account management."},
    
    {"name": "Roles", "description": "Role creation and RBAC role management."},
    
    {"name": "Permissions", "description": "Permission catalog management."},
    
    {"name": "Role Permissions", "description": "Role-to-permission assignment and RBAC relationship management."}
    
]

app = FastAPI(title="Authentication and Authorization Service", version="1.0.0", description=
              """Centralized authentication and authorization platform.

              Provides user authentication, JWT token management, role-based access control (RBAC), permission management, 
              and identity services for connected backend applications.

              Integrated Services:
              - Transaction Processing API
              - Inventory Reservation API""", openapi_tags=tags_metadata, lifespan=lifespan, 
              contact={"name": "Abhiram TK", "url": "https://github.com/Abhiram-TK", "email": "abhiramtksuresh@example.com"})

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:8002",
                                  "http://localhost:8002",
                                  "http://127.0.0.1:8003",
                                  "http://localhost:8003"],
                   allow_credentials=False,
                   allow_methods=["POST"],
                   allow_headers=["Content-Type"])

logger.info("Authentication service started")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(role_permission_router)

@app.get("/", tags=["System"], summary="Service Information")
def home():

    return {"message": "Authentication and Authorization service running"}

@app.get("/health", tags=["System"], summary="Health Check", description="""
         Verify service availability and database connectivity.

         Used by:

         - Docker health checks
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