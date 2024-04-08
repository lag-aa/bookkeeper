from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QDateEdit,
    QComboBox,
    QLabel,
    QMenu,
    QLineEdit,
    QHeaderView,
    QMessageBox,
    QFormLayout,
)
from decimal import Decimal
from datetime import datetime
from PySide6.QtCore import Qt, QDate
from bookkeeper.models.expense import Expense
from bookkeeper.views.expense.expense_edit_dialog import EditExpenseDialog


class ExpenseWidget(QWidget):
    """
    View for managing expenses.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        self.categories = []

        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(
            ["", "Сумма", "Категория", "Дата", "Комментарий"]
        )
        self.expense_table.setColumnHidden(0, True)
        self.expense_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.expense_table.customContextMenuRequested.connect(self.show_context_menu)
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expense_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.add_amount_label = QLabel("Сумма:")
        self.add_amount = QLineEdit()
        self.add_comment_label = QLabel("Комментарий:")
        self.add_comment = QLineEdit()
        self.category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.date_label = QLabel("Дата:")
        self.date_edit = QDateEdit(QDate.currentDate())
        self.add_expense_button = QPushButton("Добавить")

        form_layout = QFormLayout()
        form_layout.addRow(self.add_amount_label, self.add_amount)
        form_layout.addRow(self.category_label, self.category_combo)
        form_layout.addRow(self.date_label, self.date_edit)
        form_layout.addRow(self.add_comment_label, self.add_comment)

        layout = QVBoxLayout()
        layout.addWidget(self.expense_table)
        layout.addLayout(form_layout)
        layout.addWidget(self.add_expense_button)

        self.setLayout(layout)
        self.add_expense_button.clicked.connect(self.add_expense)

    def showEvent(self, event):
        super().showEvent(event)
        self.handle_update_view()

    def bind_add_expense(self, handler):
        """
        Binds the handler function for adding an expense.

        Args:
            handler: Handler function for adding an expense.
        """
        self.handle_add_expense = handler

    def bind_delete_expense(self, handler):
        """
        Binds the handler function for deleting an expense.

        Args:
            handler: Handler function for deleting an expense.
        """
        self.handle_delete_expense = handler

    def bind_edit_expense(self, handler):
        """
        Binds the handler function for editing an expense.

        Args:
            handler: Handler function for editing an expense.
        """
        self.handle_edit_expense = handler

    def bind_update_view(self, handler):
        """
        Binds the handler function for updating the view.

        Args:
            handler: Handler function for updating the view.
        """
        self.handle_update_view = handler

    def populate_expenses(self, expenses):
        """
        Populates the expense table with fake expenses for testing.
        """
        self.expense_table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            self.expense_table.setItem(row, 0, QTableWidgetItem(str(expense.pk)))
            self.expense_table.setItem(row, 1, QTableWidgetItem(str(expense.amount)))
            self.expense_table.setItem(row, 2, QTableWidgetItem(str(expense.category)))
            self.expense_table.setItem(
                row,
                3,
                QTableWidgetItem(expense.expense_date.strftime("%Y-%m-%d %H:%M")),
            )
            self.expense_table.setItem(row, 4, QTableWidgetItem(expense.comment))

    def populate_categories(self, categories):
        """
        Populates the category combo box with fake categories for testing.
        """
        self.categories.clear()
        self.category_combo.clear()
        for category in categories:
            self.categories.append((category.pk, category.name))
            self.category_combo.addItem(category.name, category.pk)

    def add_expense(self):
        """
        Adds a new expense based on the input fields.
        """
        amount = Decimal(self.add_amount.text())
        category = self.category_combo.currentData()
        expense_date = self.date_edit.dateTime().toPython()
        comment = self.add_comment.text()

        expense = Expense(amount, category, expense_date, comment=comment)
        self.handle_add_expense(expense)

    def show_context_menu(self, pos):
        """
        Displays the context menu for the expense table.
        """
        context_menu = QMenu()
        delete_action = context_menu.addAction("Удалить")
        edit_action = context_menu.addAction("Редактировать")
        delete_action.triggered.connect(self.delete_expense)
        edit_action.triggered.connect(self.edit_expense)
        context_menu.exec_(self.expense_table.mapToGlobal(pos))

    def delete_expense(self):
        """
        Deletes the selected expense from the database.
        """
        selected_row = self.expense_table.currentRow()

        if selected_row >= 0:
            pk = int(self.expense_table.item(selected_row, 0).text())
            self.handle_delete_expense(pk)

    def set_data(self, expense):
        self.amount_edit.setText(str(expense.amount))
        self.category_edit.setText(str(expense.category))
        self.date_edit.setText(expense.expense_date.strftime("%Y-%m-%d %H:%M"))
        self.comment_edit.setText(expense.comment)

    def edit_expense(self):
        """
        Opens the Edit Expense dialog.
        """
        selected_row = self.expense_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an expense to edit.")
            return

        expense = Expense(
            amount=Decimal(self.expense_table.item(selected_row, 1).text()),
            category=self.expense_table.item(selected_row, 2).text(),
            expense_date=datetime.strptime(
                self.expense_table.item(selected_row, 3).text(), "%Y-%m-%d %H:%M"
            ),
            comment=self.expense_table.item(selected_row, 4).text(),
            pk=int(self.expense_table.item(selected_row, 0).text()),
        )

        dialog = EditExpenseDialog()
        dialog.set_data(expense, self.categories)

        if dialog.exec_():
            updated_data = dialog.get_data()
            self.handle_edit_expense(Expense(**updated_data))
