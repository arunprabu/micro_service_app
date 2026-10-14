from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class AccountType(StrEnum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"


class Account(Base):
    """A bank account. Money is stored as integer paise (1 rupee = 100 paise), never float."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    holder_name: Mapped[str] = mapped_column(String(100))
    account_type: Mapped[str] = mapped_column(String(10))
    balance_paise: Mapped[int] = mapped_column(default=0)
    min_balance_paise: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    transactions: Mapped[list[Transaction]] = relationship(back_populates="account")
