# API Documentation

Base URL: `http://localhost:8000/api/v1`

All request and response bodies use `Content-Type: application/json`.

---

## Health Check

### `GET /api/v1/health`

Check server status.

**Response `200 OK`**

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## Auth

### `POST /api/v1/auth/register`

Register a new user account.

**Request Body**

| Field    | Type   | Required | Description          |
| -------- | ------ | -------- | -------------------- |
| email    | string | ✅       | Valid email address  |
| password | string | ✅       | Plain-text password  |
| name     | string | ✅       | Display name         |

```json
{
  "email": "user@example.com",
  "password": "Str0ng!Pass",
  "name": "Alice"
}
```

**Response `201 Created`**

| Field          | Type   | Description                     |
| -------------- | ------ | ------------------------------- |
| access_token   | string | JWT access token (30 min)       |
| refresh_token  | string | JWT refresh token (7 days)      |
| token_type     | string | Always `"bearer"`               |

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error `409 Conflict`**

```json
{
  "detail": "Email already registered"
}
```

---

### `POST /api/v1/auth/login`

Authenticate with email and password.

**Request Body**

| Field    | Type   | Required | Description         |
| -------- | ------ | -------- | ------------------- |
| email    | string | ✅       | Registered email    |
| password | string | ✅       | Account password    |

```json
{
  "email": "user@example.com",
  "password": "Str0ng!Pass"
}
```

**Response `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error `401 Unauthorized`**

```json
{
  "detail": "Invalid email or password"
}
```

**Error `403 Forbidden`** (inactive account)

```json
{
  "detail": "Account is deactivated"
}
```

---

### `POST /api/v1/auth/refresh`

Exchange an existing refresh token for a new token pair. The old refresh token is revoked (one-time use).

**Request Body**

| Field         | Type   | Required | Description                      |
| ------------- | ------ | -------- | -------------------------------- |
| refresh_token | string | ✅       | Valid refresh token from `/login` or `/register` |

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error `401 Unauthorized`**

```json
{
  "detail": "Invalid or expired refresh token"
}
```

```json
{
  "detail": "Refresh token has been revoked"
}
```

---

## Users

### `GET /api/v1/users/me`

Get the currently authenticated user's profile.

**Headers**

| Name          | Value                  | Required |
| ------------- | ---------------------- | -------- |
| Authorization | `Bearer <access_token>` | ✅       |

**Response `200 OK`**

| Field        | Type   | Description                          |
| ------------ | ------ | ------------------------------------ |
| id           | string | UUID                                 |
| email        | string | User email                           |
| name         | string | Display name                         |
| is_active    | bool   | Account active flag                  |
| is_superuser | bool   | Admin privileges flag                |
| created_at   | string | ISO 8601 timestamp (with timezone)   |
| updated_at   | string | ISO 8601 timestamp (with timezone)   |

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "user@example.com",
  "name": "Alice",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-05-20T10:00:00+00:00",
  "updated_at": "2026-05-20T10:00:00+00:00"
}
```

**Error `401 Unauthorized`** (missing or invalid token)

```json
{
  "detail": "Invalid or expired access token"
}
```

**Error `404 Not Found`**

```json
{
  "detail": "User not found"
}
```

---

## Error Response Format

All errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

Standard HTTP status codes used:

| Code | Meaning              |
| ---- | -------------------- |
| 200  | Success              |
| 201  | Created              |
| 401  | Unauthorized         |
| 403  | Forbidden            |
| 404  | Not Found            |
| 409  | Conflict             |
| 422  | Validation Error     |
| 502  | Bad Gateway          |

---

## Authentication Flow (Frontend Integration)

```
1. Register or Login
   → Store access_token + refresh_token (localStorage / secure cookie)
   → access_token expires in 30 min

2. Authenticated requests
   → Attach header: Authorization: Bearer <access_token>

3. When access_token expires (401)
   → POST /api/v1/auth/refresh  { refresh_token: "<stored refresh>" }
   → Store new access_token + refresh_token (old refresh is revoked)
   → Retry original request

4. If refresh also fails
   → Redirect to login page
```

## Curl Examples

```bash
# Register
curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"Str0ng!Pass","name":"Alice"}' \
  | jq .

# Login
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"Str0ng!Pass"}' \
  | jq .

# Refresh
curl -s -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}' \
  | jq .

# Get current user
TOKEN="eyJ..."
curl -s http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

# Health check
curl -s http://localhost:8000/api/v1/health | jq .
```
