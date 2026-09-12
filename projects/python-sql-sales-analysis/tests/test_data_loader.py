from pathlib import Path

import pytest

from src.data_loader import load_sales_csv, validate_sales_records


def test_load_sales_csv_normalizes_headers_and_values(tmp_path: Path):
    path = tmp_path / "sales.csv"
    path.write_text(
        "Order_ID,Order_Date,Customer_ID,Customer_Name,City,Product_ID,Product_Name,Category,Quantity,Unit_Price\n"
        "1,2025-01-01,1,Ava,London,101,Keyboard,Electronics,2,10.00\n"
    )

    records = load_sales_csv(path)

    assert records[0]["order_id"] == "1"
    assert records[0]["unit_price"] == "10.00"


def test_load_sales_csv_missing_input_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_sales_csv(tmp_path / "missing.csv")


def test_validate_sales_records_reports_invalid_values():
    result = validate_sales_records(
        [{"order_id": "", "order_date": "bad", "customer_id": "1", "customer_name": "", "city": "London", "product_id": "101", "product_name": "Keyboard", "category": "Electronics", "quantity": "0", "unit_price": "bad"}]
    )

    assert len(result.valid_records) == 0
    assert "missing order_id" in result.issues[0].message
    assert "invalid order_date" in result.issues[0].message
