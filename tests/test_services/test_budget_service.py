import pytest
from decimal import Decimal
from bookkeeper.models.budget import Budget, PeriodType
from bookkeeper.models.expense import Expense
from bookkeeper.services.budget_service import BudgetService
from bookkeeper.services.expense_service import ExpenseService
from bookkeeper.scripts.create_db import create_database
from bookkeeper.repository.sqlite_repository import SQLiteRepository


@pytest.fixture()
def repo():
    create_database("test.db", True)
    return SQLiteRepository(Budget, "test.db")


@pytest.fixture
def budget_service(repo):
    return BudgetService(repo)


def test_crud(budget_service):
    budget_service.delete(1)
    assert budget_service.get(1) is None

    budget = Budget(Decimal(500), "День")
    pk = budget_service.add(budget)
    budget_new = budget_service.get(pk)

    assert budget.limit_amount == budget_new.limit_amount
    assert budget.period_type == budget_new.period_type

    budget_new.limit_amount = 345
    budget_service.update(budget_new)
    budget_upd = budget_service.get(pk)

    assert budget_upd.pk == budget_new.pk
    assert budget_upd.limit_amount == budget_new.limit_amount
    assert budget_upd.period_type == budget_new.period_type


def test_get_with_expenses(budget_service):
    budget = budget_service.get_with_expenses("Год")
    ExpenseService().add(Expense(Decimal(1000), category=0))
    budget_by_day = budget_service.get_with_expenses(PeriodType.DAY)
    assert budget is None
    assert budget_by_day.expenses >= Decimal(1000)


def test_get_budget_by_pk(budget_service):
    budget_from_store = budget_service.get(1)
    assert budget_from_store.pk == 1
    assert budget_service.get(-12312) is None


def test_get_all_budget(budget_service):
    budgets_list = budget_service.get_all(where={"period_type": "Неделя"})
    assert budgets_list[0].pk is not None
    assert budgets_list[0].period_type == PeriodType.WEEK


def test_update_budget(budget_service):
    budgets = budget_service.get_all()
    if budgets:
        budget = budgets[0]
    else:
        budget = Budget(Decimal("10000"), PeriodType.WEEK)
        budget_service.add(budget)
    pk = budget.pk
    budget.limit_amount = Decimal("200")
    budget_service.update(budget)
    budget_from_store = budget_service.get(pk)
    assert budget_from_store.limit_amount == Decimal("200")


def test_delete_budget(budget_service):
    budgets = budget_service.get_all()
    if budgets:
        budget = budgets[0]
    else:
        budget = Budget(Decimal("10000"), PeriodType.WEEK)
        budget_service.add(budget)
    pk = budget.pk
    result = budget_service.delete(pk)
    assert result is None
    assert budget_service.get(pk) is None
