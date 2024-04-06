"""
Budget Model
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, date
from bookkeeper.utils.utils import get_week_boundaries, get_month_boundaries


class PeriodType(str, Enum):
    """
    Enum class to describe possible period type values.
    """

    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


@dataclass()
class Budget:
    """
    Budget data model.

    Attributes:
        limit_amount (int): The limit amount of the budget.
        period_type (PeriodType): The period type (day/week/month).
        pk (int): The record ID in the database.
    """

    limit_amount: int
    period_type: PeriodType
    pk: int = 0

    @property
    def period_dates(self) -> tuple[date, date]:
        """
        Method to get the start and end dates of the period.

        Returns:
            tuple[date, date]: Start and end dates of the period.
        """
        date_now = datetime.now()
        period_dates = {
            PeriodType.DAY: (date_now.date(), date_now.date()),
            PeriodType.WEEK: get_week_boundaries(date_now),
            PeriodType.MONTH: get_month_boundaries(date_now),
        }
        return period_dates[self.period_type]
