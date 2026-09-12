import json
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
