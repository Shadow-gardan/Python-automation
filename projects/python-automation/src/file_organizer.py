from pathlib import Path
import shutil
from typing import Any


FILE_CATEGORIES = {
	"Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
	"Documents": [".pdf", ".doc", ".docx", ".txt"],
	"Spreadsheets": [".csv", ".xls", ".xlsx"],
	"Videos": [".mp4", ".mkv", ".avi", ".mov"],
	"Audio": [".mp3", ".wav", ".flac"],
	"Archives": [".zip", ".tar", ".gz", ".rar"],
}


def get_category(file_path: Path) -> str:
	"""Return the category for a file based on its extension."""
	extension = file_path.suffix.lower()
	for category, extensions in FILE_CATEGORIES.items():
		if extension in extensions:
			return category
	return "Other"


def _unique_destination(destination: Path) -> Path:
	"""Return a non-existing path when a file name is already in use."""
	if not destination.exists():
		return destination

	counter = 1
	while True:
		candidate = destination.with_name(
			f"{destination.stem}_{counter}{destination.suffix}"
		)
		if not candidate.exists():
			return candidate
		counter += 1


def organize_files(input_directory: str | Path, output_directory: str | Path) -> dict[str, Any]:
	"""Copy input files into type folders and return processing statistics."""
	input_path = Path(input_directory)
	output_path = Path(output_directory)

	if not input_path.exists():
		raise FileNotFoundError(f"Input directory does not exist: {input_path}")
	if not input_path.is_dir():
		raise NotADirectoryError(f"Input path is not a directory: {input_path}")

	output_path.mkdir(parents=True, exist_ok=True)
	files_by_category: dict[str, int] = {}
	files_copied = 0
	files_skipped = 0

	for file_path in sorted(input_path.iterdir()):
		if not file_path.is_file():
			files_skipped += 1
			continue

		category = get_category(file_path)
		category_directory = output_path / category
		category_directory.mkdir(parents=True, exist_ok=True)
		destination = _unique_destination(category_directory / file_path.name)
		shutil.copy2(file_path, destination)
		files_copied += 1
		files_by_category[category] = files_by_category.get(category, 0) + 1

	return {
		"total_files": files_copied + files_skipped,
		"files_copied": files_copied,
		"files_skipped": files_skipped,
		"files_by_category": files_by_category,
	}
