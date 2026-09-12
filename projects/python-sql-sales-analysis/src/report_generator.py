"""Readable sales report generation."""

from datetime import datetime
from pathlib import Path
from typing import Any


def _section(rows: list[dict[str, Any]], value_key: str = "revenue") -> str:
    """Format a list of analytics rows as simple report lines."""
    if not rows:
        return "  No data"
    lines = []
    for row in rows:
        label = (
            row.get("product_name")
            or row.get("customer_name")
            or row.get("city")
            or row.get("category")
            or row.get("month")
        )
        value = row.get(value_key)
        lines.append(f"  - {label}: {value}")
    return "\n".join(lines)


def write_sales_report(
    analysis: dict[str, Any],
    output_directory: str | Path,
) -> Path:
    """Write a timestamped report and never overwrite an existing report."""
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = directory / f"sales_report_{timestamp}.txt"
    counter = 1
    while path.exists():
        path = directory / f"sales_report_{timestamp}_{counter}.txt"
        counter += 1

    summary = analysis["summary"]
    content = f"""Sales Analysis Report
======================

Executive Summary
-----------------
Total Revenue: ${summary['total_revenue']:,.2f}
Total Orders: {summary['total_orders']}
Total Items Sold: {summary['total_items_sold']}
Average Order Value: ${summary['average_order_value']:,.2f}
Total Customers: {summary['total_customers']}
Total Products: {summary['total_products']}
Average Customer Spending: ${analysis['average_customer_spending']:,.2f}

Top Products by Revenue
----------------------
{_section(analysis['top_products_by_revenue'])}

Top Products by Quantity
-----------------------
{_section(analysis['top_products_by_quantity'], 'quantity_sold')}

Top Customers by Revenue
-----------------------
{_section(analysis['top_customers_by_revenue'])}

Revenue by City
---------------
{_section(analysis['revenue_by_city'])}

Revenue by Category
------------------
{_section(analysis['revenue_by_category'])}

Monthly Revenue
---------------
{_section(analysis['monthly_revenue'])}
"""
    path.write_text(content, encoding="utf-8")
    return path
