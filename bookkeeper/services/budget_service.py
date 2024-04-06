"""
Budget Service
"""

from typing import Any
from bookkeeper.models.budget import Budget
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class BudgetService:
    def __init__(self, repo: AbstractRepository[T] = None) -> None:
        """
        Initializes the BudgetService.

        Parameters:
            repo (AbstractRepository[T], optional): Repository to use. Defaults to None.
        """
        self.repo = repo or SQLiteRepository[Budget](Budget)

    def add(self, budget: Budget) -> int:
        """
        Add a budget to the storage.

        Parameters:
            budget (Budget): Budget object.

        Returns:
            int: PK of the created budget operation.
        """
        return self.repo.add(budget)

    def get(self, pk: int) -> Budget | None:
        """
        Get a budget by pk.

        Parameters:
            pk (int): Budget pk.

        Returns:
            Budget | None: Budget object.
        """
        return self.repo.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Budget]:
        """
        Get a list of all budget records from the storage.

        Parameters:
            where (dict[str, Any] | None, optional): Filtering object. Defaults to None.

        Returns:
            list[Budget]: List of Budget objects.
        """
        return self.repo.get_all(where)

    def update(self, obj: Budget) -> None:
        """
        Update budget data. The object must contain the pk field.

        Parameters:
            obj (Budget): Budget object.
        """
        self.repo.update(obj)

    def delete(self, pk: int) -> None:
        """
        Delete a record.

        Parameters:
            pk (int): Budget operation pk.
        """
        self.repo.delete(pk)
