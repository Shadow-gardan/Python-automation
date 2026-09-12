"""Command-line interface for the automation workflow."""

import argparse
import logging
import sqlite3

from src.config import (
    CLEANED_CUSTOMER_PATH,
    CUSTOMER_INPUT_PATH,
    DATABASE_PATH,
    INPUT_DIR,
    LOG_PATH,
    OUTPUT_DIR,
    REPORT_PATH,
)
from src.data_processor import clean_csv, load_records
from src.database import create_tables, customer_summary, get_connection, import_customers
from src.file_organizer import organize_files
from src.logger import configure_logging
from src.report_generator import write_text_report


def organize(logger: logging.Logger) -> dict:
    """Organize input files and return file statistics."""
    logger.info("Starting file organization")
    stats = organize_files(INPUT_DIR, OUTPUT_DIR)
    logger.info("Organized %s files", stats["files_copied"])
    return stats


def clean_customers(logger: logging.Logger) -> dict[str, int]:
    """Clean the sample customer CSV and return cleaning statistics."""
    logger.info("Cleaning customer CSV: %s", CUSTOMER_INPUT_PATH)
    stats = clean_csv(CUSTOMER_INPUT_PATH, CLEANED_CUSTOMER_PATH)
    logger.info("Cleaned %s rows", stats["final_row_count"])
    return stats


def import_database(logger: logging.Logger) -> dict:
    """Import cleaned customer records into SQLite."""
    if not CLEANED_CUSTOMER_PATH.exists():
        clean_customers(logger)
    records = load_records(CLEANED_CUSTOMER_PATH)
    with get_connection(DATABASE_PATH) as connection:
        create_tables(connection)
        count = import_customers(connection, records)
        stats = customer_summary(connection)
    logger.info("Imported %s customer records", count)
    return stats


def generate_report(
    logger: logging.Logger,
    file_stats: dict | None = None,
    csv_stats: dict | None = None,
) -> str:
    """Generate the final text report from current database data."""
    with get_connection(DATABASE_PATH) as connection:
        create_tables(connection)
        database_stats = customer_summary(connection)
    report_path = write_text_report(
        file_stats or {}, csv_stats or {}, database_stats, REPORT_PATH
    )
    logger.info("Report written to %s", report_path)
    return str(report_path)


def run_all(logger: logging.Logger) -> None:
    """Run file organization, CSV cleaning, database import, and reporting."""
    file_stats = organize(logger)
    csv_stats = clean_customers(logger)
    import_database(logger)
    generate_report(logger, file_stats, csv_stats)
    logger.info("Application completed")


def build_parser() -> argparse.ArgumentParser:
    """Build the supported command-line interface."""
    parser = argparse.ArgumentParser(description="Python file and data automation tool")
    parser.add_argument(
        "command",
        choices=["organize", "clean-csv", "import-db", "report", "run-all"],
        help="workflow step to run",
    )
    return parser


def main() -> None:
    """Parse a command and execute it with safe error handling."""
    args = build_parser().parse_args()
    logger = configure_logging(LOG_PATH)
    try:
        if args.command == "organize":
            organize(logger)
        elif args.command == "clean-csv":
            clean_customers(logger)
        elif args.command == "import-db":
            import_database(logger)
        elif args.command == "report":
            csv_stats = clean_customers(logger)
            generate_report(logger, csv_stats=csv_stats)
        else:
            run_all(logger)
    except (OSError, ValueError, sqlite3.Error) as error:
        logger.error("Application failed: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
