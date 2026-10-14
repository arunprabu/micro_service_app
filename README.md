# BFSI Account Service

A small **FastAPI + SQLite** microservice used as a course project. It is a ready-to-run skeleton for one banking use case with two features:

| # | Feature | Endpoint | Status |
|---|---|---|---|
| 1 | Mini statement | `GET /api/v1/accounts/{account_number}/mini-statement` | wired, returns `501` until you build it |
| 2 | Minimum balance check | `GET /api/v1/accounts/{account_number}/minimum-balance-check` | wired, returns `501` until you build it |

You will build both features yourself using **GitHub Spec Kit** (Spec-Driven Development). See [Build the features with Spec Kit](#build-the-features-with-spec-kit).

**Stack:** Python 3.12 · FastAPI · SQLAlchemy 2 · SQLite · pydantic-settings · pytest · ruff · [uv](https://docs.astral.sh/uv/)

## Quick start

Prerequisite: [install uv](https://docs.astral.sh/uv/getting-started/installation/). uv will fetch Python 3.12 if you don't have it.

```bash
uv sync                                  # create .venv and install dependencies
uv run python -m app.db.seed             # create ./data/bank.db with sample data
uv run uvicorn app.main:app --reload     # start the API
```

Open <http://127.0.0.1:8000/docs> for the interactive Swagger UI, or check the service:

```bash
curl http://127.0.0.1:8000/health
```

If port 8000 is busy, add `--port 8001` (or any free port) to the uvicorn command.

```bash
uv run pytest            # run tests
uv run ruff check .      # lint
uv run ruff format .     # format
```

Settings come from environment variables or a `.env` file. See [.env.example](./.env.example).

## How a request flows

```text
HTTP request
   │
   ▼
Router        app/api/v1/*.py        parse input, call a service, return the response (no business logic)
   │  Depends()  (wired in app/api/deps.py)
   ▼
Service       app/services/*.py      business rules (no HTTP, no SQL)
   │
   ▼
Repository    app/repositories/*.py  all database queries
   │
   ▼
Models        app/models/*.py        SQLAlchemy tables  →  SQLite file (data/bank.db)
```

Errors: services raise an `AppError` subclass ([app/core/exceptions.py](./app/core/exceptions.py)). One handler turns it into `{"error": {"code": "...", "message": "..."}}` with the right HTTP status.

## Project layout

```text
app/
├── main.py              app factory: routers, error handler, DB init at startup
├── core/                config (settings) and exceptions
├── db/                  engine + session, Base, seed script
├── models/              Account, Transaction (SQLAlchemy)
├── schemas/             Pydantic request/response models  (empty: you add them)
├── repositories/        database access
├── services/            business logic                     (placeholders: you build them)
└── api/
    ├── deps.py          dependency wiring (session → repository → service)
    ├── health.py        GET /health
    └── v1/              versioned routes (mounted under /api/v1)
tests/                   pytest, using an in-memory SQLite database
docs/features/           the two Spec Kit feature guides
```

## Sample data

Created by `uv run python -m app.db.seed` (safe to run again; it does nothing if data exists). Amounts in rupees:

| Account | Holder | Type | Balance | Minimum | Case it demonstrates |
|---|---|---|---|---|---|
| `1000000001` | Asha Verma | SAVINGS | 25,152.00 | 5,000.00 | healthy, 13 transactions |
| `1000000002` | Rohan Mehta | SAVINGS | 4,500.00 | 5,000.00 | **below** the minimum |
| `1000000003` | Kiran Traders | CURRENT | 10,000.00 | 10,000.00 | **exactly at** the minimum |

To start over, delete the `data/` folder and seed again.

## Conventions

- **Money is never a float.** The database stores integer **paise** (`balance_paise`, `amount_paise`; 1 rupee = 100 paise). Convert to `Decimal` rupees at the service/API boundary.
- **Keep layers honest:** routers have no business logic, services have no SQL, repositories have no business rules.
- **No migrations:** tables are created automatically at startup (`create_all`). If you change a model, delete `data/bank.db` and seed again.
- **Tests never touch `data/bank.db`.** They use the `client` and `db_session` fixtures in [tests/conftest.py](./tests/conftest.py).
- `TODO(feature-01)` / `TODO(feature-02)` comments mark exactly where each feature plugs in.

## Build the features with Spec Kit

[Spec Kit](https://github.com/github/spec-kit) turns *what you want* into a spec, then a plan, then tasks, then code, with the AI agent doing the typing and you reviewing each step.

### One-time setup

Spec Kit needs Python 3.11+ and uv (you already have both). In this project folder:

```bash
git init                                              # Spec Kit works best inside a git repo
uv tool install specify-cli                           # install the Spec Kit CLI once per machine
specify init --here --force --integration copilot     # add Spec Kit files to this project
```

`--force` is needed because the folder already has files. Optionally run `specify extension add git` if you want Spec Kit to create a branch per feature.

Now open the folder in VS Code and use the **GitHub Copilot Chat** agent. Spec Kit commands are chat skills like `/speckit-specify`; they are not terminal commands.

Run the constitution **once** for the whole project:

```text
/speckit-constitution Create principles for this FastAPI and SQLite learning project:
1. Keep it simple and readable for junior engineers; prefer the plain, obvious solution and add no new dependencies without a stated reason.
2. Layered architecture: routers only handle HTTP, services hold business rules, repositories hold all SQL. Do not skip or mix layers.
3. Money is stored as integer paise and handled as Decimal in code; never use float for money.
4. Test-first with pytest: every endpoint has tests for the happy path, not found, and invalid input. Tests use the in-memory fixtures in tests/conftest.py and never touch data/bank.db.
5. Quality gate: `uv run ruff check .` and `uv run pytest` must both pass before any task is considered done.
6. Errors are raised as AppError subclasses and returned as {"error": {"code", "message"}}.
7. Read-only features must never modify the database.
```

### Then build each feature

Follow the guide for each one. They are independent, so build them in either order (01 first is recommended).

1. [Feature 01: Mini statement](./docs/features/01-mini-statement.md)
2. [Feature 02: Minimum balance check](./docs/features/02-minimum-balance-check.md)

Each guide has the same flow: `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement` → `/speckit-converge`, with ready-to-paste prompts and a definition-of-done checklist. The design decisions are yours to make along the way.
