import pytest
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.scripts.create_db import create_database
from dataclasses import dataclass


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        name: str
        age: int
        pk: int = 0

    return Custom


@pytest.fixture()
def repo(custom_class):
    create_database("test.db", True)
    return SQLiteRepository(custom_class, "test.db")


def test_crud(repo, custom_class):
    obj = custom_class("alex", 23)
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class("nick", 20)
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class("alex", 23)
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class("alex", 23)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class("alex", 23) for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []

    for i in range(5):
        o = custom_class(str(i), 5)
        repo.add(o)
        objects.append(o)

    assert repo.get_all({"name": "0"}) == [objects[0]]
    assert repo.get_all({"age": 5}) == objects
