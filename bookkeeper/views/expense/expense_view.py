from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHeaderView,
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
)


class ExpenseListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Expense List Widget"))

        expenses_table = QTableWidget(4, 20)
        expenses_table.setColumnCount(4)
        expenses_table.setRowCount(20)
        expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split()
        )

        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        expenses_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        expenses_table.verticalHeader().hide()

        def set_data(data: list[list[str]]):
            for i, row in enumerate(data):
                for j, x in enumerate(row):
                    expenses_table.setItem(i, j, QTableWidgetItem(x.capitalize()))
                    

        layout.addWidget(expenses_table)
        # Здесь вы можете добавить элементы управления для отображения списка расходов и функциональность для редактирования


class NewExpenseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("New Expense Widget"))
        # Здесь вы можете добавить элементы управления для добавления нового расхода
