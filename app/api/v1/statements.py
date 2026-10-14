from fastapi import APIRouter

from app.api.deps import StatementServiceDep

router = APIRouter(prefix="/accounts", tags=["Mini Statement"])


# TODO(feature-01): add response_model + query params. See docs/features/01-mini-statement.md
@router.get("/{account_number}/mini-statement", summary="Get the mini statement of an account")
def get_mini_statement(account_number: str, service: StatementServiceDep):
    return service.get_mini_statement(account_number)
