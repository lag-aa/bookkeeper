"""
Module containing the description of an abstract repository.

The repository implements storage of objects by assigning each object a unique
identifier in the 'pk' attribute (primary key). Objects that can be saved
in the repository must support adding the 'pk' attribute and should not
use it for other purposes.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Model should contain the 'pk' attribute.
    """

    pk: int


T = TypeVar("T", bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Abstract repository.
    Abstract methods:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Add an object to the repository, return the object's id,
        also store the id in the 'pk' attribute.
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:
        """Get an object by id"""

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Get all records based on some condition.
        'where' - condition as a dictionary {'field_name': value}
        if the condition is not specified (by default), return all records.
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """Update object data. The object must contain the 'pk' field."""

    @abstractmethod
    def delete(self, pk: int) -> None:
        """Delete a record"""
