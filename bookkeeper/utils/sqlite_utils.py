"""
SQLite database utility.
"""

from typing import Any, Dict, List, Tuple
from datetime import datetime
from decimal import Decimal
import sqlite3
from bookkeeper.models.budget import PeriodType


def dict_factory(cursor: sqlite3.Cursor, row: Tuple) -> Dict[str, Any]:
    """
    Custom row factory for SQLite cursor.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        row (Tuple): Row fetched from the database.

    Returns:
        Dict[str, Any]: Dictionary representing the row data.
    """
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


# pylint: disable=W0511
class SQLite:
    """
    Utility class for SQLite database operations.

    Attributes:
        db_name (str): The name of the SQLite database.
        conn (sqlite3.Connection): SQLite database connection.
        cur (sqlite3.Cursor): SQLite database cursor.
    """

    def __init__(self, db_name: str) -> None:
        """
        Initializes the SQL utility.

        Args:
            db_name (str): The name of the SQLite database.
        """
        self.db_name: str = db_name
        self.conn: sqlite3.Connection = None
        self.cur: sqlite3.Cursor = None

    def __enter__(self) -> "SQLite":
        """
        Enters the context manager.

        Returns:
            SQL: The SQL utility object.
        """
        self.conn = sqlite3.connect(
            self.db_name,
            detect_types=(sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES),
        )
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """
        Exits the context manager.
        """
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.commit()
                self.conn.close()
        except sqlite3.Error as error:
            print("Failed to read data from table", error)

    def fetchall(
        self, sql: str, parameters: Tuple[Any, ...] = ()
    ) -> List[Dict[str, Any]]:
        """
        Fetches all rows from the database based on the SQL query.

        Args:
            sql (str): The SQL query to execute.
            parameters (Tuple): Parameters to be substituted in the SQL query.

        Returns:
            List[Dict[str, Any]]: List of dictionaries representing the fetched rows.
        """
        with self as db:
            db.cur.execute(sql, parameters)
            return db.cur.fetchall()

    def fetchone(self, sql: str, parameters: Tuple[Any, ...] = ()) -> Dict[str, Any]:
        """
        Fetches a single row from the database based on the SQL query.

        Args:
            sql (str): The SQL query to execute.
            parameters (Tuple): Parameters to be substituted in the SQL query.

        Returns:
            Dict[str, Any]: Dictionary representing the fetched row.
        """
        with self as db:
            db.cur.execute(sql, parameters)
            return db.cur.fetchone()

    def execute(self, sql: str, parameters: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """
        Executes an SQL query on the database.

        Args:
            sql (str): The SQL query to execute.
            parameters (Tuple): Parameters to be substituted in the SQL query.

        Returns:
            sqlite3.Cursor: SQLite cursor after executing the query.
        """
        # TODO Replace validation
        try:
            with self as db:
                return db.cur.execute(sql, parameters)
        except sqlite3.IntegrityError as err:
            err_type = "UNIQUE constraint failed"
            if err_type in str(err):
                msg_error = str(err).replace(
                    err_type, "Используйте уникальное значение"
                )
                raise ValueError(msg_error) from err
            return None


def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


def adapt_period_type(val):
    """Adapt PeriodType to str."""
    return val.value


def adapt_decimal(val):
    """Adapt Decimal to str"""
    return str(val)


def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())


def convert_period_type(val):
    """Convert str to PeriodType object."""
    return PeriodType(val.decode())


def convert_decimal(val):
    """convert to Decimal"""
    return Decimal(val.decode())


# pylint: disable=W0108
sqlite3.register_adapter(datetime, adapt_datetime_iso)
sqlite3.register_adapter(str, lambda val: str(val))
sqlite3.register_adapter(PeriodType, adapt_period_type)
sqlite3.register_adapter(Decimal, adapt_decimal)

sqlite3.register_converter("PeriodType", convert_period_type)
sqlite3.register_converter("str", lambda val: str(val.decode()))
sqlite3.register_converter("Decimal", convert_decimal)
sqlite3.register_converter("datetime", convert_datetime)
