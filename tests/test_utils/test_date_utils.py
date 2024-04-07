import pytest
from bookkeeper.utils.date_utils import get_week_boundaries
from bookkeeper.utils.date_utils import get_month_boundaries
from datetime import datetime


def test_get_week_boundaries():
    """Test if the start and end dates of the week are correctly calculated."""
    test_date = datetime(2024, 4, 7, 0, 0, 0, 0)
    start_date = datetime(2024, 4, 1, 0, 0, 0, 0)
    end_date = datetime(2024, 4, 7, 23, 59, 59, 999999)
    assert (start_date, end_date) == get_week_boundaries(test_date)


def test_get_week_boundaries_none_argument():
    """Test if ValueError is raised when None is passed as argument."""
    with pytest.raises(ValueError):
        get_week_boundaries(None)


def test_get_week_boundaries_wrong_argument_type():
    """Test if TypeError is raised when argument of wrong type is passed."""
    with pytest.raises(TypeError):
        get_week_boundaries("2024-04-01")


def test_get_week_boundaries_sunday_start():
    """Test if the function correctly handles a day with Sunday as the start of the week."""
    start_date, end_date = get_week_boundaries(datetime(2024, 4, 7))
    assert start_date == datetime(2024, 4, 1, 0, 0, 0, 0)
    assert end_date == datetime(2024, 4, 7, 23, 59, 59, 999999)


def test_get_week_boundaries_monday_start():
    """Test if the function correctly handles a day with Monday as the start of the week."""
    start_date, end_date = get_week_boundaries(datetime(2024, 4, 1))
    assert start_date == datetime(2024, 4, 1, 0, 0, 0, 0)
    assert end_date == datetime(2024, 4, 7, 23, 59, 59, 999999)


def test_get_month_boundaries():
    """Test if the start and end dates of the week are correctly calculated."""
    test_date = datetime(2024, 4, 7, 0, 0, 0, 0)
    start_date = datetime(2024, 4, 1, 0, 0, 0, 0)
    end_date = datetime(2024, 4, 30, 23, 59, 59, 999999)
    assert (start_date, end_date) == get_month_boundaries(test_date)


# Test for exception when passing None as argument
def test_get_month_boundaries_none_argument():
    """Test if ValueError is raised when None is passed as argument."""
    with pytest.raises(ValueError):
        get_month_boundaries(None)


# Test for exception when passing argument of wrong type
def test_get_month_boundaries_wrong_argument_type():
    """Test if TypeError is raised when argument of wrong type is passed."""
    with pytest.raises(TypeError):
        get_month_boundaries("2024-04-01")


# Test for correct handling of day with start of month in February
def test_get_month_boundaries_february_start():
    """Test if the function correctly handles a day with the start of the month in February."""
    start_date, end_date = get_month_boundaries(datetime(2024, 2, 29))
    assert start_date.date() == datetime(2024, 2, 1).date()
    assert end_date.date() == datetime(2024, 2, 29).date()


# Test for correct handling of day with start of month in December
def test_get_month_boundaries_december_start():
    """Test if the function correctly handles a day with the start of the month in December."""
    start_date, end_date = get_month_boundaries(datetime(2023, 12, 20))
    assert start_date.date() == datetime(2023, 12, 1).date()
    assert end_date.date() == datetime(2023, 12, 31).date()
