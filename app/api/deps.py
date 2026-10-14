"""Dependency wiring: Session -> Repositories -> Services. Routers only ask for a service."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.balance_service import BalanceService
from app.services.statement_service import StatementService

DbSession = Annotated[Session, Depends(get_db)]


def get_account_repository(db: DbSession) -> AccountRepository:
    return AccountRepository(db)


def get_transaction_repository(db: DbSession) -> TransactionRepository:
    return TransactionRepository(db)


AccountRepo = Annotated[AccountRepository, Depends(get_account_repository)]
TransactionRepo = Annotated[TransactionRepository, Depends(get_transaction_repository)]


def get_statement_service(accounts: AccountRepo, transactions: TransactionRepo) -> StatementService:
    return StatementService(accounts, transactions)


def get_balance_service(accounts: AccountRepo) -> BalanceService:
    return BalanceService(accounts)


StatementServiceDep = Annotated[StatementService, Depends(get_statement_service)]
BalanceServiceDep = Annotated[BalanceService, Depends(get_balance_service)]
