import pytest
from pydantic import ValidationError

from app.schemas import PredictRequest, PredictResponse, RiskGroup

VALID_PAYLOAD = {
    "items_num_items": 2,
    "items_num_products": 2,
    "items_num_sellers": 1,
    "items_total_price": 150.0,
    "items_total_freight": 20.0,
    "items_num_categories": 1,
    "items_total_weight_g": 500.0,
    "items_multi_seller": False,
    "payment_total_value": 170.0,
    "payment_num_rows": 1,
    "payment_num_types": 1,
    "payment_max_installments": 3,
    "payment_value_boleto": 0.0,
    "payment_value_credit_card": 170.0,
    "payment_value_debit_card": 0.0,
    "payment_value_not_defined": 0.0,
    "payment_value_voucher": 0.0,
    "payment_has_boleto": False,
    "payment_has_credit_card": True,
    "payment_has_debit_card": False,
    "payment_has_not_defined": False,
    "payment_has_voucher": False,
    "order_purchase_timestamp": "2018-01-01T10:00:00",
    "order_approved_at": "2018-01-01T12:00:00",
    "order_estimated_delivery_date": "2018-01-15T00:00:00",
    "customer_zip_code_prefix": 1310,
    "primary_seller_zip_code_prefix": 4567,
}


def test_predict_request_accepts_valid_payload():
    request = PredictRequest(**VALID_PAYLOAD)
    assert request.customer_zip_code_prefix == 1310
    assert request.items_multi_seller is False


def test_predict_request_rejects_missing_field():
    payload = dict(VALID_PAYLOAD)
    del payload["items_total_price"]
    with pytest.raises(ValidationError):
        PredictRequest(**payload)


def test_predict_request_rejects_wrong_type():
    payload = dict(VALID_PAYLOAD)
    payload["items_total_price"] = "not-a-number"
    with pytest.raises(ValidationError):
        PredictRequest(**payload)


def test_predict_response_shape():
    response = PredictResponse(
        is_delayed=True,
        probability=0.62,
        risk_groups=[
            RiskGroup(name="Vận chuyển", contribution_pct=60.3),
            RiskGroup(name="Chuẩn bị & thanh toán", contribution_pct=28.5),
            RiskGroup(name="Yếu tố thời điểm", contribution_pct=11.1),
        ],
    )
    assert response.risk_groups[0].name == "Vận chuyển"


def test_predict_response_rejects_probability_out_of_range():
    with pytest.raises(ValidationError):
        PredictResponse(is_delayed=True, probability=1.5, risk_groups=[])
