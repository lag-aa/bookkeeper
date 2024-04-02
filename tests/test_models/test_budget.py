"""
Тесты для модели Бюджета
"""

import pytest
from decimal import Decimal
from bookkeeper.models.budget import Budget


@pytest.fixture
def sample_budget():
    return Budget(limit_amount=Decimal("1000.45"), period_type="day")


def test_create_object(sample_budget):
    assert sample_budget.limit_amount == Decimal("1000.45")
    assert sample_budget.period_type == "day"
    assert sample_budget.pk == 0


def test_reassign():
    """
    class should not be frozen
    """
    budget = Budget(limit_amount=Decimal("1000.45"), period_type="day")
    budget.limit_amount = Decimal("245")
    budget.period_type = "week"
    assert budget.limit_amount == Decimal("245")
    assert budget.period_type == "week"


def test_eq(sample_budget):
    """
    class should implement __eq__ method
    """
    budget = Budget(limit_amount=Decimal("1000.45"), period_type="day")
    assert budget == sample_budget
