import json
import math
from pathlib import Path

from app.schemas import PredictRequest

_MODELS_DIR = Path(__file__).resolve().parents[3] / "models"

_final_model = json.loads((_MODELS_DIR / "final_model.json").read_text(encoding="utf-8"))
FEATURE_COLUMNS = _final_model["feature_columns"]
TRAIN_MEDIAN_DISTANCE_KM = _final_model["train_median_distance_km"]

_zip_state_lookup = json.loads((_MODELS_DIR / "zip_state_lookup.json").read_text(encoding="utf-8"))
CUSTOMER_STATE_BY_ZIP = _zip_state_lookup["customer_state_by_zip"]
SELLER_STATE_BY_ZIP = _zip_state_lookup["primary_seller_state_by_zip"]

ZIP_GEO_LOOKUP = json.loads((_MODELS_DIR / "zip_geo_lookup.json").read_text(encoding="utf-8"))


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))


def _distance_km(customer_zip: int, seller_zip: int) -> float:
    customer_coord = ZIP_GEO_LOOKUP.get(str(customer_zip))
    seller_coord = ZIP_GEO_LOOKUP.get(str(seller_zip))
    if customer_coord is None or seller_coord is None:
        return TRAIN_MEDIAN_DISTANCE_KM
    return _haversine_km(customer_coord[0], customer_coord[1], seller_coord[0], seller_coord[1])


def build_feature_vector(request: PredictRequest) -> list[float]:
    approval_gap_hours = (
        request.order_approved_at - request.order_purchase_timestamp
    ).total_seconds() / 3600
    estimated_delivery_days = (
        request.order_estimated_delivery_date - request.order_purchase_timestamp
    ).total_seconds() / 86400
    order_purchase_month = request.order_purchase_timestamp.month

    customer_state = CUSTOMER_STATE_BY_ZIP.get(str(request.customer_zip_code_prefix))
    seller_state = SELLER_STATE_BY_ZIP.get(str(request.primary_seller_zip_code_prefix))
    distance_km = _distance_km(request.customer_zip_code_prefix, request.primary_seller_zip_code_prefix)

    values = {
        "items_num_items": request.items_num_items,
        "items_num_products": request.items_num_products,
        "items_num_sellers": request.items_num_sellers,
        "items_total_price": request.items_total_price,
        "items_total_freight": request.items_total_freight,
        "items_num_categories": request.items_num_categories,
        "items_total_weight_g": request.items_total_weight_g,
        "payment_total_value": request.payment_total_value,
        "payment_num_rows": request.payment_num_rows,
        "payment_num_types": request.payment_num_types,
        "payment_max_installments": request.payment_max_installments,
        "payment_value_boleto": request.payment_value_boleto,
        "payment_value_credit_card": request.payment_value_credit_card,
        "payment_value_debit_card": request.payment_value_debit_card,
        "payment_value_not_defined": request.payment_value_not_defined,
        "payment_value_voucher": request.payment_value_voucher,
        "approval_gap_hours": approval_gap_hours,
        "estimated_delivery_days": estimated_delivery_days,
        "order_purchase_month": float(order_purchase_month),
        "payment_has_boleto": float(request.payment_has_boleto),
        "payment_has_credit_card": float(request.payment_has_credit_card),
        "payment_has_debit_card": float(request.payment_has_debit_card),
        "payment_has_not_defined": float(request.payment_has_not_defined),
        "payment_has_voucher": float(request.payment_has_voucher),
        "items_multi_seller": float(request.items_multi_seller),
        "seller_customer_distance_km": distance_km,
    }

    for column in FEATURE_COLUMNS:
        if column.startswith("customer_state_"):
            values[column] = 1.0 if column == f"customer_state_{customer_state}" else 0.0
        elif column.startswith("primary_seller_state_"):
            values[column] = 1.0 if column == f"primary_seller_state_{seller_state}" else 0.0

    return [float(values[column]) for column in FEATURE_COLUMNS]
