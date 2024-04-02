import pytest
from decimal import Decimal
from bookkeeper.models.budget import Budget
from bookkeeper.services.budget_service import BudgetService


@pytest.fixture
def budget_service():
    return BudgetService()


def test_can_add_to_store(budget_service):
    budget = Budget(Decimal("1500"), "day")
    pk = budget_service.add(budget)
    assert budget.pk == pk


def test_get_expense_by_pk(budget_service):
    budget = Budget(Decimal("1500"), "day")
    pk = budget_service.add(budget)
    budget_from_store = budget_service.get(pk)
    assert budget_from_store.pk == pk
    assert budget == budget_from_store
    assert budget_service.get(-12312) is None


def test_get_all_expenses(budget_service):
    budget_service.add(Budget(Decimal("100"), "day"))
    pk = budget_service.add(Budget(Decimal("200"), "week"))
    budget_service.add(Budget(Decimal("300"), "month"))
    budgets_list = budget_service.get_all(where={"period_type": "week"})
    assert budgets_list[0].pk == pk, "Проверка фильтрации"
    assert len(budgets_list) == 1


def test_update_expense(budget_service):
    budget = Budget(Decimal("10000"), "week")
    pk = budget_service.add(budget)
    budget.limit_amount = Decimal("200")
    budget.period_type = "day"
    budget_service.update(budget)
    budget_from_store = budget_service.get(pk)
    assert budget_from_store.period_type == "day"
    assert budget_from_store.limit_amount == Decimal("200")


def test_delete_expense(budget_service):
    budget = Budget(Decimal("1500"), "day")
    pk = budget_service.add(budget)
    result = budget_service.delete(pk)
    assert result is None
    assert budget_service.get(pk) is None
