"""
Module describing a repository that operates in memory.
"""

from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class MemoryRepository(AbstractRepository[T]):
    """
    Repository operating in memory.
    """

    def __init__(self) -> None:
        """
        Initializes the MemoryRepository.
        """
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        """
        Adds an object to the repository and returns its ID.

        Args:
            obj (T): Object to add to the repository.

        Returns:
            int: The ID of the added object.
        """
        if getattr(obj, "pk", None) != 0:
            raise ValueError(f"trying to add object {obj} with filled `pk` attribute")
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        """
        Retrieves an object from the repository by its ID.

        Args:
            pk (int): The ID of the object to retrieve.

        Returns:
            T | None: The retrieved object or None if not found.
        """
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Retrieves all objects from the repository based on a condition.

        Args:
            where (dict[str, Any] | None): The condition to filter objects.

        Returns:
            list[T]: List of retrieved objects.
        """
        if where is None:
            return list(self._container.values())
        return [
            obj
            for obj in self._container.values()
            if all(getattr(obj, attr) == value for attr, value in where.items())
        ]

    def update(self, obj: T) -> None:
        """
        Updates an object in the repository.

        Args:
            obj (T): The object to update.

        Raises:
            ValueError: If the object's primary key is unknown (pk=0).
        """
        if obj.pk == 0:
            raise ValueError("attempt to update object with unknown primary key")
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        """
        Deletes an object from the repository by its ID.

        Args:
            pk (int): The ID of the object to delete.
        """
        self._container.pop(pk)
