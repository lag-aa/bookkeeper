from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
    QComboBox,
)
from decimal import Decimal
from datetime import datetime


class EditExpenseDialog(QDialog):
    """
    Dialog for editing expense details.
    """

    def __init__(self, parent=None):
        """
        Initializes the EditExpenseDialog.

        Args:
            parent: Parent widget (optional).
        """
        super().__init__(parent)
        self.setWindowTitle("Edit Expense")
        self.resize(500, 200)

        self.amount_label = QLabel("Сумма:")
        self.amount_edit = QLineEdit()
        self.category_label = QLabel("Категории:")
        self.category_combo = QComboBox()
        self.date_label = QLabel("Дата:")
        self.date_edit = QLineEdit()
        self.comment_label = QLabel("Комментарий:")
        self.comment_edit = QLineEdit()
        self.pk = None

        form_layout = QFormLayout()
        form_layout.addRow(self.amount_label, self.amount_edit)
        form_layout.addRow(self.category_label, self.category_combo)
        form_layout.addRow(self.date_label, self.date_edit)
        form_layout.addRow(self.comment_label, self.comment_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def set_data(self, expense, categories):
        """
        Sets the data in the dialog fields.

        Args:
            expense (Expense): The expense object to edit.
            categories (list): List of categories.
        """
        self.amount_edit.setText(str(expense.amount))
        self.date_edit.setText(expense.expense_date.strftime("%Y-%m-%d %H:%M"))
        self.comment_edit.setText(expense.comment)
        self.pk = expense.pk

        for pk, name in categories:
            self.category_combo.addItem(name, pk)

        crx = self.category_combo.findText(expense.category)
        if crx != -1:
            self.category_combo.setCurrentIndex(crx)

    def get_data(self):
        """
        Retrieves the edited data from the dialog.

        Returns:
            dict: Dictionary containing the edited expense data.
        """
        amount = Decimal(self.amount_edit.text())
        category = self.category_combo.currentData()
        date = datetime.strptime(self.date_edit.text(), "%Y-%m-%d %H:%M")
        comment = self.comment_edit.text()
        return {
            "amount": amount,
            "category": category,
            "expense_date": date,
            "comment": comment,
            "pk": self.pk,
        }
