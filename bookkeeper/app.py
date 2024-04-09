"""Module for the main entry point of the application."""

# pylint: disable=E0611
import sys
import os
import configparser
from PySide6.QtWidgets import QApplication
from bookkeeper.views.home import MainWindow
from bookkeeper.scripts.create_db import create_database

config = configparser.ConfigParser()
config.read("bookkeeper/config/settings.ini")
db_name = config["sqllite"]["db_name"]


def main():
    """Main function to launch the application."""

    if not os.path.exists(db_name):
        # Если файл не существует, создаем базу данных
        create_database(db_name)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
