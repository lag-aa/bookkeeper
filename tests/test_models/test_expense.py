"""
Тесты для модели расходов
"""

import pytest
from datetime import datetime
from decimal import Decimal
from bookkeeper.models.expense import Expense


@pytest.fixture
def sample_expense():
    return Expense(amount=Decimal("100.50"), category=1)


def test_create_object(sample_expense):
    assert sample_expense.amount == Decimal("100.50")
    assert sample_expense.category == 1
    assert isinstance(sample_expense.expense_date, datetime)
    assert isinstance(sample_expense.added_date, datetime)
    assert sample_expense.comment == ""
    assert sample_expense.pk == 0


def test_create_with_full_args_list():
    date = datetime.now()
    expense = Expense(
        amount=Decimal("200"),
        category=1,
        expense_date=date,
        added_date=date,
        comment="test",
        pk=1,
    )
    assert expense.amount == Decimal("200")
    assert expense.category == 1
    assert expense.comment == "test"
    assert expense.expense_date == date
    assert expense.added_date == date
    assert expense.pk == 1


def test_reassign():
    """
    class should not be frozen
    """
    date = datetime.now()
    expense = Expense(amount=Decimal("100.50"), category=1)
    expense.amount = Decimal("245")
    expense.category = 2
    expense.expense_date = date
    expense.comment = "Test reassign"
    assert expense.amount == Decimal("245")
    assert expense.category == 2
    assert expense.expense_date == date
    assert expense.comment == "Test reassign"


def test_eq(sample_expense):
    """
    class should implement __eq__ method
    """
    date = datetime.now()
    expense = Expense(
        amount=Decimal("100.50"), category=1, expense_date=date, added_date=date
    )
    sample_expense.expense_date = date
    sample_expense.added_date = date
    assert expense == sample_expense
