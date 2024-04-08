"""
Тесты для сервиса категории расходов
"""

import pytest
from inspect import isgenerator
from bookkeeper.models.category import Category
from bookkeeper.services.category_service import CategoryService
from bookkeeper.scripts.create_db import create_database
from bookkeeper.repository.sqlite_repository import SQLiteRepository


@pytest.fixture()
def repo():
    create_database("test.db")
    return SQLiteRepository(Category, "test.db")


@pytest.fixture
def category_service(repo):
    return CategoryService(repo)


def test_crud(category_service):
    category = Category(name="Развлечения")
    pk = category_service.add(category)
    assert category.pk != 0
    assert category.pk == pk
    res_category = category_service.get(pk)
    assert res_category == category
    category.name = "Музыка"
    category_service.update(category)
    assert category_service.get(pk).name == "Музыка"
    category_service.delete(pk)
    assert category_service.get(pk) is None


def test_get_all(category_service):
    category_name = "Все или ничего"
    category_service.add(Category(category_name))
    categories = category_service.get_all({"name": category_name})
    assert categories
    assert categories[0].name == category_name


def test_get_parent(category_service):
    c1 = Category(name="parent")
    pk = category_service.add(c1)
    c2 = Category(name="name", parent=pk)
    assert category_service.get_parent(c2) == c1


def test_get_all_parents(category_service):
    parent_pk = None
    for i in range(5):
        c = Category(str(i), parent=parent_pk)
        parent_pk = category_service.add(c)
    gen = category_service.get_all_parents(c)
    assert isgenerator(gen)
    assert [c.name for c in gen] == ["3", "2", "1", "0"]


def test_get_subcategories(category_service):
    parent_pk = None
    for i in range(5):
        c = Category(str(i), parent=parent_pk)
        parent_pk = category_service.add(c)
    c = category_service.get_all({"name": "0"})[0]
    gen = category_service.get_subcategories(c.pk)
    assert isgenerator(gen)
    # using set because order doesn't matter
    assert {c.name for c in gen} == {"1", "2", "3", "4"}


def test_get_subcategories_complicated(category_service):
    root = Category("0")
    root_pk = category_service.add(root)

    category_service.add(Category("1", root_pk))
    pk2 = category_service.add(Category("2", root_pk))

    category_service.add(Category("3", pk2))
    category_service.add(Category("4", pk2))

    gen = category_service.get_subcategories(root.pk)
    assert isgenerator(gen)
    # using set because order doesn't matter
    assert {c.name for c in gen} == {"1", "2", "3", "4"}


def test_create_from_tree(category_service):
    tree = [("parent", None), ("1", "parent"), ("2", "1")]
    cats = category_service.create_from_tree(tree)
    assert len(cats) == len(tree)
    parent = next(c for c in cats if c.name == "parent")
    assert parent.parent is None
    c1 = next(c for c in cats if c.name == "1")
    assert c1.parent == parent.pk
    c2 = next(c for c in cats if c.name == "2")
    assert c2.parent == c1.pk


def test_create_from_tree_error(category_service):
    tree = [("1", "parent"), ("parent", None)]
    with pytest.raises(KeyError):
        category_service.create_from_tree(tree)
