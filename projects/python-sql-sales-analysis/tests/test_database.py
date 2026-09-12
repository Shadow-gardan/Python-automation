def test_database_has_normalized_tables(sales_connection):
    tables = {
        row[0]
        for row in sales_connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }

    assert {"customers", "products", "orders", "order_items"} <= tables


def test_database_import_preserves_relationships(sales_connection):
    assert sales_connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 3
    assert sales_connection.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 3
    assert sales_connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 4
    assert sales_connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 5
