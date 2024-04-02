"""
Модель отчета о расходах за определенный период
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExpenseReport:
    """
    Отчет о расхода за определенный период
    period_type - тип периода (день/неделя/месяц)
    """

    period_type: str
    total_expense: Decimal
    limit_amount: Decimal
