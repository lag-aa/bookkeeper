"""
Utility functions
"""

from typing import Iterable, Iterator, Union


def _get_indent(line: str) -> int:
    """
    Get the indentation level of a line.

    Parameters:
        line (str): A line of text.

    Returns:
        int: Indentation level.
    """
    return len(line) - len(line.lstrip())


def _lines_with_indent(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    """
    Generate lines with their corresponding indentation level.

    Parameters:
        lines (Iterable[str]): Iterable object containing lines of text.

    Yields:
        tuple[int, str]: Indentation level and line content.
    """
    for line in lines:
        if not line or line.isspace():
            continue
        yield _get_indent(line), line.strip()


def read_tree(lines: Iterable[str]) -> list[tuple[str, Union[str, None]]]:
    """
    Read the tree structure from text based on indentation. Return a list of
    "child-parent" pairs in topological order. The parent of a top-level item is None.

    Example:
    The following text:
    parent
        child1
            child2
        child3

    will yield this tree:
    [('parent', None), ('child1', 'parent'),
     ('child2', 'child1'), ('child3', 'parent')]

    Empty lines are ignored.

    Parameters:
        lines (Iterable[str]): Iterable object containing lines of text.

    Returns:
        list[tuple[str, Union[str, None]]]: List of "child-parent" pairs.
    """
    parents: list[tuple[Union[str, None], int]] = []
    last_indent = -1
    last_name = None
    result: list[tuple[str, Union[str, None]]] = []
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
