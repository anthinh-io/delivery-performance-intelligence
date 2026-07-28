from datetime import datetime

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    items_num_items: int
    items_num_products: int
    items_num_sellers: int
    items_total_price: float
    items_total_freight: float
    items_num_categories: int
    items_total_weight_g: float
    items_multi_seller: bool

    payment_total_value: float
    payment_num_rows: int
    payment_num_types: int
    payment_max_installments: int
    payment_value_boleto: float
    payment_value_credit_card: float
    payment_value_debit_card: float
    payment_value_not_defined: float
    payment_value_voucher: float
    payment_has_boleto: bool
    payment_has_credit_card: bool
    payment_has_debit_card: bool
    payment_has_not_defined: bool
    payment_has_voucher: bool

    order_purchase_timestamp: datetime
    order_approved_at: datetime
    order_estimated_delivery_date: datetime

    customer_zip_code_prefix: int
    primary_seller_zip_code_prefix: int


class RiskGroup(BaseModel):
    name: str
    contribution_pct: float


class PredictResponse(BaseModel):
    is_delayed: bool
    probability: float = Field(ge=0.0, le=1.0)
    risk_groups: list[RiskGroup]
