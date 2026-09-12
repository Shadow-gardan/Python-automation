# FastAPI Task Management REST API

A practical REST API for managing work tasks. This Project #3 portfolio piece demonstrates FastAPI backend development, RESTful CRUD operations, Pydantic validation, SQLAlchemy with SQLite, filtering, pagination, structured logging, automated testing, and generated API documentation.

## Why This Project Exists

Freelance clients frequently need a small, reliable service for tracking work items before investing in a larger product. This API provides that core workflow with a clean architecture that is easy to extend and straightforward to deploy on Ubuntu/Linux.

## Features

- Create, read, update, and delete tasks.
- Validate task titles, statuses, priorities, and dates.
- Filter tasks by `status` and `priority`.
- Paginate task lists with `skip` and `limit`.
- Persist tasks in SQLite through SQLAlchemy.
- Return clear 404 and 422 responses.
- Log startup, task mutations, and application events to `logs/app.log`.
- Provide interactive Swagger UI and ReDoc documentation.
- Test the API against an isolated temporary SQLite database.

## Technology Stack

Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, pytest, and HTTPX.

## Architecture

```text
HTTP request
    |
    v
FastAPI router and Pydantic schema validation
    |
    v
CRUD service functions
    |
    v
SQLAlchemy session and SQLite tasks table
    |
    v
Validated response model and application log
```

## Project Structure

```text
fastapi-task-manager/
├── app/
│   ├── config.py             # Environment-aware settings
│   ├── crud.py               # Database operations
│   ├── database.py           # Engine, sessions, and table initialization
│   ├── dependencies.py       # Shared FastAPI dependencies
│   ├── logging_config.py     # File and console logging
│   ├── main.py               # FastAPI application
│   ├── models.py             # SQLAlchemy Task model
│   ├── schemas.py            # Pydantic request/response models
│   └── routers/
│       ├── health.py         # Health endpoint
│       └── tasks.py          # Task CRUD endpoints
├── data/                     # Local SQLite data directory
├── logs/                     # Runtime logs
├── tests/                    # Isolated API tests
├── .env.example              # Configuration template
├── requirements.txt
└── README.md
```

## Database Design

The `tasks` table contains:

- `id`: primary key
- `title`: required task title
- `description`: optional details
- `status`: `pending`, `in_progress`, or `completed`
- `priority`: `low`, `medium`, or `high`
- `due_date`: optional timestamp
- `created_at` and `updated_at`: UTC timestamps

The default SQLite database is `data/tasks.db`, which is ignored by Git.

## Installation on Ubuntu/Linux

```bash
git clone <repository-url>
cd fastapi-task-manager
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

The application works without a `.env` file. Copy `.env.example` if you want to document local settings in your environment:

```bash
cp .env.example .env
```

Supported environment variables are `APP_NAME`, `DEBUG`, and `DATABASE_URL`. Do not commit `.env` or secrets.

## Run the API

From the project root:

```bash
uvicorn app.main:app --reload
```

Open these URLs while the server is running:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Check service health |
| GET | `/api/v1/tasks` | List tasks with filters and pagination |
| GET | `/api/v1/tasks/{task_id}` | Get one task |
| POST | `/api/v1/tasks` | Create a task |
| PUT | `/api/v1/tasks/{task_id}` | Update a task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

Task list query parameters:

- `status=pending`, `in_progress`, or `completed`
- `priority=low`, `medium`, or `high`
- `skip`: non-negative offset, default `0`
- `limit`: page size from `1` to `100`, default `20`

Example requests:

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Prepare proposal","priority":"high"}'

curl 'http://127.0.0.1:8000/api/v1/tasks?status=pending&limit=10'
```

A successful create response includes the generated ID and timestamps:

```json
{
  "id": 1,
  "title": "Prepare proposal",
  "description": null,
  "status": "pending",
  "priority": "high",
  "due_date": null,
  "created_at": "2026-09-12T12:00:00+00:00",
  "updated_at": "2026-09-12T12:00:00+00:00"
}
```

## Error Handling

- `404 Not Found` is returned when a task ID does not exist.
- `422 Unprocessable Entity` is returned for invalid JSON, status, priority, title, or pagination values.
- Internal database details are not exposed in normal API responses.

## Testing

Tests use FastAPI `TestClient` and a temporary SQLite database. They do not modify the default application database.

```bash
python -m pytest -v
```

## Safety

The project uses no authentication secrets, external APIs, shell commands, or destructive file operations. SQLAlchemy handles database parameters, `.env` and SQLite files are ignored by Git, and test fixtures isolate test data from production data.

## Future Improvements

- User accounts and authentication when the product requires them.
- PostgreSQL deployment configuration.
- Task labels and full-text search.
- Background reminders for due dates.
- Docker packaging and CI automation.
