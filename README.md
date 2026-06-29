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
auth_service/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── permission.py
│   │   └── role_permission.py
│   │
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── seed/
│   └── main.py
│
├── logs/
├── .env.example
├── requirements.txt
└── README.md
```

## Run Locally

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

### Seed Development Data

Populate the database with sample users, roles, permissions, and role-permission assignments.

```bash
python app/database/seed_users.py
```

```bash
python app/database/seed_roles.py
```

```bash
python app/database/seed_permissions.py
```

```bash
python app/database/seed_role_permissions.py
```

### Start Application

```bash
uvicorn app.main:app --reload --port 8000
```

### Swagger UI

```text
http://127.0.1:8000/docs
```

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

Next Phase

- Docker containerization
- Docker Compose deployment
