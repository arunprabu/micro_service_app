# Feature 01 — Mini Statement

> **Goal:** build the mini statement endpoint using **GitHub Spec Kit (Spec-Driven Development)**.
> Describe *what and why* first, then let the workflow take you through the plan, tasks and code. **Do not hand-write the feature.**
> Review the output of each step before moving on.

**Before you start:** complete the one-time setup in the [README](../../README.md#build-the-features-with-spec-kit) (install `specify`, `specify init`, constitution) and make sure `uv run pytest` is green.

Paste the prompts below into the Copilot Chat agent **one at a time** (Copilot uses the `/speckit-*` syntax).

---

## 1. The business use case

A customer, or a support officer helping them, gives an **account number** and instantly sees the **most recent transactions**, like the mini statement on an ATM slip or a banking app home screen.

## 2. What the skeleton already gives you

| Piece | Where | State |
|---|---|---|
| Route | [app/api/v1/statements.py](../../app/api/v1/statements.py) | `GET /api/v1/accounts/{account_number}/mini-statement` is wired and returns `501` |
| Service | [app/services/statement_service.py](../../app/services/statement_service.py) | placeholder that raises `FeatureNotImplementedError` |
| Repositories | [app/repositories/](../../app/repositories) | `AccountRepository.get_by_account_number` exists; `TransactionRepository` is empty |
| Schemas | [app/schemas/](../../app/schemas) | empty |
| Errors | [app/core/exceptions.py](../../app/core/exceptions.py) | `AccountNotFoundError` (404) is ready to use |
| Data | `Account` and `Transaction` models, [seed data](../../app/db/seed.py) | 3 accounts with sample transactions |
| Tests | [tests/conftest.py](../../tests/conftest.py) | `client` and `db_session` fixtures (in-memory SQLite) |

---

## 3. Run the Spec Kit workflow

### Step 1 — Specify (what and why, no tech)

```text
/speckit-specify Build a mini statement feature for a retail bank's account service.

A customer, or a support officer on their behalf, provides an account number and gets a short summary of the account's most recent activity, like the mini statement on an ATM slip. It shows who the account belongs to, the current balance, and the latest transactions.

Why: customers want a quick look at recent activity without requesting a full statement, which reduces branch visits and support calls.

This feature is read-only. Out of scope: date-range filters, pagination, PDF or email delivery, authentication, and any change to account data.
```

**Review:** open the generated `specs/<nnn>-mini-statement/spec.md`. Are the user stories, acceptance scenarios and edge cases what you expected? What did the spec leave open?

### Step 2 — Clarify

```text
/speckit-clarify Focus on: how many transactions are shown and whether the caller can change that, the order of the transactions, how the account number is displayed, and what happens for an unknown account and for an account with no transactions.
```

Answer the agent's questions like a product owner would. Your answers are written back into the spec.

### Step 3 — Plan (now the tech is allowed)

```text
/speckit-plan Use the existing FastAPI skeleton in this repo. Keep the layering router -> service -> repository -> SQLAlchemy models, and add no new dependencies, tables or migrations. Money is stored as integer paise and must never be handled as float. Return Pydantic response models, raise AppError subclasses for errors, and write pytest tests using the fixtures in tests/conftest.py.
```

**Review:** does the plan respect the layers and the constitution? Is anything over-engineered?

### Step 4 — Tasks

```text
/speckit-tasks
```

### Step 5 — Analyze (optional quality gate)

```text
/speckit-analyze
```

### Step 6 — Implement

```text
/speckit-implement
```

### Step 7 — Converge

```text
/speckit-converge
```

Repeat **implement → converge** until the result says **Converged**.

---

## 4. Definition of done

```bash
uv run ruff check .
uv run pytest
uv run python -m app.db.seed
uv run uvicorn app.main:app --reload
```

- [ ] Every acceptance scenario in your `spec.md` is covered by a passing test.
- [ ] You tried the endpoint in Swagger (<http://127.0.0.1:8000/docs>, or the port you chose) for the seed accounts, an unknown account and bad input.
- [ ] `FeatureNotImplementedError` is gone from `statement_service.py`.
- [ ] No `float` is used for money, and the feature does not modify the database.
- [ ] Layers are respected: no business logic in the router, no SQL in the service.

## 5. Stretch ideas (each is a new Spec Kit cycle)

- Filter by date range.
- Add pagination.
- Return the statement as a PDF.
