from bookkeeper.services.budget_service import BudgetService
from bookkeeper.views.budget.budget_veiw import BudgetWidget
from bookkeeper.models.budget import Budget


class BudgetController:
    """
    Controller for managing budgets.
    """

    def __init__(
        self, view: BudgetWidget = None, expense_service: BudgetService = None
    ):
        """
        Initializes the BudgetController.

        Args:
            view (BudgetWidget): The budget view widget.
            expense_service (BudgetService): The budget service.
        """
        self.view = view or BudgetWidget()
        self.budget_service = expense_service or BudgetService()
        self.view.bind_add_budget(self.add_budget)
        self.view.bind_delete_budget(self.delete_budget)
        self.view.bind_update_view(self.populate_budgets)

    def populate_budgets(self) -> None:
        """
        Populates the budget view with all budgets.
        """
        budgets = self.budget_service.get_all_with_expenses()
        self.view.populate_budgets(budgets)

    def add_budget(self, budget: Budget) -> None:
        """
        Adds a new budget.

        Args:
            budget (Budget): The budget object to add.
        """
        self.budget_service.add(budget)
        self.populate_budgets()

    def edit_budget(self, budget: Budget) -> None:
        """
        Edits an existing budget.

        Args:
            budget (Budget): The updated budget object.
        """
        self.budget_service.update(budget)
        self.populate_budgets()

    def delete_budget(self, pk: int) -> None:
        """
        Deletes a budget.

        Args:
            pk (int): The ID of the budget to delete.
        """
        self.budget_service.delete(pk)
        self.populate_budgets()
