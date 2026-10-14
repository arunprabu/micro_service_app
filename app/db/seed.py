"""Load sample accounts and transactions. Run: uv run python -m app.db.seed"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, init_db
from app.models import Account, AccountType, Transaction, TxnType

# (days_ago, type, amount in rupees, description) - oldest first.
Entry = tuple[int, TxnType, int, str]

SAMPLE_ACCOUNTS: list[tuple[str, str, AccountType, int, list[Entry]]] = [
    # Healthy savings account: balance Rs 25,152 vs minimum Rs 5,000.
    (
        "1000000001",
        "Asha Verma",
        AccountType.SAVINGS,
        5_000,
        [
            (30, TxnType.CREDIT, 50_000, "Salary credit - ACME Corp"),
            (28, TxnType.DEBIT, 12_000, "Rent - UPI"),
            (25, TxnType.DEBIT, 1_500, "Electricity bill"),
            (22, TxnType.DEBIT, 2_200, "ATM withdrawal"),
            (20, TxnType.DEBIT, 850, "Grocery - POS"),
            (18, TxnType.CREDIT, 3_000, "UPI from Rahul"),
            (15, TxnType.DEBIT, 499, "OTT subscription"),
            (12, TxnType.DEBIT, 1_800, "Restaurant - POS"),
            (10, TxnType.DEBIT, 5_000, "NEFT to LIC"),
            (7, TxnType.CREDIT, 1_250, "Refund - e-commerce"),
            (5, TxnType.DEBIT, 2_750, "Fuel - POS"),
            (3, TxnType.DEBIT, 999, "Mobile recharge"),
            (1, TxnType.DEBIT, 1_500, "ATM withdrawal"),
        ],
    ),
    # Savings account BELOW its minimum: balance Rs 4,500 vs minimum Rs 5,000.
    (
        "1000000002",
        "Rohan Mehta",
        AccountType.SAVINGS,
        5_000,
        [
            (20, TxnType.CREDIT, 10_000, "Cash deposit"),
            (15, TxnType.DEBIT, 4_000, "Rent - UPI"),
            (8, TxnType.DEBIT, 1_200, "Grocery - POS"),
            (2, TxnType.DEBIT, 300, "Cab fare"),
        ],
    ),
    # Current account EXACTLY at its minimum: balance Rs 10,000 vs minimum Rs 10,000.
    (
        "1000000003",
        "Kiran Traders",
        AccountType.CURRENT,
        10_000,
        [
            (10, TxnType.CREDIT, 25_000, "Customer payment - Invoice 101"),
            (6, TxnType.DEBIT, 15_000, "Vendor payment - NEFT"),
        ],
    ),
]


def seed(db: Session) -> int:
    """Insert sample data if the accounts table is empty. Returns the accounts created."""
    if db.scalar(select(Account.id).limit(1)) is not None:
        return 0

    now = datetime.now(UTC)
    for number, holder, account_type, min_balance, entries in SAMPLE_ACCOUNTS:
        account = Account(
            account_number=number,
            holder_name=holder,
            account_type=account_type,
            min_balance_paise=min_balance * 100,
        )
        balance = 0
        for days_ago, txn_type, rupees, description in entries:
            amount = rupees * 100
            balance += amount if txn_type == TxnType.CREDIT else -amount
            account.transactions.append(
                Transaction(
                    txn_type=txn_type,
                    amount_paise=amount,
                    balance_after_paise=balance,
                    description=description,
                    txn_date=now - timedelta(days=days_ago),
                )
            )
        account.balance_paise = balance
        db.add(account)
    db.commit()
    return len(SAMPLE_ACCOUNTS)


if __name__ == "__main__":
    init_db()
    with SessionLocal() as session:
        created = seed(session)
    print(f"Seeded {created} accounts." if created else "Data already present - nothing to do.")
