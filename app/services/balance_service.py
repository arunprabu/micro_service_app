from app.core.exceptions import FeatureNotImplementedError
from app.repositories.account_repository import AccountRepository


class BalanceService:
    """Business rules for the minimum balance check. Knows nothing about HTTP."""

    def __init__(self, accounts: AccountRepository):
        self.accounts = accounts

    def check_minimum_balance(self, account_number: str):
        # TODO(feature-02): build it - see docs/features/02-minimum-balance-check.md
        raise FeatureNotImplementedError("Minimum balance check is not implemented yet.")
