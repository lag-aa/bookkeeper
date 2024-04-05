"""
Модель Бюджета
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, date
from bookkeeper.utils.utils import get_week_boundaries
from bookkeeper.utils.utils import get_month_boundaries


class PeriodType(str, Enum):
    """
    Enum класс для описания возможные значений типа периода
    """

    DAY = "День"
    WEEK = "Неделя"
    MONTH = "Месяц"


@dataclass()
class Budget:
    """
    Бюджет.
    limit_amount - сумма ограничения бюджета
    period_type - тип периода (день/неделя/месяц)
    pk - id записи в базе данных
    """

    limit_amount: int
    period_type: PeriodType
    pk: int = 0

    @property
    def period_dates(self) -> tuple[date, date]:
        """
        Метод для получения даты начала и окончания периода
        """
        date_now = datetime.now()
        period_dates = {
            PeriodType.DAY: (date_now.date(), date_now.date()),
            PeriodType.WEEK: get_week_boundaries(date_now),
            PeriodType.MONTH: get_month_boundaries(date_now),
        }
        return period_dates[self.period_type]
