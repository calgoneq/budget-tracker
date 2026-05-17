# Budget Tracker API

REST API for tracking personal expenses, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Stack

- **FastAPI** — REST API with Pydantic validation
- **SQLAlchemy ORM 2.0** — database models and session management
- **PostgreSQL** — persistent storage
- **Alembic** — database migrations
- **pytest + httpx** — integration tests with isolated test database

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/transactions` | List all transactions (optional `?kategoria=` filter) |
| GET | `/transactions/{id}` | Get transaction by ID |
| POST | `/transactions` | Add new transaction |
| DELETE | `/transactions/{id}` | Delete transaction |

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
createdb budget_tracker

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

## Running Tests

```bash
# Create test database first
createdb budget_test

pytest tests/
```

## Project Structure

```
├── main.py           # FastAPI app, routes
├── db.py             # SQLAlchemy database layer
├── models.py         # Pydantic request models
├── models_db.py      # SQLAlchemy ORM models
├── transaction.py    # Transaction domain class
├── exceptions.py     # Custom exceptions
├── filters.py        # Transaction filtering logic
├── migrations/       # Alembic migration files
└── tests/            # Integration tests
```

## Example Request

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"sklep": "Biedronka", "kwota": 45.50, "kategoria": "jedzenie", "data": "2026-05-17"}'
```
