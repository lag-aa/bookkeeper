from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QMenu,
    QLineEdit,
    QHeaderView,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt
from decimal import Decimal
from bookkeeper.models.budget import Budget, PeriodType
from bookkeeper.utils.error_handling import handle_error


class BudgetWidget(QWidget):
    """
    Widget for managing budgets.
    """

    def __init__(self, parent=None):
        """
        Initializes the BudgetWidget.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(4)
        self.budget_table.setHorizontalHeaderLabels(["", "Период", "Расходы", "Лимит"])
        self.budget_table.setColumnHidden(0, True)
        self.budget_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.budget_table.customContextMenuRequested.connect(self.show_context_menu)
        self.budget_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.budget_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.add_period_type_label = QLabel("Период:")
        self.period_type_combo = QComboBox()
        self.add_amount_limit_label = QLabel("Лимит:")
        self.add_amount_limit = QLineEdit()

        for period in PeriodType:
            self.period_type_combo.addItem(period.value, period)

        self.add_budget_button = QPushButton("Добавить")

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.add_period_type_label)
        form_layout.addWidget(self.period_type_combo)
        form_layout.addWidget(self.add_amount_limit_label)
        form_layout.addWidget(self.add_amount_limit)
        form_layout.addWidget(self.add_budget_button)

        layout = QVBoxLayout()
        layout.addWidget(self.budget_table)
        layout.addLayout(form_layout)

        self.setLayout(layout)
        self.add_budget_button.clicked.connect(self.add_budget)

    def showEvent(self, event):
        """
        Overrides the QWidget showEvent method.
        """
        super().showEvent(event)
        self.handle_update_view()

    def bind_add_budget(self, handler):
        """
        Binds the add_budget handler.

        Args:
            handler: Handler function for adding budget.
        """
        self.handle_add_budget = handle_error(self, handler=handler)

    def bind_delete_budget(self, handler):
        """
        Binds the delete_budget handler.

        Args:
            handler: Handler function for deleting budget.
        """
        self.handle_delete_budget = handle_error(self, handler=handler)

    def bind_update_view(self, handler):
        """
        Binds the update_view handler.

        Args:
            handler: Handler function for updating view.
        """
        self.handle_update_view = handle_error(self, handler=handler)

    def populate_budgets(self, budgets):
        """
        Populates the budget table with budgets.

        Args:
            budgets: List of budgets.
        """
        self.budget_table.setRowCount(len(budgets))
        for row, budget in enumerate(budgets):
            self.budget_table.setItem(row, 0, QTableWidgetItem(str(budget.pk)))
            self.budget_table.setItem(
                row, 1, QTableWidgetItem(str(budget.period_type.value))
            )
            self.budget_table.setItem(row, 2, QTableWidgetItem(str(budget.expenses)))
            self.budget_table.setItem(
                row, 3, QTableWidgetItem(str(budget.limit_amount))
            )

    def add_budget(self):
        """
        Adds a new budget.
        """
        # TODO Crutch, replace it
        try:
            period_type = self.period_type_combo.currentData()
            limit_amount = Decimal(self.add_amount_limit.text())

            budget = Budget(limit_amount, period_type)
            self.handle_add_budget(budget)
        except Exception as ex:
            QMessageBox.critical(self, "Ошибка", str(ex))

    def show_context_menu(self, pos):
        """
        Displays the context menu for the budget table.

        Args:
            pos: Position of the context menu.
        """
        context_menu = QMenu()
        delete_action = context_menu.addAction("Удалить")
        delete_action.triggered.connect(self.delete_budget)
        context_menu.exec_(self.budget_table.mapToGlobal(pos))

    def delete_budget(self):
        """
        Deletes the selected budget.
        """
        selected_row = self.budget_table.currentRow()

        if selected_row >= 0:
            pk = int(self.budget_table.item(selected_row, 0).text())
            self.handle_delete_budget(pk)
