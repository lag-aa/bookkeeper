import pytest
from bookkeeper.models.budget import Budget
from bookkeeper.services.budget_service import BudgetService
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
    budget = Budget(1500, "Год")
    pk = budget_service.add(budget)
    budget_new = budget_service.get(pk)

    assert budget.limit_amount == budget_new.limit_amount
    assert budget.period_type == budget_new.period_type

    budget_new.limit_amount = 345
    print(budget_new)

    budget_service.update(budget_new)

    print(budget_new)

    budget_upd = budget_service.get(pk)
    assert budget_upd.pk == budget_new.pk
    assert budget_upd.limit_amount == budget_new.limit_amount
    assert budget_upd.period_type == budget_new.period_type
    budget_service.delete(pk)
    assert budget_service.get(pk) is None


# def test_can_add_to_store(budget_service):
#     budget = Budget(Decimal("1500"), "day")
#     pk = budget_service.add(budget)
#     assert budget.pk == pk


# def test_get_budget_by_pk(budget_service):
#     budget = Budget(Decimal("1500"), "day")
#     pk = budget_service.add(budget)
#     budget_from_store = budget_service.get(pk)
#     assert budget_from_store.pk == pk
#     assert budget == budget_from_store
#     assert budget_service.get(-12312) is None


# def test_get_all_budget(budget_service):
#     budget_service.add(Budget(Decimal("100"), "day"))
#     pk = budget_service.add(Budget(Decimal("200"), "week"))
#     budget_service.add(Budget(Decimal("300"), "month"))
#     budgets_list = budget_service.get_all(where={"period_type": "week"})
#     assert budgets_list[0].pk == pk, "Проверка фильтрации"
#     assert len(budgets_list) == 1


# def test_update_budget(budget_service):
#     budget = Budget(Decimal("10000"), "week")
#     pk = budget_service.add(budget)
#     budget.limit_amount = Decimal("200")
#     budget.period_type = "day"
#     budget_service.update(budget)
#     budget_from_store = budget_service.get(pk)
#     assert budget_from_store.period_type == "day"
#     assert budget_from_store.limit_amount == Decimal("200")


# def test_delete_budget(budget_service):
#     budget = Budget(Decimal("1500"), "day")
#     pk = budget_service.add(budget)
#     result = budget_service.delete(pk)
#     assert result is None
#     assert budget_service.get(pk) is None
