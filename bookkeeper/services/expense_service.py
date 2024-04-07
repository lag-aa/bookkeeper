"""
Expense Service
"""

from typing import Any
from datetime import datetime
from decimal import Decimal
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.expense import Expense


class ExpenseService:
    def __init__(self, repo: AbstractRepository[Expense] = None) -> None:
        """
        Initializes the ExpenseService.

        Parameters:
            repo (AbstractRepository[T], optional): Repository to use. Defaults to None.
        """
        self.repo = repo or ExpenseRepository()

    def add(self, expense: Expense) -> int:
        """
        Add an expense to the storage.

        Parameters:
            expense (Expense): Expense object.

        Returns:
            int: ID of the created expense operation.
        """
        return self.repo.add(expense)

    def get(self, pk: int) -> Expense | None:
        """
        Get an expense operation by pk.

        Parameters:
            pk (int): Expense pk.

        Returns:
            Expense | None: Expense object.
        """
        return self.repo.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Expense]:
        """
        Get a list of all expense operations from the storage.

        Parameters:
            where (dict[str, Any] | None, optional): Filtering object. Defaults to None.

        Returns:
            list[Expense]: List of Expense objects.
        """
        return self.repo.get_all(where)

    def update(self, obj: Expense) -> None:
        """
        Update expense operation data. The object must contain the pk field.

        Parameters:
            obj (Expense): Expense object.
        """
        self.repo.update(obj)

    def delete(self, pk: int) -> None:
        """
        Delete a record

        Parameters:
            pk (int): Expense pk.
        """
        self.repo.delete(pk)

    def get_total_expense_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> Decimal:
        """
        Get the total expenses for the specified period of time.

        Parameters:
        start_date (datetime): The start date of the period.
        end_date (datetime): The end date of the period.

        Returns:
        Decimal: The total expenses for the specified period.
        """
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("start_date and end_date must be instances of datetime.")

        return self.repo.get_total_expense_for_period(start_date, end_date)
