# Python + SQL Sales & Customer Data Analysis System

A beginner-readable portfolio project that turns fictional sales CSV data into a normalized SQLite database, reusable SQL business analysis, and a timestamped management report.

## Business Problem

Small businesses often receive sales exports that are difficult to summarize repeatedly. This project demonstrates a safe, repeatable workflow for validating incoming data, removing exact duplicate rows, loading relational tables, answering business questions with SQL, and producing a readable report without changing the original CSV.

## Features

- Validates required sales columns, dates, quantities, prices, customer fields, and product fields.
- Removes exact duplicate sales rows and rejects invalid records.
- Normalizes text fields and dates in a separate cleaned CSV.
- Imports data into normalized `customers`, `products`, `orders`, and `order_items` tables.
- Uses SQLite foreign keys, transactions, and parameterized SQL.
- Calculates revenue, orders, items sold, average order value, top products, top customers, city revenue, category revenue, monthly revenue, and average customer spending.
- Generates timestamped text reports without overwriting existing reports.
- Logs application stages to `logs/app.log`.
- Includes 13 pytest tests using temporary files and in-memory databases.

## Technology Stack

- Python 3
- SQLite and SQL
- Python standard library
- pytest
- Linux/Ubuntu
- Git/GitHub

## Architecture

```text
 data/input/sales.csv
          |
          v
  Load and validate CSV
          |
          v
  Clean duplicate/invalid rows
          |
          v
  SQLite relational database
          |
          v
  SQL business analytics
          |
          v
  Timestamped text report
```

## Database Schema

- `customers`: one row per customer, with name and city.
- `products`: one row per product, with category and reference price.
- `orders`: one row per order, linked to a customer.
- `order_items`: one row per product line in an order, linked to orders and products.

This design allows one order to contain multiple products without duplicating customer or product details.

## Project Structure

```text
python-sql-sales-analysis/
├── data/
│   ├── input/sales.csv              # Fictional source dataset
│   └── output/                      # Cleaned CSV and generated reports
├── database/                        # SQLite database, ignored by Git
├── logs/                            # Runtime logs, ignored by Git
├── src/
│   ├── config.py                    # Project-relative paths
│   ├── data_loader.py               # CSV loading and validation
│   ├── data_cleaner.py              # Cleaning and statistics
│   ├── database.py                  # Schema and import transactions
│   ├── analytics.py                 # SQL business queries
│   ├── report_generator.py          # Text report formatting
│   ├── logger.py                    # Logging setup
│   └── main.py                      # CLI orchestration
└── tests/                           # Automated tests
```

## Installation on Ubuntu/Linux

```bash
git clone <repository-url>
cd python-sql-sales-analysis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The application has no runtime dependency outside Python's standard library. `pytest` is installed for development and testing.

## CLI Usage

Run commands from the project root:

```bash
python -m src.main --help
python -m src.main validate
python -m src.main clean
python -m src.main database
python -m src.main analyze
python -m src.main report
python -m src.main run-all
```

`run-all` executes validation, cleaning, database creation/import, SQL analytics, and report generation in that order.

## Example Workflow

The sample dataset contains 35 rows, including one exact duplicate. A complete run produces:

```text
Input rows: 35
Duplicate rows removed: 1
Clean output rows: 34
Database tables: customers, products, orders, order_items
Report: data/output/sales_report_YYYYMMDD_HHMMSS.txt
Log: logs/app.log
```

The report contains executive totals plus top products, top customers, revenue by city, revenue by category, monthly revenue, and average customer spending.

## Testing

```bash
python -m pytest -v
```

Tests use temporary directories and in-memory SQLite databases. They do not modify the project's real database or sample input.

## Safety

- The original CSV is never modified.
- Invalid rows are rejected rather than silently changed.
- Reports use timestamped filenames and do not overwrite existing reports.
- SQL values are passed as parameters.
- SQLite foreign keys are enabled.
- Databases, logs, virtual environments, caches, and environment files are ignored by Git.
- The project uses `pathlib.Path` and does not depend on a specific username or absolute machine path.

## Future Improvements

- Add Excel import support.
- Add a PostgreSQL export option.
- Add scheduled execution.
- Add a small web dashboard.
- Add a REST API.
- Add Docker packaging.

## Freelance Value

This project demonstrates a realistic client workflow: validating a sales export, cleaning unreliable data, designing relational tables, writing SQL analysis, automating repeatable reports, and supporting the process with tests, logging, and clear command-line operations.
