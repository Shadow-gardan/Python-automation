"""Command-line interface for the sales analysis workflow."""

import argparse
import logging
import sqlite3

from src.analytics import run_all_analytics
from src.config import (
    CLEANED_SALES_PATH,
    DATABASE_PATH,
    LOG_PATH,
    OUTPUT_DIR,
    SALES_INPUT_PATH,
)
from src.data_cleaner import CleaningStats, clean_sales_data
from src.data_loader import load_sales_csv, validate_sales_records
from src.database import create_tables, get_connection, import_sales_records
from src.logger import configure_logging
from src.report_generator import write_sales_report


def validate_input(logger: logging.Logger) -> int:
    """Validate the input CSV and print any row-level issues."""
    records = load_sales_csv(SALES_INPUT_PATH)
    result = validate_sales_records(records)
    if result.issues:
        for issue in result.issues:
            logger.warning("Row %s: %s", issue.row_number, issue.message)
    logger.info("Validated %s rows with %s issue(s)", len(records), len(result.issues))
    print(f"Validated {len(records)} rows; issues: {len(result.issues)}")
    return len(result.issues)


def clean_input(logger: logging.Logger) -> CleaningStats:
    """Create a cleaned CSV copy and print cleaning statistics."""
    stats = clean_sales_data(SALES_INPUT_PATH, CLEANED_SALES_PATH)
    logger.info(
        "Cleaned %s rows: %s duplicates, %s rejected",
        stats.input_rows,
        stats.duplicate_rows,
        stats.rejected_rows,
    )
    print(
        f"Cleaned {stats.input_rows} rows; output: {stats.output_rows}, "
        f"duplicates: {stats.duplicate_rows}, rejected: {stats.rejected_rows}"
    )
    return stats


def import_database(logger: logging.Logger) -> int:
    """Create the SQLite schema and import cleaned records."""
    if not CLEANED_SALES_PATH.exists():
        clean_input(logger)
    records = load_sales_csv(CLEANED_SALES_PATH)
    with get_connection(DATABASE_PATH) as connection:
        create_tables(connection)
        imported = import_sales_records(connection, records)
    logger.info("Imported %s sales rows into SQLite", imported)
    print(f"Imported {imported} rows into {DATABASE_PATH}")
    return imported


def analyze_database(logger: logging.Logger) -> dict:
    """Run all SQL analytics and return their structured results."""
    if not DATABASE_PATH.exists():
        import_database(logger)
    with get_connection(DATABASE_PATH) as connection:
        analysis = run_all_analytics(connection)
    logger.info("Completed SQL analytics")
    summary = analysis["summary"]
    print(
        f"Revenue: ${summary['total_revenue']:,.2f}; "
        f"orders: {summary['total_orders']}; customers: {summary['total_customers']}"
    )
    return analysis


def generate_report(logger: logging.Logger) -> str:
    """Run analytics and write the timestamped sales report."""
    analysis = analyze_database(logger)
    report_path = write_sales_report(analysis, OUTPUT_DIR)
    logger.info("Generated report: %s", report_path)
    print(f"Report written to {report_path}")
    return str(report_path)


def run_all(logger: logging.Logger) -> None:
    """Run validation, cleaning, database import, analysis, and reporting."""
    logger.info("Application started")
    validate_input(logger)
    clean_input(logger)
    import_database(logger)
    generate_report(logger)
    logger.info("Application completed")
    print("Complete sales analysis workflow finished.")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Python and SQL sales analysis system")
    parser.add_argument(
        "command",
        choices=["validate", "clean", "database", "analyze", "report", "run-all"],
        help="workflow stage to execute",
    )
    return parser


def main() -> None:
    """Run one CLI command with logged, user-readable error handling."""
    args = build_parser().parse_args()
    logger = configure_logging(LOG_PATH)
    try:
        if args.command == "validate":
            validate_input(logger)
        elif args.command == "clean":
            clean_input(logger)
        elif args.command == "database":
            import_database(logger)
        elif args.command == "analyze":
            analyze_database(logger)
        elif args.command == "report":
            generate_report(logger)
        else:
            run_all(logger)
    except (OSError, ValueError, sqlite3.Error) as error:
        logger.error("Application failed: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
