"""
Сервис бюджета
"""

from typing import Any
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository


class BudgetService:
    def __init__(self) -> None:
        self.repo = MemoryRepository[Budget]()

    def add(self, budget: Budget) -> int:
        """
        Добавить бюджет в хранилище.

        Parameters
        ----------
        budget - Объект Budget, бюджет

        Returns
        -------
        PK созданной расходной операции
        """
        return self.repo.add(budget)

    def get(self, pk: int) -> Budget | None:
        """
        Получить бюджет по pk

        Parameters
        ----------
        pk - pk бюджета

        Returns
        -------
        Объект Budget
        """
        return self.repo.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Budget]:
        """
        Получить список всех записей о бюджете из хранилища

        Parameters
        ----------
        where - Объект фильтрации

        Returns
        -------
        Список объектов Budget
        """
        return self.repo.get_all(where)

    def update(self, obj: Budget) -> None:
        """
        Обновить данные об расходной операции. Объект должен содержать поле pk.

        Parameters
        ----------
        obj - Объект Budget
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
