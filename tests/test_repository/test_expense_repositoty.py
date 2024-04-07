from datetime import datetime
import pytest
from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.expense import Expense


@pytest.fixture
def repo():
    return ExpenseRepository("test.db")


def test_get_total_expense_for_period(repo):
    """
    Test case to check the get_total_expense_for_period method with a non-empty result.
    """
    repo.add(Expense(500, 0, datetime(2000, 1, 2)))
    repo.add(Expense(500, 0, datetime(2000, 1, 2)))
    repo.add(Expense(500, 0, datetime(2000, 1, 2)))

    start_date = datetime(2000, 1, 1)
    end_date = datetime(2000, 1, 31)

    total_expense = repo.get_total_expense_for_period(start_date, end_date)
    assert total_expense == 1500


def test_get_total_expense_for_period_empty(repo):
    """
    Test case to check the get_total_expense_for_period method with an empty result.
    """
    start_date = datetime(1899, 1, 1)
    end_date = datetime(1899, 1, 31)

    total_expense = repo.get_total_expense_for_period(start_date, end_date)
    assert total_expense == 0
