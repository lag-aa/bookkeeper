"""
Модель Бюджета
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class PeriodType(str, Enum):
    """
    Enum класс для описания возможные значений типа периода
    """

    day = "day"
    week = "week"
    month = "month"


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    limit_amount - сумма ограничения бюджета
    period_type - тип периода (день/неделя/месяц)
    pk - id записи в базе данных
    """

    limit_amount: Decimal
    period_type: PeriodType
    pk: int = 0
