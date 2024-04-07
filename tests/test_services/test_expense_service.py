import pytest
from datetime import datetime
from decimal import Decimal
from bookkeeper.models.expense import Expense
from bookkeeper.services.expense_service import ExpenseService
from bookkeeper.scripts.create_db import create_database
from bookkeeper.repository.expense_repository import ExpenseRepository


@pytest.fixture()
def repo():
    create_database("test.db", True)
    return ExpenseRepository("test.db")


@pytest.fixture
def expense_service(repo):
    return ExpenseService(repo)


def test_can_add_to_store(expense_service):
    expense = Expense(100, 1)
    pk = expense_service.add(expense)
    assert expense.pk == pk


def test_get_expense_by_pk(expense_service):
    expense = Expense(100, 1)
    pk = expense_service.add(expense)
    assert expense.pk == pk
    assert expense == expense
    assert expense_service.get(-12312) is None


def test_get_all_expenses(expense_service):
    expense_service.add(Expense(100, 1))
    pk = expense_service.add(Expense(200, 2))
    expense_service.add(Expense(300, 3))
    expenses_list = expense_service.get_all(where={"amount": 200})
    assert expenses_list[0].pk == pk
    assert len(expenses_list) == 1


def test_update_expense(expense_service):
    expense = Expense(100, 1)
    pk = expense_service.add(expense)
    expense.comment = "Hello, It's me"
    expense.amount = 200
    expense_service.update(expense)
    expense_from_store = expense_service.get(pk)
    assert expense_from_store.comment == "Hello, It's me"
    assert expense_from_store.amount == 200


def test_delete_expense(expense_service):
    expense = Expense(100, 1)
    pk = expense_service.add(expense)
    result = expense_service.delete(pk)
    assert result is None
    assert expense_service.get(pk) is None


def test_get_total_expense_for_period(expense_service):
    today = datetime.now()
    expense_service.add(Expense(5000, 1, expense_date=today))
    total = expense_service.get_total_expense_for_period(today, today)
    assert total != Decimal(0)
    assert total >= 5000
