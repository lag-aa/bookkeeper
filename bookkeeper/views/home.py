from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from bookkeeper.views.budget.budget_veiw import BudgetWidget
from bookkeeper.views.category.category_view import CategoryWidget
from bookkeeper.views.expense.expense_view import ExpenseWidget
from bookkeeper.controllers.category_controller import CategoryController
from bookkeeper.controllers.expense_controller import ExpenseController
from bookkeeper.controllers.budget_controller import BudgetController


class MainWindow(QMainWindow):
    """
    Main window for managing expenses.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        super().__init__()
        self.setWindowTitle("bookkeeper - Управление расходами")
        self.resize(800, 600)  # Change window size upon opening

        # Create widgets
        self.budget_widget = BudgetWidget()
        self.new_expense_widget = ExpenseWidget()
        self.category_widget = CategoryWidget()

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Add tab widgets
        self.tab_widget.addTab(self.new_expense_widget, "Список расходов")
        self.tab_widget.addTab(self.budget_widget, "Бюджет")
        self.tab_widget.addTab(self.category_widget, "Категории")

        # Set tab widget as central widget of the main window
        self.setCentralWidget(self.tab_widget)

        # Connect controllers to views
        CategoryController(view=self.category_widget)
        ExpenseController(view=self.new_expense_widget)
        BudgetController(view=self.budget_widget)
