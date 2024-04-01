"""
Сервис категории расходов
"""

from collections import defaultdict
from typing import Iterator
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category


# TODO Добавить аннотации к методам
class CategoryService:
    def __init__(self, repo: AbstractRepository[Category]) -> None:
        self.repo = repo

    def add(self, category: Category) -> int:
        """
        Добавить категорию в хранилище.

        Parameters
        ----------
        category - Объект Category, категория

        Returns
        -------
        ID созданной категории
        """
        return self.repo.add(category)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Category]:
        """
        Получить список всех категорий из хранилища

        Parameters
        ----------
        where - Объект фильтрации

        Returns
        -------
        Список объектов Category
        """
        return self.repo.get_all(where)

    def get_parent(self, category: Category) -> Category | None:
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        category - Объект Category, категория

        Returns
        -------
        Объект класса Category или None
        """
        if category.parent is None:
            return None
        return self.repo.get(category.parent)

    def get_all_parents(self, category: Category) -> Iterator[Category]:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        category - Объект Category, категория

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(category)
        if parent is None:
            return
        yield parent
        yield from self.get_all_parents(parent)

    def get_subcategories(self, category_pk: int) -> Iterator[Category]:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        category_pk - pk ключ объекта Category

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """

        def get_children(
            graph: dict[int | None, list[Category]], root: int
        ) -> Iterator[Category]:
            """dfs in graph from root"""
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in self.repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, category_pk)

    def create_from_tree(self, tree: list[tuple[str, str | None]]) -> list[Category]:
        """
        Создать дерево категорий из списка пар "потомок-родитель".
        Список должен быть топологически отсортирован, т.е. потомки
        не должны встречаться раньше своего родителя.
        Проверка корректности исходных данных не производится.
        При использовании СУБД с проверкой внешних ключей, будет получена
        ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        со стороны СУБД, результат, возможно, будет корректным, если исходные
        данные корректны за исключением сортировки. Если нет, то нет.
        "Мусор на входе, мусор на выходе".

        Parameters
        ----------
        tree - список пар "потомок-родитель"

        Returns
        -------
        Список созданных объектов Category
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = Category(child, created[parent].pk if parent is not None else None)
            self.repo.add(cat)
            created[child] = cat
        return list(created.values())
