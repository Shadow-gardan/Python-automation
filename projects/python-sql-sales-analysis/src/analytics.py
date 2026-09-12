"""Business analytics implemented as readable SQL queries."""

import sqlite3
from typing import Any


def _rows(
    connection: sqlite3.Connection,
    query: str,
    parameters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a read-only query and return dictionaries for report generation."""
    return [
        dict(row)
        for row in connection.execute(query, parameters or {}).fetchall()
    ]


def sales_summary(connection: sqlite3.Connection) -> dict[str, Any]:
    """Return executive sales totals using SQL aggregation."""
    row = connection.execute(
        """
        SELECT
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(SUM(oi.quantity), 0) AS total_items_sold,
            COUNT(DISTINCT c.customer_id) AS total_customers,
            COUNT(DISTINCT p.product_id) AS total_products
        FROM order_items AS oi
        JOIN orders AS o ON o.order_id = oi.order_id
        JOIN customers AS c ON c.customer_id = o.customer_id
        JOIN products AS p ON p.product_id = oi.product_id
        """
    ).fetchone()
    average_order_value = (
        row["total_revenue"] / row["total_orders"] if row["total_orders"] else 0
    )
    return {
        "total_revenue": round(row["total_revenue"], 2),
        "total_orders": row["total_orders"],
        "total_items_sold": row["total_items_sold"],
        "average_order_value": round(average_order_value, 2),
        "total_customers": row["total_customers"],
        "total_products": row["total_products"],
    }


def top_products_by_revenue(connection: sqlite3.Connection, limit: int = 5) -> list[dict[str, Any]]:
    """Return products ranked by revenue."""
    return _rows(
        connection,
        """
        SELECT p.product_name, p.category,
               ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
               SUM(oi.quantity) AS quantity_sold
        FROM order_items AS oi
        JOIN products AS p ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY revenue DESC, p.product_name ASC
        LIMIT :limit
        """,
        {"limit": max(0, int(limit))},
    )


def top_products_by_quantity(connection: sqlite3.Connection, limit: int = 5) -> list[dict[str, Any]]:
    """Return products ranked by quantity sold."""
    return _rows(
        connection,
        """
        SELECT p.product_name, p.category,
               SUM(oi.quantity) AS quantity_sold,
               ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items AS oi
        JOIN products AS p ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY quantity_sold DESC, p.product_name ASC
        LIMIT :limit
        """,
        {"limit": max(0, int(limit))},
    )


def top_customers_by_revenue(connection: sqlite3.Connection, limit: int = 5) -> list[dict[str, Any]]:
    """Return customers ranked by revenue."""
    return _rows(
        connection,
        """
        SELECT c.customer_name, c.city,
               ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items AS oi
        JOIN orders AS o ON o.order_id = oi.order_id
        JOIN customers AS c ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, c.city
        ORDER BY revenue DESC, c.customer_name ASC
        LIMIT :limit
        """,
        {"limit": max(0, int(limit))},
    )


def revenue_by_city(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return revenue grouped by customer city."""
    return _rows(
        connection,
        """
        SELECT c.city, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items AS oi
        JOIN orders AS o ON o.order_id = oi.order_id
        JOIN customers AS c ON c.customer_id = o.customer_id
        GROUP BY c.city
        ORDER BY revenue DESC, c.city ASC
        """,
    )


def revenue_by_category(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return revenue grouped by product category."""
    return _rows(
        connection,
        """
        SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items AS oi
        JOIN products AS p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY revenue DESC, p.category ASC
        """,
    )


def monthly_revenue(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return revenue grouped by calendar month."""
    return _rows(
        connection,
        """
        SELECT strftime('%Y-%m', o.order_date) AS month,
               ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items AS oi
        JOIN orders AS o ON o.order_id = oi.order_id
        GROUP BY month
        ORDER BY month
        """,
    )


def average_customer_spending(connection: sqlite3.Connection) -> float:
    """Return average customer spending using a SQL subquery."""
    row = connection.execute(
        """
        SELECT COALESCE(AVG(customer_revenue), 0) AS average_spending
        FROM (
            SELECT o.customer_id, SUM(oi.quantity * oi.unit_price) AS customer_revenue
            FROM orders AS o
            JOIN order_items AS oi ON oi.order_id = o.order_id
            GROUP BY o.customer_id
        )
        """
    ).fetchone()
    return round(row["average_spending"], 2)


def run_all_analytics(connection: sqlite3.Connection) -> dict[str, Any]:
    """Run every report query and return structured analysis results."""
    return {
        "summary": sales_summary(connection),
        "top_products_by_revenue": top_products_by_revenue(connection),
        "top_products_by_quantity": top_products_by_quantity(connection),
        "top_customers_by_revenue": top_customers_by_revenue(connection),
        "revenue_by_city": revenue_by_city(connection),
        "revenue_by_category": revenue_by_category(connection),
        "monthly_revenue": monthly_revenue(connection),
        "average_customer_spending": average_customer_spending(connection),
    }
