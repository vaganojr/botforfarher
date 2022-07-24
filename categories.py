from typing import List

from .classes import Product
from .db import insert as db_insert
from .db import fetchall as db_fetchall
from .products import add_product


def add_category(product: Product) -> Product:
    """
    Добавляет категорию в БД.
    :param product: товар, у котого указана категория.
    :return: добавленный товар.
    """
    product.category = product.category.lower().capitalize()
    db_insert("Category", {"codename": product.category})
    return add_product(product)


def all_categories() -> List[str]:
    """
    Возвращает все категории.
    :return: список с названиями категорий.
    """
    result_rows = db_fetchall("Category", ["codename"])
    result = []
    for row in result_rows:
        result.append(row['codename'])
    return result
