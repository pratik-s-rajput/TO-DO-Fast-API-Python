## Purpose
Brief, actionable guidance for AI coding assistants working in this repository.

## Big picture
- **Frameworks:** FastAPI (ASGI) + SQLAlchemy (async). App entry: [app/main.py](app/main.py#L1).
- **Runtime flow:** app starts in `app/main.py`; on startup it runs a simple DB check (`SELECT 1`) to verify connectivity.
- **DB layer:** async SQLAlchemy engine and session factory live in [app/db/session.py](app/db/session.py#L1-L20). DB sessions are provided via `get_db` in [app/db/deps.py](app/db/deps.py#L1-L20).

## Key files to reference
- [app/main.py](app/main.py#L1) — FastAPI app and startup health check.
- [app/core/config.py](app/core/config.py#L1-L20) — `Settings` (Pydantic `BaseSettings`) and `.env` usage.
- [app/db/session.py](app/db/session.py#L1-L50) — `engine`, `AsyncSessionLocal` configuration (note: `echo=True` by default).
- [app/db/deps.py](app/db/deps.py#L1-L20) — `get_db` dependency generator.
- `app/models/` and `app/schemas/` — expected locations for ORM models and Pydantic schemas (currently empty).

## Run & debug (developer workflows)
- Start the dev server: `uvicorn app.main:app --reload` from repo root.
- The app reads environment variables using Pydantic `BaseSettings` and will load `.env` from the repo root (see [app/core/config.py](app/core/config.py#L1-L20)).
- Provide a proper async-compatible DATABASE_URL in `.env`. Example:

  DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/todo_db

- The startup event in `app/main.py` executes a quick `SELECT 1` against the engine; fix or update this check if you change connection semantics.
- To reduce noise in logs set `echo=False` in [app/db/session.py](app/db/session.py#L1-L20).

## Project-specific patterns & conventions
- Use the `AsyncSessionLocal` factory from [app/db/session.py](app/db/session.py#L1-L20) for async DB work; endpoints should receive sessions via `Depends(get_db)` (see [app/db/deps.py](app/db/deps.py#L1-L20)).
- Keep ORM models in `app/models/` and Pydantic request/response schemas in `app/schemas/`.
- Configuration values are centralized in `app/core/config.py` and loaded from `.env`; do not hardcode secrets in code.

## Integration points & assumptions
- The code expects an async-capable DB driver. If you see `create_async_engine`, assume URLs must use an async dialect (e.g., `postgresql+asyncpg://`).
- No migration tool is present in the repository; if adding DB migrations, document chosen tool and its command in repo README.

## When editing code — quick examples
- Create an endpoint that uses DB session:

```py
from fastapi import Depends
from app.db.deps import get_db

async def endpoint(db=Depends(get_db)):
    async with db as session:
        ...
```

## Notes / todo for humans
- `app/core/config.py` currently contains an invalid `DATABASE_URL` assignment pattern; ensure `Settings` uses proper typed fields and values in `.env`.
- `app/models/` and `app/schemas/` are empty — add examples if you want the AI to scaffold endpoints.

If anything above is unclear or you'd like more examples (typical CRUD endpoint, migration setup, or test commands), tell me which area to expand.
