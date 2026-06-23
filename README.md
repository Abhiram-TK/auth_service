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

## Integration

This service issues JWT tokens used by:

- Sales Transaction Service
- Inventory Reservation & Dispatch System

The token contains:

- User ID
- Username
- Role
- Permissions

allowing connected services to perform authorization without querying the authentication database.

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
