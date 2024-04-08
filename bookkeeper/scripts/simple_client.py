"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from pprint import pprint

from bookkeeper.services.category_service import CategoryService
from bookkeeper.services.expense_service import ExpenseService
from bookkeeper.services.budget_service import BudgetService
from bookkeeper.scripts.create_db import create_database

create_database("bookkeeper.db")

exp_service = ExpenseService()
cat_service = CategoryService()
budget_service = BudgetService()

cats = """
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
""".splitlines()

# cat_service.create_from_tree(read_tree(cats))


while True:
    print("Сущности: category, expense, budget")
    print("1. Создать сущность")
    print("2. Получить по pk")
    print("3. Показать все")
    print("4. Удалить")
    print("5. Обновить")
    print("0. exit")
    option = int(input("Ваш выбор: "))
    if option == 1:
        print("category: name parent")
        print("expense: amount category")
        print("budget: limit_amount period_type")
        model, *values = input("Ваш выбор: ").split()
        if model == "category":
            cat_service.add(Category(*values))
            res = cat_service.get_all()
        elif model == "budget":
            budget_service.add(Budget(*values))
            res = budget_service.get_all()
        elif model == "expense":
            exp_service.add(Expense(*values))
            res = exp_service.get_all()
        pprint(res)
    elif option == 2:
        model, pk = input("Сущность и pk: ").split()
        if model == "category":
            res = cat_service.get(pk)
        elif model == "budget":
            res = budget_service.get(pk)
        elif model == "expense":
            res = exp_service.get(pk)
        pprint(res)
    elif option == 3:
        pprint(cat_service.get_all())
        print()
        pprint(exp_service.get_all())
        print()
        pprint(budget_service.get_all())
        print()
    elif option == 4:
        model, pk = input("Сущность и pk: ").split()
        if model == "category":
            cat_service.delete(pk)
        elif model == "budget":
            budget_service.delete(pk)
        elif model == "expense":
            exp_service.delete(pk)
    elif option == 5:
        period = input("Введите период: ")
        budget = budget_service.get_with_expenses(period_type=period)
        print(budget)
    else:
        break
