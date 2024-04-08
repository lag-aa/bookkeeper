from datetime import datetime
from decimal import Decimal
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense


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

    def get_all(self, where: dict[str, Any] | None = None) -> list[Expense]:
        query: str = (
            f"SELECT {self.table_name}.*, category.name AS category \
            FROM {self.table_name} LEFT JOIN category ON expense.category = category.pk"
        )
        params: tuple = ()

        if where:
            keys: str = ", ".join([f"{key} = ?" for key in where.keys()])
            values: tuple = tuple(where.values())
            query += f" WHERE {keys}"
            params = values

        rows: list[dict[str, Any]] = self.db.fetchall(query, params)
        return [self.cls(**row) for row in rows]
