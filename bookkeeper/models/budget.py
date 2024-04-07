"""
Budget Model
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from datetime import datetime
from bookkeeper.utils.date_utils import get_week_boundaries
from bookkeeper.utils.date_utils import get_month_boundaries


class PeriodType(str, Enum):
    """
    Enum class to describe possible period type values.
    """

    DAY = "День"
    WEEK = "Неделя"
    MONTH = "Месяц"


@dataclass
class Budget:
    """
    Budget data model.

    Attributes:
        limit_amount (int): The limit amount of the budget.
        period_type (PeriodType): The period type (day/week/month).
        pk (int): The record ID in the database.
    """

    limit_amount: Decimal
    period_type: PeriodType
    expenses: Decimal = Decimal(0)
    pk: int = 0

    @property
    def period_dates(self) -> tuple[datetime, datetime]:
        """
        Method to get the start and end dates of the period.

        Returns:
            tuple[date, date]: Start and end dates of the period.
        """
        if not isinstance(self.period_type, PeriodType):
            raise TypeError("self.period_type should be an instance of PeriodType.")

        today = datetime.now()
        morning = datetime.combine(today, datetime.min.time())
        night = datetime.combine(today, datetime.max.time())
        period_dates = {
            PeriodType.DAY: (morning, night),
            PeriodType.WEEK: get_week_boundaries(today),
            PeriodType.MONTH: get_month_boundaries(today),
        }
        return period_dates[self.period_type]
