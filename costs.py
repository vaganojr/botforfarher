from .tools import get_now_formatted
from .db import insert as db_insert
from .classes import Product


def add_cost(product: Product) -> Product:
    """
    Добавляет трату в БД.
    :param product: товар.
    :return: добавленный товар.
    """
    db_insert("Cost",
              {"price": product.price,
               "created": get_now_formatted(),
               "product_codename": product.codename})
    return product
