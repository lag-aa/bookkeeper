"""Module for the main entry point of the application."""

# pylint: disable=E0611
import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.views.home import MainWindow


def main():
    """Main function to launch the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
