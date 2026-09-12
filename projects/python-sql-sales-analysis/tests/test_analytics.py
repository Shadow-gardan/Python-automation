from src.analytics import (
    average_customer_spending,
    monthly_revenue,
    revenue_by_city,
    run_all_analytics,
    top_products_by_revenue,
)


def test_sales_summary_calculates_business_totals(sales_connection):
    summary = run_all_analytics(sales_connection)["summary"]

    assert summary == {
        "total_revenue": 105.0,
        "total_orders": 4,
        "total_items_sold": 9,
        "average_order_value": 26.25,
        "total_customers": 3,
        "total_products": 3,
    }


def test_top_product_is_ranked_by_revenue(sales_connection):
    top_product = top_products_by_revenue(sales_connection, limit=1)[0]

    assert top_product["product_name"] == "Hub"
    assert top_product["revenue"] == 60.0


def test_city_and_month_queries_return_grouped_rows(sales_connection):
    assert revenue_by_city(sales_connection)[0] == {"city": "London", "revenue": 55.0}
    assert monthly_revenue(sales_connection) == [
        {"month": "2025-01", "revenue": 50.0},
        {"month": "2025-02", "revenue": 55.0},
    ]


def test_average_customer_spending_uses_customers(sales_connection):
    assert average_customer_spending(sales_connection) == 35.0
