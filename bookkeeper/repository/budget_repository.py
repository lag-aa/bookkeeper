"""Module for the BudgetRepository class."""

from decimal import Decimal
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.budget import Budget


class BudgetRepository(SQLiteRepository[Budget], AbstractRepository[Budget]):
    """Repository class for managing budgets."""

    def __init__(self, db_file: str = None) -> None:
        super().__init__(Budget, db_file)

    def get_with_expenses(self, pk: int):
        """
        Retrieve a budget with associated expenses.

        Args:
            pk (int): Primary key of the budget to retrieve.

        Returns:
            Budget or None: Budget object with expenses if found, else None.
        """

        budget = self.get(pk=pk)
        if not budget:
            return None

        start_date, end_date = budget.period_dates
        query = """
            SELECT SUM(amount) as total FROM expense
            WHERE expense_date BETWEEN ? AND ?
        """
        row = self.db.fetchone(query, (start_date, end_date))
        expenses = Decimal(row["total"]) if row["total"] else Decimal("0")
        budget.expenses = expenses
        return budget
