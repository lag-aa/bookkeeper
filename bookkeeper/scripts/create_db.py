import sqlite3
from bookkeeper.models.budget import PeriodType
import configparser


def create_database(db_name: str = None, test_mode: bool = False):
    """
    Function for creating a database, tables, and populating them with data.

    Parameters
    ----------
    db_name : str
        Name (path to) the database.
    test_mode : bool
        Test mode flag, if True, test tables will be created.
    """

    config = configparser.ConfigParser()
    config.read("bookkeeper/config/settings.ini")

    if not db_name:
        db_name = config["sqllite"]["db_name"]
        
    # Establish connection to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop all tables from the database
    cursor.execute("DROP TABLE IF EXISTS category;")
    cursor.execute("DROP TABLE IF EXISTS expense;")
    cursor.execute("DROP TABLE IF EXISTS budget;")

    if test_mode:
        cursor.execute("DROP TABLE IF EXISTS Custom;")

    # Create tables if they do not already exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "category" (
        "name"	str UNIQUE,
        "parent"	int,
        "pk"	INTEGER UNIQUE,
        FOREIGN KEY("parent") REFERENCES "category",
        PRIMARY KEY("pk" AUTOINCREMENT)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "expense" (
        "amount"  Decimal NOT NULL,
        "category"	int NOT NULL,
        "expense_date"	datetime NOT NULL,
        "added_date"	datetime NOT NULL DEFAULT 'DATE(''now'')',
        "comment"	str,
        "pk"	INTEGER UNIQUE,
        FOREIGN KEY("category") REFERENCES category(pk),
        PRIMARY KEY("pk" AUTOINCREMENT)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "budget" (
        "limit_amount"	Decimal NOT NULL,
        "period_type"	PeriodType NOT NULL UNIQUE,
        "expenses"	Decimal DEFAULT 0,
        "pk"	INTEGER UNIQUE,
        PRIMARY KEY("pk" AUTOINCREMENT)
    );
    """
    )

    # Test data
    category_data = [("Food", 1, None), ("Transport", 2, None), ("Utilities", 3, None)]

    expense_data = [
        (
            1,
            454,
            1,
            "2024-04-03 01:48:50.826683",
            "2024-04-05 01:48:50.826683",
            "Groceries",
        ),
        (
            2,
            4533,
            2,
            "2024-04-04 01:48:50.826683",
            "2024-04-05 01:48:50.826683",
            "Bus ticket",
        ),
        (
            3,
            4353,
            3,
            "2024-04-05 01:48:50.826683",
            "2024-04-05 01:48:50.826683",
            "Electricity bill",
        ),
        (
            4,
            4353,
            3,
            "2024-04-06 01:48:50.826683",
            "2024-04-05 01:48:50.826683",
            "Electricity bill",
        ),
    ]

    budget_data = [
        (1, PeriodType.DAY, "1000"),
        (2, PeriodType.WEEK, "7000"),
        (3, PeriodType.MONTH, "30000"),
    ]

    # Insert data into the category table
    cursor.executemany(
        "INSERT INTO category (name, pk, parent) VALUES (?, ?, ?)", category_data
    )

    # Insert data into the expense table
    cursor.executemany(
        "INSERT INTO expense (pk, amount, category, expense_date, \
        added_date, comment) VALUES (?, ?, ?, ?, ?, ?)",
        expense_data,
    )

    # Insert data into the budget table
    cursor.executemany(
        "INSERT INTO budget (pk, period_type, limit_amount) VALUES (?, ?, ?)",
        budget_data,
    )

    # Save changes to the database
    conn.commit()

    # Close connection to the database
    conn.close()
