from pathlib import Path

from src.report_generator import write_text_report


def test_text_report_does_not_overwrite_existing_report(tmp_path: Path):
    report_path = tmp_path / "report.txt"
    report_path.write_text("original")

    generated_path = write_text_report(
        {"total_files": 1},
        {"final_row_count": 1},
        {"total_customers": 1},
        report_path,
    )

    assert generated_path != report_path
    assert report_path.read_text() == "original"
    assert "Customers: 1" in generated_path.read_text()