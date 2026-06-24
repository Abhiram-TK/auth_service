# Authentication & Authorization Service

Authentication and Authorization Service built with FastAPI, PostgreSQL, JWT Authentication, and Permission-Based Access Control (PBAC).

This service acts as the central security layer for the portfolio ecosystem and is consumed by the Sales Transaction Service and Inventory Reservation & Dispatch System.

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
- Inventory Reservation & Dispatch System

Integration flow:

```text
Authentication Service
          │
          ▼
      JWT Token
          │
          ▼
Sales Transaction Service
          │
          ▼
Inventory Reservation &
Dispatch System
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
app/
├── core/
│   ├── config.py
│   ├── logger.py
│   └── security.py
│
├── database/
│   └── connection.py
│
├── models/
│   ├── user.py
│   ├── role.py
│   ├── permission.py
│   └── role_permission.py
│
├── schemas/
│   ├── user_schema.py
│   ├── role_schema.py
│   └── permission_schema.py
│
├── routes/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── role_routes.py
│   ├── permission_routes.py
│   └── role_permission_routes.py
│
├── services/
│   ├── auth_service.py
│   ├── jwt_service.py
│   ├── rbac_service.py
│   └── permission_checker.py
│
├── seed/
│   ├── seed_roles.py
│   ├── seed_permissions.py
│   └── seed_role_permissions.py
│
└── main.py
```

## Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/auth_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Start Application

```bash
uvicorn app.main:app --reload --port 8000
```

### Swagger UI

```text
http://localhost:8000/docs
```
