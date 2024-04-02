"""
Модель категории расходов
"""

from dataclasses import dataclass


@dataclass
class Category:
    """
    Категория расходов, хранит название в атрибуте name и ссылку (id) на
    родителя (категория, подкатегорией которой является данная) в атрибуте parent.
    У категорий верхнего уровня parent = None
    name - название категории
    parent - pk ключ родителя
    pk - id записи в базе данных
    """

    name: str
    parent: int | None = None
    pk: int = 0
