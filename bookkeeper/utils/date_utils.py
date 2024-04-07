"""
Utilities for working with dates
"""

from datetime import datetime, timedelta


def get_week_boundaries(day: datetime) -> tuple[datetime, datetime]:
    """
    Get the start and end dates of the week based on the specified day.

    Parameters:
        day (datetime): The day for which to find the dates.

    Returns:
        tuple[datetime, datetime]: Tuple containing the start and end dates of the week.
    """
    if day is None:
        raise ValueError("Argument 'day' cannot be None.")

    if not isinstance(day, datetime):
        raise TypeError("Argument 'day' must be of type datetime.")

    weekday = day.weekday()
    min_time = datetime.min.time()
    max_time = datetime.max.time()
    start_of_week = datetime.combine(day - timedelta(days=weekday), min_time)
    end_of_week = datetime.combine(start_of_week + timedelta(days=6), max_time)
    return start_of_week, end_of_week


def get_month_boundaries(day: datetime) -> tuple[datetime, datetime]:
    """
    Get the start and end dates of the month based on the specified day.

    Parameters:
        day (datetime): The day for which to find the dates.

    Returns:
        tuple[datetime, datetime]: Tuple containing the start and end dates of the month.
    """
    if day is None:
        raise ValueError("Argument 'day' cannot be None.")

    if not isinstance(day, datetime):
        raise TypeError("Argument 'day' must be of type datetime.")

    min_time = datetime.min.time()
    max_time = datetime.max.time()
    start_of_month = datetime.combine(day.replace(day=1).date(), min_time)
    next_month = (start_of_month + timedelta(weeks=5)).replace(day=1).date()
    end_of_month = datetime.combine(next_month - timedelta(days=1), max_time)
    return start_of_month, end_of_month
