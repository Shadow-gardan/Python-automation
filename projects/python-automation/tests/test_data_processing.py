import json
import tempfile
import unittest
from pathlib import Path

from src.data_processor import load_records
from src.report_generator import summarize_records, write_report


class DataProcessingTests(unittest.TestCase):
    def test_load_records_normalizes_csv_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.csv"
            path.write_text("Product Name,Quantity\n Widget , 2 \n,,\n")

            self.assertEqual(
                load_records(path),
                [{"product_name": "Widget", "quantity": "2"}],
            )

    def test_json_records_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "records.json"
            report_path = root / "reports" / "summary.json"
            input_path.write_text(json.dumps([{"Name": "Ada", "Score": 10}]))

            records = load_records(input_path)
            self.assertEqual(records, [{"name": "Ada", "score": 10}])
            self.assertEqual(summarize_records(records)["record_count"], 1)
            write_report(records, report_path)
            self.assertEqual(json.loads(report_path.read_text())["fields"], ["name", "score"])


if __name__ == "__main__":
    unittest.main()