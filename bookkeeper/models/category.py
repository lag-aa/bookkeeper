"""
Category Model
"""

from dataclasses import dataclass


@dataclass()
class Category:
    """
    Сategory model.

    Attributes:
        name (str): The name of the category.
        parent (int | None): The ID of the parent category (None for top-level categories).
        pk (int): The record ID in the database.
    """

    name: str
    parent: int | None = None
    pk: int = 0
