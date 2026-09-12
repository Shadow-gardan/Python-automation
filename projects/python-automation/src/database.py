"""SQLite persistence and reporting queries for customer records."""

import sqlite3
from pathlib import Path
from typing import Any, Iterable


def get_connection(database_path: str | Path) -> sqlite3.Connection:
	"""Create a SQLite connection and enable named-row access."""
	path = Path(database_path)
	path.parent.mkdir(parents=True, exist_ok=True)
	connection = sqlite3.connect(path)
	connection.row_factory = sqlite3.Row
	return connection


def create_tables(connection: sqlite3.Connection) -> None:
	"""Create application tables if they do not exist."""
	connection.execute(
		"""
		CREATE TABLE IF NOT EXISTS customers (
			id INTEGER PRIMARY KEY,
			name TEXT NOT NULL,
			email TEXT NOT NULL,
			age INTEGER,
			city TEXT NOT NULL
		)
		"""
	)
	connection.commit()


def import_customers(
	connection: sqlite3.Connection,
	records: Iterable[dict[str, Any]],
) -> int:
	"""Replace customer rows using parameterized SQL and return row count."""
	rows = [
		(
			int(record["id"]),
			str(record.get("name", "N/A")),
			str(record.get("email", "N/A")),
			int(record["age"]) if str(record.get("age", "")).isdigit() else None,
			str(record.get("city", "N/A")),
		)
		for record in records
	]
	connection.execute("DELETE FROM customers")
	connection.executemany(
		"""
		INSERT INTO customers (id, name, email, age, city)
		VALUES (?, ?, ?, ?, ?)
		""",
		rows,
	)
	connection.commit()
	return len(rows)


def customer_summary(connection: sqlite3.Connection) -> dict[str, Any]:
	"""Run readable SQL queries and return customer summary statistics."""
	total = connection.execute("SELECT COUNT(*) AS total FROM customers").fetchone()["total"]
	average_age = connection.execute(
		"SELECT AVG(age) AS average_age FROM customers WHERE age IS NOT NULL"
	).fetchone()["average_age"]
	city_rows = connection.execute(
		"""
		SELECT city, COUNT(*) AS customer_count
		FROM customers
		GROUP BY city
		ORDER BY customer_count DESC, city ASC
		"""
	).fetchall()
	missing = connection.execute(
		"""
		SELECT COUNT(*) AS missing_count
		FROM customers
		WHERE email = 'N/A' OR city = 'N/A' OR age IS NULL
		"""
	).fetchone()["missing_count"]
	return {
		"total_customers": total,
		"average_age": round(average_age, 2) if average_age is not None else None,
		"customers_by_city": {
			row["city"]: row["customer_count"] for row in city_rows
		},
		"customers_with_missing_information": missing,
	}