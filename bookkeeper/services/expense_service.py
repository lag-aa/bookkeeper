"""
Expense Service
"""

from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense


class ExpenseService:
    def __init__(self, repo: AbstractRepository[T] = None) -> None:
        """
        Initializes the ExpenseService.

        Parameters:
            repo (AbstractRepository[T], optional): Repository to use. Defaults to None.
        """
        self.repo = repo or SQLiteRepository[Expense](Expense)

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
