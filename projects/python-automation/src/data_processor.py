import csv
import json
from pathlib import Path
from typing import Any


def _clean_row(row: dict[str, Any]) -> dict[str, Any]:
	"""Normalize column names and discard surrounding whitespace in values."""
	return {
		str(key).strip().lower().replace(" ", "_"): value.strip()
		if isinstance(value, str)
		else value
		for key, value in row.items()
		if key is not None
	}


def load_csv(file_path: str | Path) -> list[dict[str, Any]]:
	"""Load non-empty rows from a CSV file with normalized fields."""
	path = Path(file_path)
	with path.open("r", encoding="utf-8", newline="") as file:
		return [
			_clean_row(row)
			for row in csv.DictReader(file)
			if any(
				key is not None
				and value is not None
				and str(value).strip()
				for key, value in row.items()
			)
		]


def clean_csv(input_path: str | Path, output_path: str | Path) -> dict[str, int]:
	"""Deduplicate and fill missing CSV values without changing the input file."""
	input_file = Path(input_path)
	output_file = Path(output_path)
	if not input_file.exists():
		raise FileNotFoundError(f"CSV file does not exist: {input_file}")

	with input_file.open("r", encoding="utf-8", newline="") as source:
		reader = csv.DictReader(source)
		if not reader.fieldnames:
			raise ValueError("CSV file must include a header")
		fieldnames = [field.strip().lower().replace(" ", "_") for field in reader.fieldnames]
		unique_rows: list[dict[str, str]] = []
		seen: set[tuple[str, ...]] = set()
		missing_values_replaced = 0
		original_row_count = 0
		duplicate_count = 0

		for raw_row in reader:
			if not any(value and value.strip() for value in raw_row.values() if value is not None):
				continue
			original_row_count += 1
			row: dict[str, str] = {}
			for original_field, field in zip(reader.fieldnames, fieldnames):
				value = (raw_row.get(original_field) or "").strip()
				if not value:
					value = "N/A"
					missing_values_replaced += 1
				row[field] = value
			dedupe_fields = [field for field in fieldnames if field != "id"] or fieldnames
			key = tuple(row[field] for field in dedupe_fields)
			if key in seen:
				duplicate_count += 1
				continue
			seen.add(key)
			unique_rows.append(row)

	output_file.parent.mkdir(parents=True, exist_ok=True)
	with output_file.open("w", encoding="utf-8", newline="") as destination:
		writer = csv.DictWriter(destination, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(unique_rows)

	return {
		"original_row_count": original_row_count,
		"duplicate_count": duplicate_count,
		"final_row_count": len(unique_rows),
		"missing_values_replaced": missing_values_replaced,
	}


def load_json(file_path: str | Path) -> list[dict[str, Any]]:
	"""Load a JSON object list and validate its top-level shape."""
	path = Path(file_path)
	with path.open("r", encoding="utf-8") as file:
		data = json.load(file)

	if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
		raise ValueError("JSON input must contain a list of objects")

	return [_clean_row(row) for row in data]


def load_records(file_path: str | Path) -> list[dict[str, Any]]:
	"""Load CSV or JSON records based on the file extension."""
	path = Path(file_path)
	if path.suffix.lower() == ".csv":
		return load_csv(path)
	if path.suffix.lower() == ".json":
		return load_json(path)
	raise ValueError(f"Unsupported data format: {path.suffix or '<none>'}")
