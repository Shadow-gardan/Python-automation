import sqlite3

import pytest

from src.database import create_tables, get_connection, import_sales_records


@pytest.fixture
def sample_records():
    return [
        {"order_id": "1001", "order_date": "2025-01-01", "customer_id": "1", "customer_name": "Ava", "city": "London", "product_id": "101", "product_name": "Keyboard", "category": "Electronics", "quantity": "2", "unit_price": "10.00"},
        {"order_id": "1001", "order_date": "2025-01-01", "customer_id": "1", "customer_name": "Ava", "city": "London", "product_id": "102", "product_name": "Hub", "category": "Electronics", "quantity": "1", "unit_price": "20.00"},
        {"order_id": "1002", "order_date": "2025-01-02", "customer_id": "2", "customer_name": "Ben", "city": "Leeds", "product_id": "101", "product_name": "Keyboard", "category": "Electronics", "quantity": "1", "unit_price": "10.00"},
        {"order_id": "1003", "order_date": "2025-02-01", "customer_id": "1", "customer_name": "Ava", "city": "London", "product_id": "103", "product_name": "Notebook", "category": "Office", "quantity": "3", "unit_price": "5.00"},
        {"order_id": "1004", "order_date": "2025-02-02", "customer_id": "3", "customer_name": "Cara", "city": "Leeds", "product_id": "102", "product_name": "Hub", "category": "Electronics", "quantity": "2", "unit_price": "20.00"},
    ]


@pytest.fixture
def sales_connection(sample_records):
    connection = get_connection(":memory:")
    create_tables(connection)
    import_sales_records(connection, sample_records)
    yield connection
    connection.close()
