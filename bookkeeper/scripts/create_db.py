import sqlite3


def create_database(db_name: str = None, test_mode: bool = False):
    """
    Функция предназначена для создания БД, таблиц и заполнения их данными

    Parameters
    ----------
    db_file - Название (путь к) БД
    test_mode - Режим тестирования, если True будут созданы таблицы для тестирования

    Exceptions
    ----------
    TypeError -  Если параметр db_file равен None или не передан.
    """
    if not db_name:
        raise TypeError(
            "Параметр 'db_file' является обязательным и не может быть None."
        )

    # Создание подключения к базе данных
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Удаление всех таблиц из базы данных
    cursor.execute("DROP TABLE IF EXISTS category;")
    cursor.execute("DROP TABLE IF EXISTS expense;")
    cursor.execute("DROP TABLE IF EXISTS budget;")

    if test_mode:
        cursor.execute("DROP TABLE IF EXISTS Custom;")

        # cursor.execute(
        #     """
        # CREATE TABLE "Custom" (
        #     "name"	TEXT NOT NULL,
        #     "pk"	INTEGER UNIQUE,
        #     PRIMARY KEY("pk")
        #     );
        # """
        # )

    # Создание таблиц, если они еще не существуют
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "category" (
        "name"	TEXT NOT NULL UNIQUE,
        "parent"	INTEGER,
        "pk"	INTEGER NOT NULL UNIQUE,
        FOREIGN KEY("parent") REFERENCES "category",
        PRIMARY KEY("pk")
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "expense" (
        "amount"  INTEGER NOT NULL,
        "category"	INTEGER NOT NULL,
        "expense_date"	TEXT NOT NULL,
        "added_date"	TEXT NOT NULL DEFAULT 'DATE(''now'')',
        "comment"	TEXT,
        "pk"	INTEGER NOT NULL UNIQUE,
        PRIMARY KEY("pk")
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS "budget" (
        "limit_amount"	INTEGER NOT NULL,
        "period_type"	TEXT NOT NULL UNIQUE,
        "pk"	INTEGER NOT NULL UNIQUE,
        PRIMARY KEY("pk")
    );
    """
    )

    # Тестовые данные
    category_data = [("Еда", 1, None), ("Траснпорт", 2, None), ("ЖКХ", 3, None)]

    expense_data = [
        (
            1,
            454,
            1,
            "2024-04-05 01:48:50.826683",
            "2024-04-05 01:48:50.826683",
            "Groceries",
        ),
        (
            2,
            4533,
            2,
            "2024-04-05 01:48:50.826683",
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
    ]

    budget_data = [
        (1, "День", "1000"),
        (2, "Неделя", "7000"),
        (3, "Месяц", "30000"),
    ]

    # Вставка данных в таблицу category
    cursor.executemany(
        "INSERT INTO category (name, pk, parent) VALUES (?, ?, ?)", category_data
    )

    # Вставка данных в таблицу expense
    cursor.executemany(
        "INSERT INTO expense (pk, amount, category, expense_date, \
        added_date, comment) VALUES (?, ?, ?, ?, ?, ?)",
        expense_data,
    )

    # Вставка данных в таблицу budget
    cursor.executemany(
        "INSERT INTO budget (pk, period_type, limit_amount) VALUES (?, ?, ?)",
        budget_data,
    )

    # Сохранение изменений в базе данных
    conn.commit()

    # Закрытие подключения к базе данных
    conn.close()
