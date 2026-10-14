# Feature 02 — Minimum Balance Check

> **Goal:** build the minimum balance check endpoint using **GitHub Spec Kit (Spec-Driven Development)**.
> Describe *what and why* first, then let the workflow take you through the plan, tasks and code. **Do not hand-write the feature.**
> Review the output of each step before moving on.

**Before you start:** complete the one-time setup in the [README](../../README.md#build-the-features-with-spec-kit) (install `specify`, `specify init`, constitution) and make sure `uv run pytest` is green.
This feature is independent of [Feature 01](./01-mini-statement.md); build them in either order.

Paste the prompts below into the Copilot Chat agent **one at a time** (Copilot uses the `/speckit-*` syntax).

---

## 1. The business use case

Banks require each account to keep a **minimum balance** and charge penalties when it is breached. Given an **account number**, tell the caller whether the account currently meets its minimum balance.

## 2. What the skeleton already gives you

| Piece | Where | State |
|---|---|---|
| Route | [app/api/v1/balance.py](../../app/api/v1/balance.py) | `GET /api/v1/accounts/{account_number}/minimum-balance-check` is wired and returns `501` |
| Service | [app/services/balance_service.py](../../app/services/balance_service.py) | placeholder that raises `FeatureNotImplementedError` |
| Repository | [app/repositories/account_repository.py](../../app/repositories/account_repository.py) | `get_by_account_number` exists |
| Schemas | [app/schemas/](../../app/schemas) | empty |
| Errors | [app/core/exceptions.py](../../app/core/exceptions.py) | `AccountNotFoundError` (404) is ready to use |
| Data | `Account` model has the balance and the minimum balance; [seed data](../../app/db/seed.py) | 3 accounts: above, below and exactly at the minimum |
| Tests | [tests/conftest.py](../../tests/conftest.py) | `client` and `db_session` fixtures (in-memory SQLite) |

---

## 3. Run the Spec Kit workflow

### Step 1 — Specify (what and why, no tech)

```text
/speckit-specify Build a minimum balance check for a retail bank's account service.

Every account must maintain a minimum balance, which is stored on the account. Given an account number, tell the caller whether the account currently meets its minimum balance requirement. The answer shows the current balance, the required minimum, whether the requirement is met and, if it is not, by how much the account falls short.

Why: banks levy penalties for non-maintenance of the minimum balance, so branch staff and digital channels need a quick, reliable way to check an account.

This feature is read-only. Out of scope: debiting money, charging penalties, notifications, and authentication.
```

**Review:** open the generated `specs/<nnn>-minimum-balance-check/spec.md`. Are the user stories, acceptance scenarios and edge cases what you expected? What did the spec leave open?

### Step 2 — Clarify

```text
/speckit-clarify Focus on: the case where the balance is exactly equal to the minimum, how amounts are represented in the response, how the account number is displayed, and what happens for an unknown account.
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
- [ ] You tried the endpoint in Swagger (<http://127.0.0.1:8000/docs>, or the port you chose) for all three seed accounts (above, below and exactly at the minimum), an unknown account and bad input.
- [ ] `FeatureNotImplementedError` is gone from `balance_service.py`.
- [ ] No `float` is used for money, and the feature does not modify the database.
- [ ] Layers are respected: no business logic in the router, no SQL in the service.

## 5. Stretch ideas (each is a new Spec Kit cycle)

- Check whether a proposed withdrawal would breach the minimum.
- Different minimums by customer tier.
- Estimate the penalty fee when the minimum is breached.
