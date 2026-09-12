import sqlite3

from src.database import create_tables, customer_summary, import_customers


def test_database_import_and_summary():
	connection = sqlite3.connect(":memory:")
	connection.row_factory = sqlite3.Row
	create_tables(connection)

	count = import_customers(
		connection,
		[
			{"id": "1", "name": "Aman", "email": "aman@example.com", "age": "21", "city": "Delhi"},
			{"id": "2", "name": "Neha", "email": "N/A", "age": "24", "city": "Lucknow"},
		],
	)

	assert count == 2
	assert customer_summary(connection) == {
		"total_customers": 2,
		"average_age": 22.5,
		"customers_by_city": {"Delhi": 1, "Lucknow": 1},
		"customers_with_missing_information": 1,
	}