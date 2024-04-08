from bookkeeper.services.expense_service import ExpenseService
from bookkeeper.views.expense.expense_view import ExpenseWidget
from bookkeeper.services.category_service import CategoryService
from bookkeeper.models.expense import Expense


class ExpenseController:
    """
    Controller for managing expenses.
    """

    def __init__(
        self, view: ExpenseWidget = None, expense_service: ExpenseService = None
    ):
        """
        Initializes the ExpenseController.

        Args:
            view (ExpenseWidget): The expense view widget.
            expense_service (ExpenseService): The expense service.
        """
        self.view = view or ExpenseWidget()
        self.expense_service = expense_service or ExpenseService()
        self.category_services = CategoryService()
        self.populate_expenses()
        self.populate_categories()

        self.view.bind_add_expense(self.add_expense)
        self.view.bind_delete_expense(self.delete_expense)
        self.view.bind_edit_expense(self.edit_expense)

    def populate_expenses(self) -> None:
        """
        Populates the expense view with expenses.
        """
        expenses = self.expense_service.get_all()
        self.view.populate_expenses(expenses)

    def populate_categories(self) -> None:
        """
        Populates the category combo box with categories.
        """
        categories = self.category_services.get_all()
        self.view.populate_categories(categories)

    def add_expense(self, expense: Expense) -> None:
        """
        Adds a new expense.

        Args:
            expense (Expense): The expense to add.
        """
        self.expense_service.add(expense)
        self.populate_expenses()

    def edit_expense(self, expense: Expense) -> None:
        """
        Edits an existing expense.

        Args:
            expense (Expense): The updated expense.
        """
        self.expense_service.update(expense)
        self.populate_expenses()

    def delete_expense(self, pk: int) -> None:
        """
        Deletes an expense.

        Args:
            pk (int): The ID of the expense to delete.
        """
        self.expense_service.delete(pk)
        self.populate_expenses()
