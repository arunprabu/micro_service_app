from app.core.exceptions import FeatureNotImplementedError
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository


class StatementService:
    """Business rules for the mini statement. Talks to repositories, knows nothing about HTTP."""

    def __init__(self, accounts: AccountRepository, transactions: TransactionRepository):
        self.accounts = accounts
        self.transactions = transactions

    def get_mini_statement(self, account_number: str):
        # TODO(feature-01): build it - see docs/features/01-mini-statement.md
        raise FeatureNotImplementedError("Mini statement is not implemented yet.")
