from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class TxnType(StrEnum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class Transaction(Base):
    """One ledger entry. balance_after_paise is the account balance right after this entry."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    txn_type: Mapped[str] = mapped_column(String(10))
    amount_paise: Mapped[int]
    balance_after_paise: Mapped[int]
    description: Mapped[str] = mapped_column(String(200))
    txn_date: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(UTC))

    account: Mapped[Account] = relationship(back_populates="transactions")
