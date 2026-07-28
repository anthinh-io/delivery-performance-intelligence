import json
from pathlib import Path

import pytest

from app.preprocessing import FEATURE_COLUMNS, build_feature_vector
from app.schemas import PredictRequest

MODELS_DIR = Path(__file__).resolve().parents[3] / "models"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# Đơn hàng thật trong data/processed/orders_features_test.csv, đối chiếu với field
# thô trong data/processed/orders_joined.csv - xem src/api/tests/fixtures/golden_order.json.
GOLDEN = json.loads((FIXTURES_DIR / "golden_order.json").read_text(encoding="utf-8"))


def test_feature_columns_loaded_from_final_model_json():
    final_model = json.loads((MODELS_DIR / "final_model.json").read_text(encoding="utf-8"))
    assert FEATURE_COLUMNS == final_model["feature_columns"]
    assert len(FEATURE_COLUMNS) == 76


def test_build_feature_vector_matches_real_training_row():
    request = PredictRequest(**GOLDEN["request"])
    vector = build_feature_vector(request)

    assert FEATURE_COLUMNS == GOLDEN["feature_columns"]
    assert len(vector) == len(GOLDEN["expected_feature_vector"]) == 76
    for column, actual, expected in zip(FEATURE_COLUMNS, vector, GOLDEN["expected_feature_vector"]):
        assert actual == pytest.approx(expected), f"{column}: {actual} != {expected}"


def test_unknown_customer_zip_gives_all_zero_customer_state_columns():
    payload = dict(GOLDEN["request"])
    payload["customer_zip_code_prefix"] = 999999  # zip không tồn tại trong lookup
    request = PredictRequest(**payload)
    vector = build_feature_vector(request)

    customer_state_values = [
        v for c, v in zip(FEATURE_COLUMNS, vector) if c.startswith("customer_state_")
    ]
    assert customer_state_values == [0.0] * len(customer_state_values)


def test_unknown_zip_falls_back_to_train_median_distance():
    final_model = json.loads((MODELS_DIR / "final_model.json").read_text(encoding="utf-8"))
    train_median = final_model["train_median_distance_km"]

    payload = dict(GOLDEN["request"])
    payload["primary_seller_zip_code_prefix"] = 999999  # zip không có toạ độ
    request = PredictRequest(**payload)
    vector = build_feature_vector(request)

    distance_index = FEATURE_COLUMNS.index("seller_customer_distance_km")
    assert vector[distance_index] == train_median
