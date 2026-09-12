"""CSV loading and validation for sales records."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = (
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "city",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
)


@dataclass(frozen=True)
class ValidationIssue:
    """A validation problem associated with one input row."""

    row_number: int
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Validated rows and the issues found in the input."""

    valid_records: list[dict[str, str]]
    issues: list[ValidationIssue]


def load_sales_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Load non-empty CSV rows and normalize their field names and values."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Sales CSV does not exist: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("Sales CSV must contain a header row")
        columns = [column.strip().lower() for column in reader.fieldnames]
        missing_columns = set(REQUIRED_COLUMNS) - set(columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Sales CSV is missing required columns: {missing}")

        records = []
        for raw_row in reader:
            if not any(str(value or "").strip() for value in raw_row.values()):
                continue
            records.append(
                {
                    column: str(raw_row.get(original, "") or "").strip()
                    for original, column in zip(reader.fieldnames, columns)
                    if column in REQUIRED_COLUMNS
                }
            )
        return records


def validate_sales_records(records: list[dict[str, str]]) -> ValidationResult:
    """Validate IDs, dates, customer/product fields, quantities, and prices."""
    valid_records: list[dict[str, str]] = []
    issues: list[ValidationIssue] = []
    seen_rows: set[tuple[str, ...]] = set()

    for row_number, record in enumerate(records, start=2):
        problems: list[str] = []
        if not record.get("order_id"):
            problems.append("missing order_id")
        if not record.get("customer_id") or not record.get("customer_name"):
            problems.append("missing customer information")
        if not record.get("product_id") or not record.get("product_name"):
            problems.append("missing product information")
        try:
            date.fromisoformat(record.get("order_date", ""))
        except ValueError:
            problems.append("invalid order_date; expected YYYY-MM-DD")
        try:
            if int(record.get("quantity", "0")) <= 0:
                problems.append("quantity must be positive")
        except ValueError:
            problems.append("quantity must be an integer")
        try:
            if float(record.get("unit_price", "0")) <= 0:
                problems.append("unit_price must be positive")
        except ValueError:
            problems.append("unit_price must be numeric")

        row_key = tuple(record.get(column, "") for column in REQUIRED_COLUMNS)
        if row_key in seen_rows:
            problems.append("duplicate sales record")
        else:
            seen_rows.add(row_key)

        if problems:
            issues.append(ValidationIssue(row_number, "; ".join(problems)))
        else:
            valid_records.append(record)

    return ValidationResult(valid_records, issues)
