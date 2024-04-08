"""
Module for SQLite repository operations.

This module provides a SQLiteRepository class for performing CRUD operations
on objects stored in a SQLite database.

Classes:
    SQLiteRepository: A repository class for SQLite database operations.
"""

from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.utils.sqlite_utils import SQLite
import configparser


config = configparser.ConfigParser()
config.read("bookkeeper/config/settings.ini")
db_name = config["sqllite"]["db_name"]


class SQLiteRepository(AbstractRepository[T]):
    """
    A repository class for SQLite database operations.

    Args:
        cls (type): The class type of objects to be stored in the repository.
        db_file (str): The path to the SQLite database file. Default is db_name \
            from settings.ini.

    Attributes:
        db (SQL): The SQL database connection.
        cls (type): The class type of objects stored in the repository.
        table_name (str): The name of the database table.
        fields (dict[str, Any]): The fields and their types of the objects \
            stored in the repository.
    """

    def __init__(self, cls: type, db_file: str = None) -> None:
        """
        Initializes the SQLiteRepository.

        Args:
            cls (type): The class type of objects to be stored in the repository.
            db_file (str): The path to the SQLite database file. Default is db_name \
                from settings.ini.
        """
        config = configparser.ConfigParser()
        config.read("bookkeeper/config/settings.ini")

        if db_file is None:
            db_file = config["sqllite"]["db_name"]

        self.db: SQLite = SQLite(db_file)
        self.cls: type = cls
        self.table_name: str = cls.__name__.lower()
        self.fields: dict[str, Any] = get_annotations(cls, eval_str=True)
        self.__create_table()

    def __create_table(self) -> None:
        """
        Creates the database table based on the class fields.

        Note:
            If an attribute is annotated as UnionType, str type will be used \
                for that attribute.
        """
        columns: list[str] = []
        for key, key_type in self.fields.items():
            column_type: Any = getattr(key_type, "__name__", "str")
            columns.append(
                f"{key} {column_type if key != 'pk' else 'INTEGER PRIMARY KEY UNIQUE'}"
            )
        fields: str = ", ".join(columns) if columns else ""
        self.db.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} \
            ({fields})"
        )

    def add(self, obj: T) -> int:
        """
        Adds an object to the repository.

        Args:
            obj (T): The object to be added.

        Returns:
            int: The primary key (pk) of the added object.
        """
        fields: dict[str, Any] = self.fields.copy()
        fields.pop("pk", None)
        if getattr(obj, "pk", None) != 0:
            raise ValueError(f"trying to add object {obj} with filled `pk` attribute")

        columns: str = ", ".join(fields)
        p: str = ", ".join(["?"] * len(fields))
        values: tuple[Any] = tuple([getattr(obj, x) for x in fields])

        cur = self.db.execute("PRAGMA foreign_keys = ON")
        query: str = (
            f"INSERT INTO {self.table_name} ({columns}) VALUES ({p})"
            if columns
            else f"INSERT INTO {self.table_name} DEFAULT VALUES"
        )
        cur = self.db.execute(query, values)
        obj.pk = cur.lastrowid
        return obj.pk

    def get(self, pk: int) -> T | None:
        """
        Retrieves an object from the repository based on its primary key (pk).

        Args:
            pk (int): The primary key of the object to be retrieved.

        Returns:
            T | None: The retrieved object or None if not found.
        """
        query: str = f"SELECT * FROM {self.table_name} WHERE pk = ?"
        row: dict[str, Any] = self.db.fetchone(query, (pk,))
        return self.cls(**row) if row else None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Retrieves all objects from the repository, optionally filtered by a WHERE clause.

        Args:
            where (dict[str, Any] | None): Optional WHERE clause parameters.

        Returns:
            list[T]: List of retrieved objects.
        """
        query: str = f"SELECT * FROM {self.table_name}"
        params: tuple = ()

        if where:
            keys: str = ", ".join([f"{key} = ?" for key in where.keys()])
            values: tuple = tuple(where.values())
            query += f" WHERE {keys}"
            params = values

        rows: list[dict[str, Any]] = self.db.fetchall(query, params)
        return [self.cls(**row) for row in rows]

    def update(self, obj: T) -> None:
        """
        Updates an object in the repository.

        Args:
            obj (T): The object to be updated.

        Raises:
            ValueError: If the object's primary key (pk) is unknown.
        """
        if obj.pk == 0:
            raise ValueError("attempt to update object with unknown primary key")
        fields: dict[str, Any] = dict(vars(obj))
        pk: int = fields.pop("pk")  # Remove "pk" if it exists
        columns: str = ", ".join([f"{key} = ?" for key in fields.keys()])
        values: tuple = tuple(fields.values())
        self.db.execute(
            f"UPDATE {self.table_name} SET {columns} WHERE pk = ?",
            (*values, pk),
        )

    def delete(self, pk: int) -> None:
        """
        Deletes an object from the repository based on its primary key (pk).

        Args:
            pk (int): The primary key of the object to be deleted.

        Raises:
            KeyError: If the object with the specified primary key does not exist.
        """
        query: str = f"SELECT * FROM {self.table_name} WHERE pk = ?"
        row: dict[str, Any] = self.db.fetchone(query, (pk,))

        if not row:
            raise KeyError(
                f"Records with pk={pk} do not exist in the '{self.table_name}' table"
            )

        self.db.execute(f"DELETE FROM {self.table_name} WHERE pk = ?", (pk,))
