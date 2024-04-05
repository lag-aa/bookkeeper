"""
Сервис расходов
"""

from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense


class ExpenseService:
    def __init__(self, repo: AbstractRepository[T] = None) -> None:
        self.repo = repo or SQLiteRepository[Expense](Expense)

    def add(self, expense: Expense) -> int:
        """
        Добавить расход в хранилище.

        Parameters
        ----------
        expense - Объект Expense, расходная операция

        Returns
        -------
        PK созданной расходной операции
        """
        return self.repo.add(expense)

    def get(self, pk: int) -> Expense | None:
        """
        Получить расходную операцию по pk

        Parameters
        ----------
        pk - pk расходной операции
        Returns
        -------
        Объект Expense
        """
        return self.repo.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Expense]:
        """
        Получить список всех расходных операций из хранилища

        Parameters
        ----------
        where - Объект фильтрации

        Returns
        -------
        Список объектов Expense
        """
        return self.repo.get_all(where)

    def update(self, obj: Expense) -> None:
        """
        Обновить данные об расходной операции. Объект должен содержать поле pk.

        Parameters
        ----------
        obj - Объект Expense
        """
        self.repo.update(obj)

    def delete(self, pk: int) -> None:
        """
        Удалить запись

        Parameters
        ----------
        pk - pk расходной операции
        """
        self.repo.delete(pk)
