import re
from typing import List

from .classes import Deposit
from .tools import get_now_formatted
from .db import get_cursor
from .db import fetchall as db_fetchall
from .db import insert as db_insert


def add_deposit(raw_message: str) -> Deposit:
    """
    Добавляет доход в БД по сообщению.
    :param raw_message: сообщение.
    """
    deposit = _parse_message(raw_message)
    # Проверяем наличие вкладчика в БД.
    cursor = get_cursor()
    cursor.execute(f"SELECT codename "
                   f"FROM Budget "
                   f"WHERE codename = '{deposit.name}'")
    row = cursor.fetchone()
    # Если вкладчика нет, то добавляем его в БД по имени.
    if not row:
        _add_depositor(deposit)
    # Добавляем доход в БД.
    _add_deposit(deposit)
    return deposit


def all_depositors() -> List[str]:
    """
    Возвращает все категории.
    :return: список с названиями категорий.
    """
    result_rows = db_fetchall("Budget", ["codename"])
    result = []
    for row in result_rows:
        result.append(row['codename'])
    return result


def _add_depositor(deposit: Deposit) -> None:
    """
    Добавляет вкладчика в БД по доходу.
    :param deposit: доход.
    """
    db_insert("Budget", {"codename": deposit.name})


def _add_deposit(deposit: Deposit) -> None:
    """
    Добавляет доход в БД.
    :param deposit: доход.
    """
    db_insert("Deposit",
              {"money": deposit.money,
               "created": get_now_formatted(),
               "depositor_name": deposit.name})


def _parse_message(raw_message: str) -> Deposit:
    """
    Обрабатывает сообщение в экземпляр Deposit.
    Имя и вклад должны быть разделены тире.
    :param raw_message: сообщение.
    :return: вклад.
    """
    try:
        # Разбиваем сообщение на две части, и убираем пробел, если есть в конце имени.
        name, money = raw_message.split('-')
        if name[-1] == " ":
            name = name[:-1]
        # Приводим к нормальному виду (первая буква - заглавная, остальные - строчные).
        name = name.lower().capitalize()
        # Находим число-вклад.
        money = re.findall(r"[-+]?\d*\.\d+|\d+", money)[0]
    except Exception as e:
        raise e
    return Deposit(name=name, money=float(money))
