import sqlite3
from pathlib import Path

from app.db import build_database

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SAMPLE_CSV = FIXTURES_DIR / "orders_sample.csv"


def test_build_database_loads_all_rows_from_csv(tmp_path):
    db_path = tmp_path / "orders.sqlite3"
    build_database(SAMPLE_CSV, db_path)

    conn = sqlite3.connect(db_path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    finally:
        conn.close()

    assert count == 3


def test_build_database_preserves_values_and_types(tmp_path):
    db_path = tmp_path / "orders.sqlite3"
    build_database(SAMPLE_CSV, db_path)

    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT order_status, items_total_price, customer_zip_code_prefix,
                   payment_has_credit_card, items_multi_seller, is_delayed
            FROM orders WHERE order_id = ?
            """,
            ("aaa1",),
        ).fetchone()
    finally:
        conn.close()

    assert row == ("delivered", 29.99, 3149, 1, 0, 0)


def test_build_database_marks_delayed_order(tmp_path):
    db_path = tmp_path / "orders.sqlite3"
    build_database(SAMPLE_CSV, db_path)

    conn = sqlite3.connect(db_path)
    try:
        is_delayed = conn.execute(
            "SELECT is_delayed FROM orders WHERE order_id = ?", ("bbb2",)
        ).fetchone()[0]
    finally:
        conn.close()

    assert is_delayed == 1


def test_build_database_stores_missing_values_as_null(tmp_path):
    db_path = tmp_path / "orders.sqlite3"
    build_database(SAMPLE_CSV, db_path)

    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT order_delivered_carrier_date, order_delivered_customer_date,
                   primary_seller_zip_code_prefix, review_score_avg, is_delayed
            FROM orders WHERE order_id = ?
            """,
            ("ccc3",),
        ).fetchone()
    finally:
        conn.close()

    assert row == (None, None, None, None, None)


def test_build_database_is_idempotent_when_rerun(tmp_path):
    db_path = tmp_path / "orders.sqlite3"
    build_database(SAMPLE_CSV, db_path)
    build_database(SAMPLE_CSV, db_path)

    conn = sqlite3.connect(db_path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    finally:
        conn.close()

    assert count == 3
