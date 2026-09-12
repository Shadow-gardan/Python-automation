from pathlib import Path

from src.data_cleaner import clean_sales_data


CSV_HEADER = "order_id,order_date,customer_id,customer_name,city,product_id,product_name,category,quantity,unit_price\n"


def test_clean_sales_data_removes_duplicates_and_rejects_invalid_rows(tmp_path: Path):
    input_path = tmp_path / "sales.csv"
    output_path = tmp_path / "output" / "cleaned.csv"
    row = "1,2025-01-01,1, Ava  , London ,101, Keyboard,Electronics,2,10.00\n"
    input_path.write_text(CSV_HEADER + row + row + "2,bad,1,Ben,Leeds,102,Hub,Electronics,1,20.00\n")

    stats = clean_sales_data(input_path, output_path)

    assert stats.input_rows == 3
    assert stats.duplicate_rows == 1
    assert stats.rejected_rows == 1
    assert stats.output_rows == 1
    assert " Ava  " in input_path.read_text()
    assert "Ava" in output_path.read_text()


def test_clean_sales_data_creates_output_parent(tmp_path: Path):
    input_path = tmp_path / "sales.csv"
    input_path.write_text(CSV_HEADER + "1,2025-01-01,1,Ava,London,101,Keyboard,Electronics,2,10.00\n")

    output_path = tmp_path / "nested" / "cleaned.csv"
    clean_sales_data(input_path, output_path)

    assert output_path.exists()
