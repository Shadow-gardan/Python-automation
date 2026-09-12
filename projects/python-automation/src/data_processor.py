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
