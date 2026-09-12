import tempfile
import unittest
from pathlib import Path

from src.file_organizer import get_category, organize_files


class FileOrganizerTests(unittest.TestCase):
	def test_missing_input_directory(self):
		with tempfile.TemporaryDirectory() as directory:
			with self.assertRaises(FileNotFoundError):
				organize_files(Path(directory) / "missing", Path(directory) / "output")

	def test_get_category_is_case_insensitive(self):
		self.assertEqual(get_category(Path("photo.PNG")), "Images")
		self.assertEqual(get_category(Path("unknown.xyz")), "Other")

	def test_organize_files_copies_files_into_categories(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			input_directory = root / "input"
			output_directory = root / "output"
			input_directory.mkdir()
			(input_directory / "report.pdf").write_text("report")
			(input_directory / "photo.jpg").write_text("photo")
			(input_directory / "notes.xyz").write_text("notes")
			(input_directory / "nested").mkdir()

			stats = organize_files(str(input_directory), str(output_directory))

			self.assertEqual(
				(output_directory / "Documents" / "report.pdf").read_text(),
				"report",
			)
			self.assertTrue((output_directory / "Images" / "photo.jpg").exists())
			self.assertTrue((output_directory / "Other" / "notes.xyz").exists())
			self.assertEqual(stats["files_copied"], 3)
			self.assertEqual(stats["files_skipped"], 1)

	def test_duplicate_names_are_preserved(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			input_directory = root / "input"
			output_directory = root / "output"
			input_directory.mkdir()
			(input_directory / "report.txt").write_text("new")
			documents = output_directory / "Documents"
			documents.mkdir(parents=True)
			(documents / "report.txt").write_text("old")

			organize_files(str(input_directory), str(output_directory))

			self.assertEqual((documents / "report.txt").read_text(), "old")
			self.assertEqual((documents / "report_1.txt").read_text(), "new")


if __name__ == "__main__":
	unittest.main()
