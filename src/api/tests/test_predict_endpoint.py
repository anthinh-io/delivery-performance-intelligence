import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
GOLDEN = json.loads((FIXTURES_DIR / "golden_order.json").read_text(encoding="utf-8"))


def test_predict_endpoint_returns_200_with_expected_shape():
    response = client.post("/predict", json=GOLDEN["request"])

    assert response.status_code == 200
    body = response.json()
    assert body["is_delayed"] == GOLDEN["expected_is_delayed"]
    assert body["probability"] == pytest.approx(GOLDEN["expected_probability"], abs=1e-4)
    assert len(body["risk_groups"]) == 3
    assert {g["name"] for g in body["risk_groups"]} == {
        "Vận chuyển",
        "Chuẩn bị & thanh toán",
        "Yếu tố thời điểm",
    }


def test_predict_endpoint_rejects_invalid_payload():
    payload = dict(GOLDEN["request"])
    del payload["items_total_price"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
