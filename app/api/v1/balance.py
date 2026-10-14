from fastapi import APIRouter

from app.api.deps import BalanceServiceDep

router = APIRouter(prefix="/accounts", tags=["Minimum Balance Check"])


# TODO(feature-02): add response_model + query params.
# See docs/features/02-minimum-balance-check.md
@router.get(
    "/{account_number}/minimum-balance-check",
    summary="Check an account against its minimum balance",
)
def check_minimum_balance(account_number: str, service: BalanceServiceDep):
    return service.check_minimum_balance(account_number)
