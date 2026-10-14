from sqlalchemy.orm import Session


class TransactionRepository:
    """All database access for transactions lives here.

    TODO(feature-01): add the query that the mini statement needs.
    """

    def __init__(self, db: Session):
        self.db = db
