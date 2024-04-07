from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from bookkeeper.views.budget.budget_veiw import BudgetWidget
from bookkeeper.views.category.category_view import CategoryWidget
from bookkeeper.views.expense.expense_view import ExpenseListWidget
from bookkeeper.views.expense.expense_view import NewExpenseWidget
from bookkeeper.controllers.category_controller import CategoryController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("bookkeeper - Управление расходами")
        self.resize(800, 600)  # Изменение размера окна при открытии

        # Создание виджетов
        self.expense_list_widget = ExpenseListWidget()
        self.budget_widget = BudgetWidget()
        self.new_expense_widget = NewExpenseWidget()
        self.category_widget = CategoryWidget()

        # Создание виджета вкладок
        self.tab_widget = QTabWidget()

        # Добавление виджетов вкладок
        self.tab_widget.addTab(self.expense_list_widget, "Список расходов")
        self.tab_widget.addTab(self.budget_widget, "Бюджет")
        self.tab_widget.addTab(self.new_expense_widget, "Новый расход")
        self.tab_widget.addTab(self.category_widget, "Категории")

        # Установка виджета вкладок как центрального виджета главного окна
        self.setCentralWidget(self.tab_widget)

        category_controller = CategoryController(view=self.category_widget)
        category_controller.view.show()
