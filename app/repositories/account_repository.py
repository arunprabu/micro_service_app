from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Account


class AccountRepository:
    """All database access for accounts lives here. Services never write SQL."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_account_number(self, account_number: str) -> Account | None:
        return self.db.scalar(select(Account).where(Account.account_number == account_number))
