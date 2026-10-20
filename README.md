# URL Shortener

A URL shortening service built with FastAPI, PostgreSQL, and Redis.

---

## Features

- Create short links for long URLs
- Redirect users to the original URLs
- User authentication with JWT
- Store link metadata in PostgreSQL
- Cache accessed links in Redis
- Run the application with Docker Compose

---

## Tech Stack

- Python 3.12
- FastAPI (async)
- PostgreSQL
- SQLAlchemy 2.0
- Redis
- Alembic
- Docker Compose
- Pytest

---

## Architecture

The application follows a layered architecture:

- `api/` - HTTP endpoints and request handling
- `services/` - business logic
- `db/` - database models and session management
- `core/` - application configuration and security
- `cache/` - Redis operations
- `schemas/` - Pydantic models
- `workers/` - worker synchronization
---

## Requirements

- Docker
- Docker Compose

---

## Installation

1. Clone the repository:

```bash
   git clone https://github.com/timur-dev-hub/shortener
   cd shortener
```

2. Create the environment file:

```bash
   cp .env.example .env
```

3. Configure the required environment variables in `.env`.

4. Start the application:

```bash
   docker compose up --build -d
```

---

## API Documentation

After starting the application, open:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Running Tests Locally

1. Create and activate a virtual environment:

```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   .venv\Scripts\activate         # Windows
```

2. Install dependencies:

```bash
   pip install -r requirements.txt
```

3. Create the test environment file:

```bash
   cp .env.test.example .env.test
```

4. Configure the required environment variables in `.env.test`.

5. Start the test services (test-postgres, test-redis):

```bash
   docker compose -f compose.test.yaml --env-file .env.test up -d
```

6. Run the tests:

```bash
   pytest -v
```

---

## Environment Variables

See `.env.example` for the list of required environment variables.

---

## License

This project is licensed under the MIT License.