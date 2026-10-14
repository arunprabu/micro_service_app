from sqlalchemy import select

from app.db.seed import seed
from app.models import Account, Transaction
from app.repositories.account_repository import AccountRepository


def test_get_by_account_number_finds_seeded_account(db_session):
    seed(db_session)

    account = AccountRepository(db_session).get_by_account_number("1000000001")

    assert isinstance(account, Account)
    assert account.holder_name == "Asha Verma"


def test_get_by_account_number_returns_none_for_unknown(db_session):
    assert AccountRepository(db_session).get_by_account_number("does-not-exist") is None


def test_seed_is_idempotent_and_balances_match_ledger(db_session):
    assert seed(db_session) == 3
    assert seed(db_session) == 0

    for account in db_session.scalars(select(Account)):
        latest = db_session.scalars(
            select(Transaction)
            .where(Transaction.account_id == account.id)
            .order_by(Transaction.txn_date.desc(), Transaction.id.desc())
            .limit(1)
        ).one()
        assert account.balance_paise == latest.balance_after_paise
