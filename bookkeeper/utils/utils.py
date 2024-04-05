"""
Вспомогательные функции
"""

from typing import Iterable, Iterator
from datetime import datetime, date, timedelta


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _lines_with_indent(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    for line in lines:
        if not line or line.isspace():
            continue
        yield _get_indent(line), line.strip()


def read_tree(lines: Iterable[str]) -> list[tuple[str, str | None]]:
    """
    Прочитать структуру дерева из текста на основе отступов. Вернуть список
    пар "потомок-родитель" в порядке топологической сортировки. Родитель
    элемента верхнего уровня - None.

    Пример. Следующий текст:
    parent
        child1
            child2
        child3

    даст такое дерево:
    [('parent', None), ('child1', 'parent'),
     ('child2', 'child1'), ('child3', 'parent')]

    Пустые строки игнорируются.

    Parameters
    ----------
    lines - Итерируемый объект, содержащий строки текста (файл или список строк)

    Returns
    -------
    Список пар "потомок-родитель"
    """
    parents: list[tuple[str | None, int]] = []
    last_indent = -1
    last_name = None
    result: list[tuple[str, str | None]] = []
    for line, (indent, name) in enumerate(_lines_with_indent(lines)):
        if indent > last_indent:
            parents.append((last_name, last_indent))
        elif indent < last_indent:
            while indent < last_indent:
                _, last_indent = parents.pop()
            if indent != last_indent:
                raise IndentationError(
                    f"unindent does not match any outer indentation "
                    f"level in line {line}:\n"
                )
        result.append((name, parents[-1][0]))
        last_name = name
        last_indent = indent
    return result


def get_week_boundaries(day: datetime) -> tuple[date, date]:
    """
    Получить дату начала и конца недели по указанному дню

    Parameters
    ----------
    day - день, для которого требуется найти даты

    Returns
    -------
    Кортеж, состоящий из даты начала и конца недели
    """
    weekday = day.weekday()
    start_of_week = day - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.date(), end_of_week.date()


def get_month_boundaries(day: datetime) -> tuple[date, date]:
    """
    Получить дату начала и конца месяца по указанному дню
    """
    start_of_month = day.replace(day=1).date()
    next_month = start_of_month.replace(month=start_of_month.month + 1)
    end_of_month = next_month - timedelta(days=1)
    return start_of_month, end_of_month
