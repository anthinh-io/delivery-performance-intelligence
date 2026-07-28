import json
from pathlib import Path

import joblib
import numpy as np
import shap

from app.preprocessing import FEATURE_COLUMNS, build_feature_vector
from app.schemas import PredictRequest, PredictResponse, RiskGroup

_MODELS_DIR = Path(__file__).resolve().parents[3] / "models"

_model = joblib.load(_MODELS_DIR / "xgboost_final.pkl")
_explainer = shap.TreeExplainer(_model)
DECISION_THRESHOLD = json.loads((_MODELS_DIR / "final_model.json").read_text(encoding="utf-8"))["decision_threshold"]

# Cơ chế 3 nhóm nguyên nhân rủi ro đã chốt ở PR #64 (notebooks/27_risk_group_shap_spike.ipynb).
_STATE_DUMMY_COLUMNS = [
    c for c in FEATURE_COLUMNS if c.startswith("customer_state_") or c.startswith("primary_seller_state_")
]
_CORE_SHIPPING_COLUMNS = ["seller_customer_distance_km", "estimated_delivery_days"]
_SEASONAL_COLUMN = "order_purchase_month"
_PREP_COLUMNS = [
    c
    for c in FEATURE_COLUMNS
    if c not in _STATE_DUMMY_COLUMNS and c not in _CORE_SHIPPING_COLUMNS and c != _SEASONAL_COLUMN
]

SHIPPING_GROUP_NAME = "Vận chuyển"
PREP_GROUP_NAME = "Chuẩn bị & thanh toán"
SEASONAL_GROUP_NAME = "Yếu tố thời điểm"


def _risk_groups(shap_row: np.ndarray, feature_values: list[float]) -> list[RiskGroup]:
    shap_abs = dict(zip(FEATURE_COLUMNS, np.abs(shap_row)))
    values = dict(zip(FEATURE_COLUMNS, feature_values))

    shipping_magnitude = sum(shap_abs[c] for c in _CORE_SHIPPING_COLUMNS)
    shipping_magnitude += sum(shap_abs[c] * values[c] for c in _STATE_DUMMY_COLUMNS)
    prep_magnitude = sum(shap_abs[c] for c in _PREP_COLUMNS)
    seasonal_magnitude = shap_abs[_SEASONAL_COLUMN]

    total_magnitude = shipping_magnitude + prep_magnitude + seasonal_magnitude

    return [
        RiskGroup(name=SHIPPING_GROUP_NAME, contribution_pct=shipping_magnitude / total_magnitude * 100),
        RiskGroup(name=PREP_GROUP_NAME, contribution_pct=prep_magnitude / total_magnitude * 100),
        RiskGroup(name=SEASONAL_GROUP_NAME, contribution_pct=seasonal_magnitude / total_magnitude * 100),
    ]


def predict(request: PredictRequest) -> PredictResponse:
    feature_values = build_feature_vector(request)
    x = np.array([feature_values])

    probability = float(_model.predict_proba(x)[0, 1])
    is_delayed = probability >= DECISION_THRESHOLD

    shap_row = _explainer.shap_values(x)[0]
    risk_groups = _risk_groups(shap_row, feature_values)

    return PredictResponse(is_delayed=is_delayed, probability=probability, risk_groups=risk_groups)
