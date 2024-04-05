"""
Тесты для модели Бюджета
"""

import pytest
from decimal import Decimal
from bookkeeper.models.budget import Budget
from datetime import datetime, date
from bookkeeper.models.budget import PeriodType


@pytest.fixture
def sample_budget():
    return Budget(limit_amount=Decimal("1000.45"), period_type=PeriodType.DAY)


def test_create_object(sample_budget):
    assert sample_budget.limit_amount == Decimal("1000.45")
    assert sample_budget.period_type == PeriodType.DAY
    assert sample_budget.pk == 0


def test_reassign():
    """
    class should not be frozen
    """
    budget = Budget(limit_amount=Decimal("1000.45"), period_type=PeriodType.DAY)
    budget.limit_amount = Decimal("245")
    budget.period_type = PeriodType.WEEK
    assert budget.limit_amount == Decimal("245")
    assert budget.period_type == PeriodType.WEEK


def test_eq(sample_budget):
    """
    class should implement __eq__ method
    """
    budget = Budget(limit_amount=Decimal("1000.45"), period_type=PeriodType.DAY)
    assert budget == sample_budget


def test_period_dates_day():
    budget_day = Budget(limit_amount=Decimal("5000"), period_type=PeriodType.DAY)
    start_date, end_date = budget_day.period_dates
    assert isinstance(start_date, date)
    assert isinstance(end_date, date)
    assert start_date == datetime.now().date()
    assert end_date == datetime.now().date()


def test_period_dates_week():
    budget_week = Budget(limit_amount=Decimal("5000"), period_type=PeriodType.WEEK)
    start_date, end_date = budget_week.period_dates
    assert isinstance(start_date, date)
    assert isinstance(end_date, date)
    assert start_date <= datetime.now().date() <= end_date


def test_period_dates_month():
    budget_month = Budget(limit_amount=Decimal("5000"), period_type=PeriodType.MONTH)
    start_date, end_date = budget_month.period_dates
    assert isinstance(start_date, date)
    assert isinstance(end_date, date)
    assert start_date <= datetime.now().date() <= end_date
