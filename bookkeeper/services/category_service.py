"""
Expense Category Service
"""

from collections import defaultdict
from typing import Iterator
from typing import Any
from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryService:
    def __init__(self, repo: AbstractRepository[Category] = None) -> None:
        """
        Initializes the CategoryService.

        Parameters:
            repo (AbstractRepository[T], optional): Repository to use. Defaults to None.
        """
        self.repo = repo or SQLiteRepository[Category](cls=Category)

    def add(self, category: Category) -> int:
        """
        Add a category to the storage.

        Parameters:
            category (Category): Category object.

        Returns:
            int: ID of the created category.
        """
        print(category)
        return self.repo.add(category)

    def get(self, pk: int) -> Category | None:
        """
        Get a category by pk.

        Parameters:
            pk (int): Category pk.

        Returns:
            Category | None: Category object.
        """
        return self.repo.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[Category]:
        """
        Get a list of all categories from the storage.

        Parameters:
            where (dict[str, Any] | None, optional): Filtering object. Defaults to None.

        Returns:
            list[Category]: List of Category objects.
        """
        return self.repo.get_all(where)

    def update(self, category: Category) -> None:
        """
        Update category data. The object must contain the pk field.

        Parameters:
            obj (Category): Category object.
        """
        self.repo.update(category)

    def delete(self, pk: int) -> None:
        """
        Delete a record.

        Parameters:
            pk (int): Category pk.
        """
        self.repo.delete(pk)

    def get_parent(self, category: Category) -> Category | None:
        """
        Get the parent category as a Category object.
        Returns None if called on a top-level category.

        Parameters:
            category (Category): Category object.

        Returns:
            Category | None: Category object or None.
        """
        if category.parent is None:
            return None
        return self.repo.get(category.parent)

    def get_all_parents(self, category: Category) -> Iterator[Category]:
        """
        Get all top-level categories in the hierarchy.

        Parameters:
            category (Category): Category object.

        Yields:
            Iterator[Category]: Category objects from the parent \
            to the top-level category.
        """
        parent = self.get_parent(category)
        if parent is None:
            return
        yield parent
        yield from self.get_all_parents(parent)

    def get_subcategories(self, category_pk: int) -> Iterator[Category]:
        """
        Get all subcategories from the hierarchy, including
        their subcategories and so on.

        Parameters:
            category_pk (int): Category object pk.

        Yields:
            Iterator[Category]: Category objects representing \
            subcategories of various levels below this category.
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
        Create a category tree from a list of "child-parent" pairs.
        The list must be topologically sorted, i.e. children
        should not appear before their parents.
        No validation of the input data is performed.
        When using DBMS with foreign key checks, an error will be raised
        (for sqlite3 - IntegrityError). Without DBMS validation,
        the result may be correct if the input data is correct except for sorting.
        If not, then not.
        "Garbage in, garbage out".

        Parameters:
            tree (list[tuple[str, str | None]]): List of "child-parent" pairs.

        Returns:
            list[Category]: List of created Category objects.
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = Category(child, created[parent].pk if parent is not None else None)
            self.repo.add(cat)
            created[child] = cat
        return list(created.values())
