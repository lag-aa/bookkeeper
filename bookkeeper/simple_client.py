"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.expense import Expense
from bookkeeper.services.category_service import CategoryService
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import read_tree

exp_repo = MemoryRepository[Expense]()
cat_service = CategoryService()

cats = """
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
""".splitlines()

cat_service.create_from_tree(read_tree(cats))

while True:
    try:
        cmd = input("$> ")
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == "категории":
        print(*cat_service.get_all(), sep="\n")
    elif cmd == "расходы":
        print(*exp_repo.get_all(), sep="\n")
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_service.get_all({"name": name})[0]
        except IndexError:
            print(f"категория {name} не найдена")
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
