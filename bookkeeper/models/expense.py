"""
Expense Operation Model
"""

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime


@dataclass()
class Expense:
    """
    Expense operation model.

    Attributes:
        amount (int): The amount of the expense.
        category (int): The ID of the expense category.
        expense_date (datetime): The date of the expense (default is current datetime).
        added_date (datetime): The date added to the database (default is current datetime).
        comment (str): Optional comment for the expense.
        pk (int): The record ID in the database.
    """

    amount: Decimal
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ""
    pk: int = 0
