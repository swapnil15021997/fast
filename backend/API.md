# API Documentation

Base URL: `http://localhost:8000/api/v1`

All request and response bodies use `Content-Type: application/json` unless specified otherwise.

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

**Response `201 Created`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error `409 Conflict`** — Email already registered

---

### `POST /api/v1/auth/login`

**Request Body**

| Field    | Type   | Required | Description         |
| -------- | ------ | -------- | ------------------- |
| email    | string | ✅       | Registered email    |
| password | string | ✅       | Account password    |

**Response `200 OK`** — Same token payload as register

**Error `401 Unauthorized`** — Invalid email or password  
**Error `403 Forbidden`** — Account is deactivated

---

### `POST /api/v1/auth/refresh`

Exchange an existing refresh token for a new token pair.

**Request Body**

| Field         | Type   | Required | Description                    |
| ------------- | ------ | -------- | ------------------------------ |
| refresh_token | string | ✅       | Valid refresh token from login |

**Response `200 OK`** — New token pair (old refresh is revoked)

---

## Users

### `GET /api/v1/users/me`

Get the currently authenticated user's profile.

**Headers:** `Authorization: Bearer <access_token>`

**Response `200 OK`**

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

---

## Flows

A flow is a container that holds guided questions, files, and chat sessions.

### `POST /api/v1/flows`

Create a new flow.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body**

| Field     | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| flow_name | string | ✅       | Name of the flow |

**Response `201 Created`**

```json
{
  "flow_id": "uuid",
  "flow_name": "My Flow",
  "flow_user_id": "uuid",
  "flow_is_delete": false,
  "is_public": false,
  "public_token": null,
  "created_at": "2026-05-20T10:00:00+00:00",
  "updated_at": "2026-05-20T10:00:00+00:00"
}
```

### `GET /api/v1/flows`

List all flows for the authenticated user (non-deleted).

**Response `200 OK`** — Array of FlowResponse

### `GET /api/v1/flows/{flow_id}`

Get a single flow by ID.

**Response `200 OK`** — FlowResponse  
**Error `404 Not Found`**

### `PATCH /api/v1/flows/{flow_id}`

Update a flow name.

**Request Body**

| Field     | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| flow_name | string | ❌       | New flow name  |

**Response `200 OK`** — Updated FlowResponse

### `DELETE /api/v1/flows/{flow_id}`

Soft-delete a flow.

**Response `204 No Content`**

---

## Questions

Questions are hierarchical (parent-child) and belong to a flow. The last question in a flow triggers AI processing with file attachments.

### `POST /api/v1/flows/{flow_id}/questions`

Create a new question in a flow.

**Request Body**

| Field              | Type    | Required | Description                          |
| ------------------ | ------- | -------- | ------------------------------------ |
| question_text      | string  | ✅       | The question text                    |
| question_is_last   | boolean | ❌       | Marks as final question (default false) |
| question_parent_id | string  | ❌       | UUID of parent question (for branching) |

**Response `201 Created`**

```json
{
  "question_id": "uuid",
  "question_text": "What is your goal?",
  "question_is_last": false,
  "question_parent_id": null,
  "question_is_delete": false,
  "question_flow_id": "uuid",
  "created_at": "2026-05-20T10:00:00+00:00",
  "updated_at": "2026-05-20T10:00:00+00:00"
}
```

### `GET /api/v1/flows/{flow_id}/questions`

List all non-deleted questions in a flow, ordered by creation.

**Response `200 OK`** — Array of QuestionResponse

### `GET /api/v1/questions/{question_id}`

Get a single question.

### `PATCH /api/v1/questions/{question_id}`

Update question fields.

**Request Body** (all optional)

| Field              | Type    | Description               |
| ------------------ | ------- | ------------------------- |
| question_text      | string  | New text                  |
| question_is_last   | boolean | Mark as last question     |
| question_is_delete | boolean | Soft-delete the question  |

### `DELETE /api/v1/questions/{question_id}`

Soft-delete a question.

**Response `204 No Content`**

---

## Files

Files are attached to flows and sent to AI when the last question is answered.

### `POST /api/v1/flows/{flow_id}/files`

Upload a file to a flow.

**Headers:** `Authorization: Bearer <access_token>`
**Content-Type:** `multipart/form-data`

| Field | Type   | Required | Description    |
| ----- | ------ | -------- | -------------- |
| file  | binary | ✅       | File to upload |

**Response `201 Created`**

```json
{
  "file_id": "uuid",
  "flow_file_id": "uuid",
  "file_path": "uploads/{flow_id}/{stored_name}",
  "file_name": "document.pdf",
  "file_size": 12345,
  "file_type": "application/pdf",
  "created_at": "2026-05-20T10:00:00+00:00",
  "updated_at": "2026-05-20T10:00:00+00:00"
}
```

### `GET /api/v1/flows/{flow_id}/files`

List all files in a flow.

### `DELETE /api/v1/files/{file_id}`

Delete a file record.

**Response `204 No Content`**

---

## AI Models

### `GET /api/v1/ai-models`

List available AI models.

**Response `200 OK`**

```json
[
  {
    "ai_id": "uuid",
    "ai_name": "gpt-4o"
  },
  {
    "ai_id": "uuid",
    "ai_name": "gpt-4o-mini"
  }
]
```

---

## Token Usage & Rate Limiting

Each user has a token quota per period (default: 100,000 tokens per 30 days). Tokens are consumed when AI processes the final question in a flow.

### `GET /api/v1/tokens/usage`

Get current token usage for the authenticated user.

**Response `200 OK`**

```json
{
  "tokens_used": 1500,
  "tokens_limit": 100000,
  "tokens_remaining": 98500,
  "period_start": "2026-05-20",
  "period_end": "2026-06-19"
}
```

**Error `429 Too Many Requests`** — Token quota exhausted

---

## Chats

Chats store conversations between the user and AI. Each chat belongs to a flow.

### `POST /api/v1/chats`

Create a new chat session.

**Request Body**

| Field   | Type   | Required | Description        |
| ------- | ------ | -------- | ------------------ |
| flow_id | string | ✅       | Parent flow ID     |
| title   | string | ❌       | Chat title (optional) |

**Response `201 Created`**

```json
{
  "id": "uuid",
  "flow_id": "uuid",
  "user_id": "uuid",
  "title": "",
  "created_at": "2026-05-20T10:00:00+00:00",
  "updated_at": "2026-05-20T10:00:00+00:00"
}
```

### `GET /api/v1/chats`

List all chats for the authenticated user.

### `GET /api/v1/chats/{chat_id}`

Get chat details with all messages.

**Response `200 OK`**

```json
{
  "id": "uuid",
  "flow_id": "uuid",
  "user_id": "uuid",
  "title": "",
  "created_at": "...",
  "updated_at": "...",
  "messages": [
    {
      "id": "uuid",
      "chat_id": "uuid",
      "role": "user",
      "content": "Hello",
      "created_at": "2026-05-20T10:00:00.123+00:00"
    },
    {
      "id": "uuid",
      "chat_id": "uuid",
      "role": "assistant",
      "content": "Hi! How can I help?",
      "created_at": "2026-05-20T10:00:01.456+00:00"
    }
  ]
}
```

### `POST /api/v1/chats/{chat_id}/messages`

Add a message to a chat.

**Request Body**

| Field   | Type   | Required | Description              |
| ------- | ------ | -------- | ------------------------ |
| role    | string | ✅       | `"user"` or `"assistant"` |
| content | string | ✅       | Message content          |

### `GET /api/v1/chats/{chat_id}/messages`

Get all messages in a chat.

---

## Public Sharing

Flows can be shared publicly via a unique token URL. Public endpoints do **not** require authentication.

### `POST /api/v1/flows/{flow_id}/share`

Enable public sharing for a flow. Generates a unique public token.

**Headers:** `Authorization: Bearer <access_token>`

**Response `200 OK`**

```json
{
  "public_token": "uuid-v4-token",
  "share_url": "http://localhost:8000/api/v1/public/share/{public_token}"
}
```

### `DELETE /api/v1/flows/{flow_id}/share`

Disable public sharing (removes the token).

**Response `200 OK`** — Updated FlowResponse (public_token becomes null)

### `GET /api/v1/public/share/{public_token}`

Access a publicly shared flow. **No authentication required.**

**Response `200 OK`**

```json
{
  "flow_id": "uuid",
  "flow_name": "My Public Flow",
  "created_at": "2026-05-20T10:00:00+00:00"
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
| 204  | No Content           |
| 401  | Unauthorized         |
| 403  | Forbidden            |
| 404  | Not Found            |
| 409  | Conflict             |
| 422  | Validation Error     |
| 429  | Too Many Requests    |
| 502  | Bad Gateway          |

---

## Complete Endpoint Summary

| Method   | Path                                    | Auth | Description                |
| -------- | --------------------------------------- | ---- | -------------------------- |
| GET      | /api/v1/health                          | No   | Health check               |
| POST     | /api/v1/auth/register                   | No   | Register user              |
| POST     | /api/v1/auth/login                      | No   | Login                      |
| POST     | /api/v1/auth/refresh                    | No   | Refresh tokens             |
| GET      | /api/v1/users/me                        | Yes  | Current user profile       |
| POST     | /api/v1/flows                           | Yes  | Create flow                |
| GET      | /api/v1/flows                           | Yes  | List flows                 |
| GET      | /api/v1/flows/{flow_id}                 | Yes  | Get flow                   |
| PATCH    | /api/v1/flows/{flow_id}                 | Yes  | Update flow                |
| DELETE   | /api/v1/flows/{flow_id}                 | Yes  | Soft-delete flow           |
| POST     | /api/v1/flows/{flow_id}/questions       | Yes  | Create question            |
| GET      | /api/v1/flows/{flow_id}/questions       | Yes  | List questions             |
| GET      | /api/v1/questions/{question_id}         | Yes  | Get question               |
| PATCH    | /api/v1/questions/{question_id}         | Yes  | Update question            |
| DELETE   | /api/v1/questions/{question_id}         | Yes  | Soft-delete question       |
| POST     | /api/v1/flows/{flow_id}/files           | Yes  | Upload file                |
| GET      | /api/v1/flows/{flow_id}/files           | Yes  | List files                 |
| DELETE   | /api/v1/files/{file_id}                 | Yes  | Delete file                |
| GET      | /api/v1/ai-models                       | No   | List AI models             |
| GET      | /api/v1/tokens/usage                    | Yes  | Get token usage            |
| POST     | /api/v1/chats                           | Yes  | Create chat                |
| GET      | /api/v1/chats                           | Yes  | List chats                 |
| GET      | /api/v1/chats/{chat_id}                 | Yes  | Get chat with messages     |
| POST     | /api/v1/chats/{chat_id}/messages        | Yes  | Add chat message           |
| GET      | /api/v1/chats/{chat_id}/messages        | Yes  | Get chat messages          |
| POST     | /api/v1/flows/{flow_id}/share           | Yes  | Enable public sharing      |
| DELETE   | /api/v1/flows/{flow_id}/share           | Yes  | Disable public sharing     |
| GET      | /api/v1/public/share/{public_token}     | No   | Access shared flow         |

---

## Optimized Queries

- **Flow list**: Single `SELECT` with `WHERE user_id` and `is_delete=False`, ordered by `created_at DESC` — no joins.
- **Questions by flow**: Single `SELECT` with `WHERE flow_id` and `is_delete=False`, ordered by `created_at ASC` — indexed on `question_flow_id`.
- **Chat detail**: Eager-loaded (`joinedload`) messages in a single query to avoid N+1.
- **Public flow lookup**: Indexed lookup on `public_token` with `is_public=True` and `is_delete=False`.
- **Token usage**: Upsert pattern — `SELECT` then `INSERT` if not found, avoiding race conditions.
- **Soft deletes**: All destructive operations use `is_delete` flags; records are never physically removed.

---

## Authentication Flow

```
1. Register or Login → store access_token + refresh_token
2. Attach header: Authorization: Bearer <access_token>
3. On 401 → POST /auth/refresh with stored refresh_token
4. If refresh also fails → redirect to login
```
