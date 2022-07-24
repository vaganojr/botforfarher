CREATE TABLE Budget(
    codename TEXT PRIMARY KEY
);

CREATE TABLE Deposit(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    money DECIMAL,
    created DATATIME,
    depositor_name TEXT,
    FOREIGN KEY(depositor_name) REFERENCES Budget(codename)
);

CREATE TABLE Category(
    codename TEXT PRIMARY KEY
);

CREATE TABLE Product(
    codename TEXT PRIMARY KEY,
    category_codename TEXT,
    FOREIGN KEY(category_codename) REFERENCES Category(codename)
);

CREATE TABLE Cost(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price DECIMAL,
    created DATATIME,
    product_codename TEXT,
    FOREIGN KEY(product_codename) REFERENCES Product(codename)
);