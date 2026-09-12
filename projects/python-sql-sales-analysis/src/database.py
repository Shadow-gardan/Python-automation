"""SQLite schema creation and sales-data import."""

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL CHECK (unit_price > 0)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price > 0),
    UNIQUE(order_id, product_id)
);
"""


def get_connection(database_path: str | Path) -> sqlite3.Connection:
    """Open SQLite with foreign-key enforcement and named result rows."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    """Create the normalized sales tables if they do not exist."""
    connection.executescript(SCHEMA)
    connection.commit()


def import_sales_records(
    connection: sqlite3.Connection,
    records: Iterable[dict[str, str]],
) -> int:
    """Replace database contents with cleaned records in one transaction."""
    rows = list(records)
    try:
        with connection:
            connection.execute("DELETE FROM order_items")
            connection.execute("DELETE FROM orders")
            connection.execute("DELETE FROM products")
            connection.execute("DELETE FROM customers")
            for record in rows:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO customers
                        (customer_id, customer_name, city)
                    VALUES (?, ?, ?)
                    """,
                    (
                        int(record["customer_id"]),
                        record["customer_name"],
                        record["city"],
                    ),
                )
                connection.execute(
                    """
                    INSERT OR IGNORE INTO products
                        (product_id, product_name, category, unit_price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        int(record["product_id"]),
                        record["product_name"],
                        record["category"],
                        float(record["unit_price"]),
                    ),
                )
                connection.execute(
                    """
                    INSERT OR IGNORE INTO orders (order_id, order_date, customer_id)
                    VALUES (?, ?, ?)
                    """,
                    (
                        int(record["order_id"]),
                        record["order_date"],
                        int(record["customer_id"]),
                    ),
                )
                connection.execute(
                    """
                    INSERT OR IGNORE INTO order_items
                        (order_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        int(record["order_id"]),
                        int(record["product_id"]),
                        int(record["quantity"]),
                        float(record["unit_price"]),
                    ),
                )
    except sqlite3.Error:
        connection.rollback()
        raise
    return len(rows)
