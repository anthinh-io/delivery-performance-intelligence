import csv
import sqlite3
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = _REPO_ROOT / "data" / "processed" / "orders_labeled.csv"
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.sqlite3"

# (tên cột, kiểu dữ liệu) khớp thứ tự cột trong data/processed/orders_labeled.csv.
_COLUMNS = [
    ("order_id", "text"),
    ("customer_id", "text"),
    ("order_status", "text"),
    ("order_purchase_timestamp", "text"),
    ("order_approved_at", "text"),
    ("order_delivered_carrier_date", "text"),
    ("order_delivered_customer_date", "text"),
    ("order_estimated_delivery_date", "text"),
    ("items_num_items", "real"),
    ("items_num_products", "real"),
    ("items_num_sellers", "real"),
    ("items_total_price", "real"),
    ("items_total_freight", "real"),
    ("payment_total_value", "real"),
    ("payment_num_rows", "real"),
    ("payment_num_types", "real"),
    ("payment_max_installments", "real"),
    ("payment_value_boleto", "real"),
    ("payment_value_credit_card", "real"),
    ("payment_value_debit_card", "real"),
    ("payment_value_not_defined", "real"),
    ("payment_value_voucher", "real"),
    ("payment_has_boleto", "bool"),
    ("payment_has_credit_card", "bool"),
    ("payment_has_debit_card", "bool"),
    ("payment_has_not_defined", "bool"),
    ("payment_has_voucher", "bool"),
    ("customer_unique_id", "text"),
    ("customer_zip_code_prefix", "int"),
    ("customer_city", "text"),
    ("customer_state", "text"),
    ("primary_seller_id", "text"),
    ("primary_seller_zip_code_prefix", "real"),
    ("primary_seller_city", "text"),
    ("primary_seller_state", "text"),
    ("items_multi_seller", "bool"),
    ("items_num_categories", "real"),
    ("review_score_avg", "real"),
    ("review_score_min", "real"),
    ("review_score_max", "real"),
    ("review_count", "real"),
    ("is_delayed", "bool"),
]

_SQL_TYPE = {"text": "TEXT", "real": "REAL", "int": "INTEGER", "bool": "INTEGER"}


def _cast(value: str, kind: str):
    if value == "":
        return None
    if kind == "text":
        return value
    if kind == "real":
        return float(value)
    if kind == "int":
        return int(float(value))
    if kind == "bool":
        return 1 if value == "True" else 0


def build_database(csv_path: Path, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    columns_sql = ", ".join(f'"{name}" {_SQL_TYPE[kind]}' for name, kind in _COLUMNS)
    column_names = ", ".join(f'"{name}"' for name, _ in _COLUMNS)
    placeholders = ", ".join("?" for _ in _COLUMNS)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DROP TABLE IF EXISTS orders")
        conn.execute(f'CREATE TABLE orders ({columns_sql}, PRIMARY KEY ("order_id"))')

        with open(csv_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = [tuple(_cast(row[name], kind) for name, kind in _COLUMNS) for row in reader]

        conn.executemany(f"INSERT INTO orders ({column_names}) VALUES ({placeholders})", rows)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    build_database(CSV_PATH, DB_PATH)
