from datetime import datetime
from decimal import Decimal
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class ExpenseRepository(SQLiteRepository[Expense], AbstractRepository[Expense]):
    def __init__(self, db_file: str = None) -> None:
        super().__init__(Expense, db_file)

    def get_total_expense_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> int:

        query = f"""
            SELECT SUM(amount) as total FROM {self.table_name} 
            WHERE expense_date BETWEEN ? AND ?
        """
        row = self.db.fetchone(query, (start_date, end_date))
        return Decimal(row["total"]) if row["total"] else Decimal("0")