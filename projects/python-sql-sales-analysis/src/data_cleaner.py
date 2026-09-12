"""Cleaning and output writing for validated sales records."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from src.data_loader import REQUIRED_COLUMNS, load_sales_csv, validate_sales_records


@dataclass(frozen=True)
class CleaningStats:
    """Counts produced while validating and cleaning sales data."""

    input_rows: int
    duplicate_rows: int
    rejected_rows: int
    output_rows: int


def clean_sales_data(input_path: str | Path, output_path: str | Path) -> CleaningStats:
    """Validate sales CSV data and write a cleaned copy without changing input."""
    records = load_sales_csv(input_path)
    result = validate_sales_records(records)
    cleaned_records = []
    for record in result.valid_records:
        cleaned_records.append(
            {
                **record,
                "order_date": date.fromisoformat(record["order_date"]).isoformat(),
                "customer_name": " ".join(record["customer_name"].split()),
                "product_name": " ".join(record["product_name"].split()),
                "city": " ".join(record["city"].split()),
                "category": " ".join(record["category"].split()),
            }
        )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(cleaned_records)

    duplicate_rows = sum(
        1 for issue in result.issues if "duplicate sales record" in issue.message
    )
    return CleaningStats(
        input_rows=len(records),
        duplicate_rows=duplicate_rows,
        rejected_rows=len(result.issues) - duplicate_rows,
        output_rows=len(cleaned_records),
    )
