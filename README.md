# Project 1 - Authentication & Authorization Service

> Portfolio Project 1

Central authentication and authorization service for the Backend Transaction Ecosystem.

## Project Overview

The Authentication Service is the identity provider for the Backend Transaction Ecosystem.

Primary responsibilities:

- User registration
- User authentication
- JWT token generation
- Role-Based Access Control (RBAC)
- Permission management

The Authentication Service is the authoritative owner of:

- Users
- Roles
- Permissions

No downstream service owns or modifies this data directly.

This service must be started before all other services.

## Ecosystem Position

This service is the entry point of the backend ecosystem.

Startup Order

```text
      Authentication Service
                ↓
    Inventory Dispatch System
                ↓
    Sales Transaction Service
                ↓
  Reconciliation Automation Engine
```

Responsibilities

- Authentication
- Authorization
- JWT issuance
- Role Based Access Control
- Permission management

Consumed by

- Inventory Dispatch System
- Sales Transaction Service
- Reconciliation Automation Engine

## Backend Ecosystem

```text
              Backend Transaction Ecosystem

           Authentication Service (Project 1)
                       Port 8001
                           │
                           ▼
         Inventory Dispatch System (Project 2)
                       Port 8002
                           │
                           ▼
          Sales Transaction Service (Project 3)
                       Port 8003
                           │
                           ▼
      Reconciliation Automation Engine (Project 4)

Performance Optimization & Caching
(Project 5)
Cross-cutting service
```

## Recruiter Workflow Diagram

```text
    Clone Repository
            ↓
   Install Dependencies
            ↓
     Configure .env
            ↓
     Run Application
            ↓
Automatic Database Initialization
            ↓
  Automatic Seed Execution
            ↓
    Swagger Available
            ↓
        Test APIs
            ↓
    Integration Ready
```

## Features

- User Registration
- User Login
- JWT Access Token Generation
- Token Validation
- User Management
- Role Management
- Permission Management
- Role-Permission Assignment
- Permission-Based Authorization
- Protected Endpoints
- Swagger Documentation
- Automatic Database Initialization
- Automatic Seed Orchestration

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pydantic
- Passlib (bcrypt)
- Faker
- Uvicorn

## Authorization Model

Users are assigned a role.

Roles are assigned permissions.

Protected endpoints validate permissions from JWT claims using a Permission Checker.

```text
User
  ↓
Role
  ↓
Permissions
  ↓
Protected Endpoint
```

## Authentication Workflow

### Login Flow

```text
User Login
      ↓
Credentials Validated
      ↓
Role Retrieved
      ↓
Permissions Retrieved
      ↓
JWT Generated
      ↓
Token Returned
```

### Authorization Flow

```text
Client Request
      ↓
JWT Validation
      ↓
Permission Extraction
      ↓
Permission Checker
      ↓
Access Granted / Denied
```

## Integration

This service issues JWT tokens used by:

- Sales Transaction Service
- Inventory Dispatch System

Integration flow:

```text
Authentication Service
          │
          ▼
      JWT Token
          │
          ├──────────────► Inventory Dispatch System
          │
          └──────────────► Sales Transaction Service
```

The token contains:

- User ID
- Username
- Role
- Permissions

allowing connected services to perform authorization without querying the authentication database.

## API Modules

### Authentication

- POST `/register`
- POST `/login`
- POST `/validate-token`
- GET `/me`
- GET `/me/permissions`
- GET `/admin/dashboard`

### Users

- GET `/users`
- GET `/users/{user_id}`
- DELETE `/users/{user_id}`
- PUT `/users/{user_id}/role`

### Roles

- GET `/roles`
- POST `/roles`

### Permissions

- GET `/permissions`
- POST `/permissions`

### Role Permissions

- GET `/roles/{role_id}/permissions`
- POST `/roles/{role_id}/permissions`
- DELETE `/roles/{role_id}/permissions/{permission_name}`

## Seed Data

The project uses Faker to generate development and testing data.

Generated data includes:

- Users
- Roles
- Permissions
- Role-Permission Assignments

This enables realistic testing without manually creating records.

## Project Structure

```text
auth_service/

├── app
│   ├── core
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── database
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── seed.py
│   │   ├── seed_permissions.py
│   │   ├── seed_role_permissions.py
│   │   ├── seed_roles.py
│   │   └── seed_users.py
│   │
│   ├── middleware
│   │   └── auth_middleware.py
│   │
│   ├── models
│   │   ├── permission.py
│   │   ├── role.py
│   │   └── user.py
│   │
│   ├── routes
│   │   ├── auth_routes.py
│   │   ├── permission_routes.py
│   │   ├── role_permission_routes.py
│   │   ├── role_routes.py
│   │   └── user_routes.py
│   │
│   ├── schemas
│   │   ├── auth_schema.py
│   │   ├── permission_schema.py
│   │   ├── role_permission_schema.py
│   │   ├── role_schema.py
│   │   ├── token_schema.py
│   │   └── user_schema.py
│   │
│   ├── services
│   │   ├── auth_service.py
│   │   ├── jwt_service.py
│   │   ├── permission_checker.py
│   │   ├── permission_service.py
│   │   ├── rbac_service.py
│   │   ├── role_permission_service.py
│   │   ├── role_service.py
│   │   └── user_service.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Configuration

Configuration is managed through environment variables.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Copy `.env.example` to `.env` before running the application.

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/Abhiram-TK/auth_service.git
```

### Navigate into Project

```bash
cd auth_service
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy:

```text
.env.example
```

to

```text
.env
```

Update the values for your local environment.

### Seed Development Data

Database initialization is handled through the project's seed orchestrator.

The orchestrator executes all seed modules in the correct dependency order and inserts only missing records.

Seed execution includes:

- Roles
- Permissions
- Role-Permission Assignments
- Users

When the application starts, the database initialization process invokes the seed orchestrator automatically.

Manual execution (if required):

```bash
python app/database/seed.py
```

### Start API

```bash
uvicorn app.main:app --reload --port 8001
```

---

## Swagger UI

```text
http://127.0.0.1:8001/docs
```

Swagger provides:

- Interactive endpoint testing
- JWT authentication
- Request validation
- Response schemas

---

## Related Projects

| Service                            | Relationship                                  |
| ---------------------------------- | --------------------------------------------- |
| Inventory Dispatch System          | Consumes JWT authentication and authorization |
| Sales Transaction Service          | Consumes JWT authentication and authorization |
| Reconciliation Automation Engine   | Consumes JWT authentication and authorization |
| Performance Optimization & Caching | Future cross-cutting service                  |

---

## Current Status

Implemented

- User registration
- User authentication
- JWT generation
- JWT validation
- Permission-based authorization
- Role management
- Permission management
- Role-permission assignment
- Protected endpoints
- Swagger documentation
- Automatic database initialization
- Automatic seed orchestration

Next Phase

- Docker containerization
- Docker Compose deployment
