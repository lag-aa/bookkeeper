"""
Tests for the Budget model
"""

import pytest
from decimal import Decimal
from datetime import datetime
from freezegun import freeze_time
from bookkeeper.models.budget import Budget
from bookkeeper.models.budget import PeriodType


@pytest.fixture
def sample_budget():
    """
    Fixture that creates a sample Budget instance for testing.
    """
    return Budget(
        limit_amount=Decimal("1000.45"),
        period_type=PeriodType.DAY,
        expenses=Decimal(334),
    )


def test_create_object(sample_budget):
    """
    Test case to ensure object creation and attribute values.
    """
    assert sample_budget.limit_amount == Decimal("1000.45")
    assert sample_budget.period_type == PeriodType.DAY
    assert sample_budget.pk == 0


def test_reassign():
    """
    Test case to ensure object reassignment.
    """
    budget = Budget(limit_amount=Decimal("1000.45"), period_type=PeriodType.DAY)
    budget.limit_amount = Decimal("245")
    budget.period_type = PeriodType.WEEK
    assert budget.limit_amount == Decimal("245")
    assert budget.period_type == PeriodType.WEEK


def test_eq(sample_budget):
    """
    Test case to check the implementation of the __eq__ method.
    """
    budget = Budget(
        limit_amount=Decimal("1000.45"),
        period_type=PeriodType.DAY,
        expenses=Decimal(334),
    )
    assert budget == sample_budget


def test_period_dates_day(sample_budget):
    """
    Test case for period dates calculation for daily periods.
    """
    fake_date = datetime(2024, 4, 5)

    with freeze_time("2024-04-05"):
        start_date, end_date = sample_budget.period_dates
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        assert start_date == datetime.combine(fake_date, datetime.min.time())
        assert end_date == datetime.combine(fake_date, datetime.max.time())


def test_period_dates_week():
    """
    Test case for period dates calculation for weekly periods.
    """
    fake_date = datetime(2024, 4, 5)
    budget_week = Budget(limit_amount=Decimal("5000"), period_type=PeriodType.WEEK)

    with freeze_time("2024-04-05"):
        start_date, end_date = budget_week.period_dates
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        assert start_date <= fake_date <= end_date


def test_period_dates_month():
    """
    Test case for period dates calculation for monthly periods.
    """
    budget_month = Budget(limit_amount=Decimal("5000"), period_type=PeriodType.MONTH)
    start_date, end_date = budget_month.period_dates
    assert isinstance(start_date, datetime)
    assert isinstance(end_date, datetime)
    assert start_date <= datetime.now() <= end_date


def test_period_dates_invalid_type():
    """
    Test case to ensure an invalid period type raises a TypeError.
    """
    with pytest.raises(TypeError):
        budget = Budget(limit_amount=Decimal("5000"), period_type="InvalidPeriodType")
        budget.period_dates
