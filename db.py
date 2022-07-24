import os
from typing import Dict, List

import sqlite3


# Подключение к БД.
conn = sqlite3.connect(os.path.join("finance.db"))
cursor = conn.cursor()


def get_cursor():
    return cursor


def insert(table: str, column_values: Dict):
    """
    Метод реализующий INSERT для БД.
    :param table: название таблицы.
    :param column_values: столбцы для вставки и значения.
    """
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """
    Все записи из конкретных столбцов таблицы.
    :param table: название таблицы.
    :param columns: список нужных столбцов.
    :return: список словарей-строк, в котором ключ - название столбца.
    """
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def all_categories_costs() -> str:
    cursor.execute("SELECT Product.category_codename, SUM(t1.count) "
                   "FROM (SELECT product_codename, SUM(price) AS count "
                         "FROM Cost "
                         "GROUP BY product_codename) AS t1 INNER JOIN Product ON t1.product_codename=Product.codename "
                   "GROUP BY Product.category_codename")
    rows = cursor.fetchall()
    answer = ''
    for row in rows:
        answer += f"{row[0]} - {row[1]}\n"
    return answer


def all_deposits() -> str:
    cursor.execute("SELECT depositor_name, SUM(money) "
                   "FROM Deposit "
                   "GROUP BY depositor_name ")
    rows = cursor.fetchall()
    answer = ''
    for row in rows:
        answer += f"{row[0]} - {row[1]}\n"
    return answer


def delete_db():
    global conn
    global cursor

    os.remove("finance.db")
    conn = sqlite3.connect(os.path.join("finance.db"))
    cursor = conn.cursor()
    _init_db()


def delete_costs() -> None:
    cursor.execute(f"DROP TABLE Cost;")
    cursor.execute("CREATE TABLE Cost("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "price INTEGER,"
                   "created DATATIME,"
                   "product_codename TEXT,"
                   "FOREIGN KEY(product_codename) REFERENCES Product(codename)"
                   ");")
    conn.commit()


def delete_deposits() -> None:
    cursor.execute(f"DROP TABLE Deposit;")
    cursor.execute("CREATE TABLE Deposit("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "money INTEGER,"
                   "created DATATIME,"
                   "depositor_name TEXT,"
                   "FOREIGN KEY(depositor_name) REFERENCES Budget(codename)"
                   ");")
    conn.commit()


def _delete_table(table: str) -> None:
    cursor.execute(f"DROP TABLE {table}")
    conn.commit()


def _init_db():
    """
    Создание таблиц в БД (выполняется скрипт 'createdb.sql').
    """
    with open("./DBMS/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """
    Проверка на наличие таблиц в БД через таблицу 'sqlite_master'.
    В случае отстутсвия создаются.
    """
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='Budget'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
