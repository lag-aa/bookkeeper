import pytest
from decimal import Decimal
from bookkeeper.models.expense import Expense
from bookkeeper.services.expense_service import ExpenseService


@pytest.fixture
def expense_service():
    return ExpenseService()


def test_can_add_to_store(expense_service):
    expense = Expense(Decimal("100"), 1)
    pk = expense_service.add(expense)
    assert expense.pk == pk


def test_get_expense_by_pk(expense_service):
    expense = Expense(Decimal("100"), 1)
    pk = expense_service.add(expense)
    expense_from_store = expense_service.get(pk)
    print(expense_from_store)
    assert expense_from_store.pk == pk
    assert expense == expense_from_store
    assert expense_service.get(-12312) is None


def test_get_all_expenses(expense_service):
    expense_service.add(Expense(Decimal("100"), 1))
    pk = expense_service.add(Expense(Decimal("200"), 2))
    expense_service.add(Expense(Decimal("300"), 3))
    expenses_list = expense_service.get_all(where={"amount": Decimal("200")})
    assert expenses_list[0].pk == pk, "Проверка фильтрации"
    assert len(expenses_list) == 1


def test_update_expense(expense_service):
    expense = Expense(Decimal("100"), 1)
    pk = expense_service.add(expense)
    expense.comment = "Hello, It's me"
    expense.amount = Decimal("200")
    expense_service.update(expense)
    expense_from_store = expense_service.get(pk)
    assert expense_from_store.comment == "Hello, It's me"
    assert expense_from_store.amount == Decimal("200")


def test_delete_expense(expense_service):
    expense = Expense(Decimal("100"), 1)
    pk = expense_service.add(expense)
    result = expense_service.delete(pk)
    assert result is None
    assert expense_service.get(pk) is None
