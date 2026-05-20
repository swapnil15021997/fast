# FastAPI Backend

Production-ready FastAPI backend scaffold with SQLAlchemy 2.0, MySQL, Redis, JWT auth, and AI integration.

## Tech Stack

- **FastAPI** — async web framework
- **SQLAlchemy 2.0** — async ORM
- **MySQL** — relational database
- **Alembic** — migrations
- **Redis** — caching
- **JWT** — authentication (access + refresh tokens)
- **OpenAI** — AI chat & embeddings
- **Pydantic v2** — validation
- **Pytest** — testing

## Project Structure

```
backend/
├── alembic/          # Migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── ai/           # OpenAI integration
│   ├── api/v1/       # API endpoints
│   ├── core/         # Config, security, dependencies
│   ├── db/           # Session, base, seed
│   ├── models/       # SQLAlchemy models
│   ├── redis/        # Redis connection & caching
│   ├── repositories/ # Data access layer
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── utils/        # Logging, helpers
├── tests/            # Pytest tests
├── .env.example
├── alembic.ini
├── pyproject.toml
└── README.md
```

## Setup

```bash
# Clone and enter the project
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .[dev]

# Copy environment config
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Seed the database
python -m app.db.seed

# Start the server
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Path                  | Description        |
|--------|-----------------------|--------------------|
| POST   | /api/v1/auth/register | Register a user    |
| POST   | /api/v1/auth/login    | Login              |
| POST   | /api/v1/auth/refresh  | Refresh token      |
| GET    | /api/v1/users/me      | Current user       |
| GET    | /api/v1/health        | Health check       |

## Curl Examples

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Str0ng!Pass","name":"Alice"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Str0ng!Pass"}'

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<refresh_token_value>"}'

# Get current user
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"

# Health check
curl http://localhost:8000/api/v1/health
```

## Testing

```bash
pytest -v --cov=app
```

## Environment Variables

See `.env.example` for all configurable variables.
