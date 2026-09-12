import json
from datetime import datetime
from pathlib import Path
from typing import Any


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
	"""Return a small, JSON-serializable summary of processed records."""
	fields = sorted({field for record in records for field in record})
	return {
		"record_count": len(records),
		"fields": fields,
		"non_empty_values": {
			field: sum(
				1 for record in records if record.get(field) not in (None, "")
			)
			for field in fields
		},
	}


def write_report(
	records: list[dict[str, Any]], output_path: str | Path
) -> Path:
	"""Write a formatted JSON summary and return its path."""
	path = Path(output_path)
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(
		json.dumps(summarize_records(records), indent=2) + "\n",
		encoding="utf-8",
	)
	return path


def write_text_report(
	file_stats: dict[str, Any],
	csv_stats: dict[str, Any],
	database_stats: dict[str, Any],
	output_path: str | Path,
) -> Path:
	"""Write a readable report, timestamping the path when it already exists."""
	path = Path(output_path)
	if path.exists():
		base_path = path.with_name(
			f"{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
		)
		path = base_path
		counter = 1
		while path.exists():
			path = base_path.with_name(
				f"{base_path.stem}_{counter}{base_path.suffix}"
			)
			counter += 1
	path.parent.mkdir(parents=True, exist_ok=True)
	category_lines = "\n".join(
		f"  - {category}: {count}"
		for category, count in sorted(file_stats.get("files_by_category", {}).items())
	)
	city_lines = "\n".join(
		f"  - {city}: {count}"
		for city, count in database_stats.get("customers_by_city", {}).items()
	)
	content = f"""Python File & Data Automation Report
====================================

File Processing
---------------
Total files processed: {file_stats.get('total_files', 0)}
Files organized: {file_stats.get('files_copied', 0)}
Files skipped: {file_stats.get('files_skipped', 0)}
Files by category:
{category_lines or '  - None'}

CSV Processing
--------------
Original rows: {csv_stats.get('original_row_count', 0)}
Duplicates removed: {csv_stats.get('duplicate_count', 0)}
Missing values replaced: {csv_stats.get('missing_values_replaced', 0)}
Final rows: {csv_stats.get('final_row_count', 0)}

Database
--------
Customers: {database_stats.get('total_customers', 0)}
Average age: {database_stats.get('average_age', 'N/A')}
Customers by city:
{city_lines or '  - None'}
Customers with missing information: {database_stats.get('customers_with_missing_information', 0)}
"""
	path.write_text(content, encoding="utf-8")
	return path
