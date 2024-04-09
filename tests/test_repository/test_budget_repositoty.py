import pytest
from decimal import Decimal
from bookkeeper.repository.budget_repository import BudgetRepository


@pytest.fixture
def repo():
    return BudgetRepository("test.db")


def test_get_with_expenses(repo):
    """Test the 'get_with_expenses' method of the BudgetRepository."""
    budget = repo.get_all()
    budget_with_expense = repo.get_with_expenses(budget[0].pk)
    assert budget_with_expense.expenses != Decimal(0)
