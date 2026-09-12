from pathlib import Path

from src.analytics import run_all_analytics
from src.report_generator import write_sales_report


def test_report_contains_business_sections(sales_connection, tmp_path: Path):
    report_path = write_sales_report(run_all_analytics(sales_connection), tmp_path)
    content = report_path.read_text()

    assert report_path.name.startswith("sales_report_")
    assert "Executive Summary" in content
    assert "Top Products by Revenue" in content
    assert "Revenue by City" in content
    assert "Monthly Revenue" in content
    assert "Total Revenue: $105.00" in content


def test_report_does_not_overwrite_same_timestamp(tmp_path: Path, sales_connection):
    analysis = run_all_analytics(sales_connection)
    first = write_sales_report(analysis, tmp_path)
    second = write_sales_report(analysis, tmp_path)

    assert first != second
    assert first.exists()
    assert second.exists()
