# Sơ đồ quan hệ (ERD) — bộ dữ liệu Olist

```mermaid
erDiagram
    olist_orders_dataset {
        string order_id PK
        string customer_id FK
        string order_status
        datetime order_purchase_timestamp
        datetime order_approved_at
        datetime order_delivered_carrier_date
        datetime order_delivered_customer_date
        datetime order_estimated_delivery_date
    }

    olist_customers_dataset {
        string customer_id PK
        string customer_unique_id
        int customer_zip_code_prefix FK
        string customer_city
        string customer_state
    }

    olist_order_items_dataset {
        string order_id PK "cũng là FK tới orders"
        int order_item_id PK
        string product_id FK
        string seller_id FK
        datetime shipping_limit_date
        float price
        float freight_value
    }

    olist_order_payments_dataset {
        string order_id PK "cũng là FK tới orders"
        int payment_sequential PK
        string payment_type
        int payment_installments
        float payment_value
    }

    olist_order_reviews_dataset {
        string review_id PK "không unique"
        string order_id FK
        int review_score
        string review_comment_title
        string review_comment_message
        datetime review_creation_date
        datetime review_answer_timestamp
    }

    olist_products_dataset {
        string product_id PK
        string product_category_name FK
        float product_name_lenght
        float product_description_lenght
        float product_photos_qty
        float product_weight_g
        float product_length_cm
        float product_height_cm
        float product_width_cm
    }

    olist_sellers_dataset {
        string seller_id PK
        int seller_zip_code_prefix FK
        string seller_city
        string seller_state
    }

    olist_geolocation_dataset {
        int geolocation_zip_code_prefix "không unique"
        float geolocation_lat
        float geolocation_lng
        string geolocation_city
        string geolocation_state
    }

    product_category_name_translation {
        string product_category_name PK
        string product_category_name_english
    }

    olist_orders_dataset ||--|| olist_customers_dataset : "customer_id (1-1, xem ghi chú)"
    olist_orders_dataset ||--o{ olist_order_items_dataset : order_id
    olist_orders_dataset ||--o{ olist_order_payments_dataset : order_id
    olist_orders_dataset ||--o{ olist_order_reviews_dataset : order_id
    olist_order_items_dataset }o--|| olist_products_dataset : product_id
    olist_order_items_dataset }o--|| olist_sellers_dataset : seller_id
    olist_products_dataset }o--o| product_category_name_translation : product_category_name
    olist_customers_dataset }o--o{ olist_geolocation_dataset : zip_code_prefix
    olist_sellers_dataset }o--o{ olist_geolocation_dataset : zip_code_prefix
```

## Ghi chú quan trọng khi đọc sơ đồ

- **`orders` ↔ `customers` là quan hệ 1-1, không phải 1-nhiều.** Theo mô tả chính thức trên Kaggle: `customer_id` được sinh mới cho mỗi đơn hàng, kể cả cùng một người mua nhiều lần. Muốn nhận diện khách hàng thật (gộp các lần mua lại) phải dùng `customer_unique_id`, cột này **không phải khóa chính/khóa ngoại join với bảng nào khác** trong 9 bảng.
- **Join qua zip code (`*_zip_code_prefix` ↔ `geolocation_zip_code_prefix`) là nhiều-nhiều, không phải khóa ngoại chuẩn.** `olist_geolocation_dataset` không có cột định danh duy nhất — nhiều dòng lat/lng khác nhau có thể cùng một `geolocation_zip_code_prefix`. Join trực tiếp sẽ làm phình số dòng (fan-out), đã dedupe bằng `groupby("geolocation_zip_code_prefix")` lấy trung bình lat/lng, join vào `customer_zip_code_prefix` và `primary_seller_zip_code_prefix`, tính khoảng cách haversine ra đặc trưng `seller_customer_distance_km` (dùng trong model cuối, xem `models/final_model.json`).
- **`product_category_name` có thể null** ở `olist_products_dataset` (sản phẩm chưa phân loại) nên join với `product_category_name_translation` là optional (ký hiệu `o|` — zero hoặc một, không bắt buộc).
- **Khóa chính là khóa kép (composite)** ở 2 bảng: `olist_order_items_dataset` (`order_id` + `order_item_id`) và `olist_order_payments_dataset` (`order_id` + `payment_sequential`) — một `order_id` có nhiều dòng trong 2 bảng này.
- **`review_id` không phải khóa duy nhất trên thực tế**, dù về mặt thiết kế được coi là PK. Kiểm tra dữ liệu thô (Task #22) phát hiện 814 dòng trùng `review_id` (789 giá trị bị lặp, có giá trị lặp tới 3 lần), không do giá trị thiếu. Khi join `olist_order_reviews_dataset` vào `olist_orders_dataset` ở Sprint 2 cần cân nhắc dedupe hoặc chấp nhận fan-out có kiểm soát.

## Chi tiết khóa chính – khóa ngoại từng bảng

| Bảng | Khóa chính (PK) | Khóa ngoại (FK) | Trỏ tới |
|---|---|---|---|
| `olist_orders_dataset` | `order_id` | `customer_id` | `olist_customers_dataset.customer_id` |
| `olist_customers_dataset` | `customer_id` | `customer_zip_code_prefix` | `olist_geolocation_dataset.geolocation_zip_code_prefix` (không unique, xem ghi chú) |
| `olist_order_items_dataset` | `order_id` + `order_item_id` (composite) | `order_id`, `product_id`, `seller_id` | `olist_orders_dataset.order_id`, `olist_products_dataset.product_id`, `olist_sellers_dataset.seller_id` |
| `olist_order_payments_dataset` | `order_id` + `payment_sequential` (composite) | `order_id` | `olist_orders_dataset.order_id` |
| `olist_order_reviews_dataset` | `review_id` (không unique thật sự, xem ghi chú) | `order_id` | `olist_orders_dataset.order_id` |
| `olist_products_dataset` | `product_id` | `product_category_name` (có thể null) | `product_category_name_translation.product_category_name` |
| `olist_sellers_dataset` | `seller_id` | `seller_zip_code_prefix` | `olist_geolocation_dataset.geolocation_zip_code_prefix` (không unique, xem ghi chú) |
| `olist_geolocation_dataset` | không có (không có cột định danh duy nhất) | — | — |
| `product_category_name_translation` | `product_category_name` | — | — |
