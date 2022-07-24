from typing import Optional


class Product(object):
    def __init__(self, codename: str, price: float, category: Optional[str]) -> None:
        self.codename = codename
        self.price = price
        self.category = category

    def __repr__(self):
        return f"Product(codename={self.codename}, price={self.price}, category={self.category})"


class Deposit(object):
    def __init__(self, name: str, money: float) -> None:
        self.name = name
        self.money = money

    def __repr__(self):
        return f"Deposit(name={self.name}, money={self.money})"
