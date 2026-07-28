import json
from pathlib import Path

import pytest

from app.model import predict
from app.schemas import PredictRequest

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
GOLDEN = json.loads((FIXTURES_DIR / "golden_order.json").read_text(encoding="utf-8"))


def test_predict_matches_real_training_row():
    request = PredictRequest(**GOLDEN["request"])
    response = predict(request)

    assert response.probability == pytest.approx(GOLDEN["expected_probability"], abs=1e-4)
    assert response.is_delayed == GOLDEN["expected_is_delayed"]

    pct_by_name = {g.name: g.contribution_pct for g in response.risk_groups}
    assert pct_by_name["Vận chuyển"] == pytest.approx(GOLDEN["expected_risk_group_pct"]["shipping"], abs=1e-2)
    assert pct_by_name["Chuẩn bị & thanh toán"] == pytest.approx(GOLDEN["expected_risk_group_pct"]["prep"], abs=1e-2)
    assert pct_by_name["Yếu tố thời điểm"] == pytest.approx(GOLDEN["expected_risk_group_pct"]["seasonal"], abs=1e-2)


def test_risk_group_percentages_sum_to_100():
    request = PredictRequest(**GOLDEN["request"])
    response = predict(request)

    total_pct = sum(g.contribution_pct for g in response.risk_groups)
    assert total_pct == pytest.approx(100.0, abs=1e-3)
    assert len(response.risk_groups) == 3
