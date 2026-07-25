# Danh sách đặc trưng — Story #7, Task #40

Chốt tại Iteration 2 (2026-07-24/25), tổng hợp từ Story #6 (`notebooks/11-13`), Task #38 (`notebooks/14_explore_candidate_features.ipynb`), Task #39 (`notebooks/15_region_pair_encoding_options.ipynb`). Nguồn dữ liệu: `data/processed/orders_labeled.csv` (99.441 dòng, 42 cột) + join bổ sung `order_items`/`products` cho khối lượng đơn hàng.

**Ràng buộc quan trọng nhất khi chọn danh sách này: đặc trưng chỉ được dùng nếu giá trị của nó ĐÃ CÓ tại thời điểm API dự đoán được gọi** (đơn hàng mới, đã duyệt thanh toán — xem mục "Giả định thời điểm dự đoán" bên dưới). Đây là ranh giới chống rò rỉ dữ liệu (data leakage) bắt buộc theo DoD (`docs/agile-playbook.md` mục 6).

## Giả định thời điểm dự đoán (đã xác nhận với User)

API dự đoán được gọi **sau khi đơn hàng đã duyệt thanh toán** (không phải ngay lúc khách bấm mua) — phù hợp bối cảnh "người quản lý vận hành nhập thông tin đơn hàng đang xử lý" (Story #13). Giả định này quyết định `order_approved_at`/`approval_gap_hours` hợp lệ làm đặc trưng; nếu sau này đổi giả định (API gọi ngay lúc đặt hàng, trước duyệt), phải loại `approval_gap_hours` khỏi danh sách.

## Đặc trưng SỐ (numeric)

| Đặc trưng | Nguồn | Cần tính thêm? | Tín hiệu (Story #6 / Task #38-40) |
|---|---|---|---|
| `items_num_items` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng — đưa vào theo domain knowledge (quy mô đơn) |
| `items_num_products` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `items_num_sellers` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `items_total_price` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `items_total_freight` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `items_num_categories` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `items_total_weight_g` | Task #38 — join `order_items`+`products` | **Có** — chưa có trong `orders_labeled.csv` | Yếu (7,39%→8,89%, không đơn điệu) |
| `payment_total_value` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `payment_num_rows` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `payment_num_types` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `payment_max_installments` | Story #4 (có sẵn) | Không | Chưa khảo sát riêng |
| `payment_value_boleto/credit_card/debit_card/not_defined/voucher` (5 cột) | Story #4 (có sẵn) | Không | Yếu ở mức hình thức thanh toán tổng hợp (7,01–8,88%, Story #6) |
| `approval_gap_hours` | Task #38 — tính từ `order_approved_at − order_purchase_timestamp` | **Có** | Trung bình (6,90%→9,73%, đơn điệu). **Chỉ hợp lệ với giả định thời điểm dự đoán ở trên** |
| `estimated_delivery_days` | Task #40 — tính từ `order_estimated_delivery_date − order_purchase_timestamp` | **Có** | Trung bình-khá (8,56%→9,66%→8,82%→8,13%→5,40%; ước tính càng dài, trễ càng thấp) |
| `order_purchase_month` | Task #40 — tính từ tháng của `order_purchase_timestamp` (1–12) | **Có** | Biên độ lớn (2,21%→17,15%) nhưng **cảnh báo confound** — xem mục "Lưu ý" |

## Đặc trưng PHÂN LOẠI (categorical / boolean)

| Đặc trưng | Nguồn | Tín hiệu |
|---|---|---|
| `customer_state` | Story #4 (có sẵn) | **Mạnh nhất** — RO 2,88% → AL 23,93% (Story #6 + Task #39) |
| `primary_seller_state` | Story #4 (có sẵn) | **Mạnh nhất**, dùng riêng thay vì ghép cặp — quyết định Task #39 (Phương án A) |
| `payment_has_boleto/credit_card/debit_card/not_defined/voucher` (5 cột, boolean) | Story #4 (có sẵn) | Yếu (Story #6) |
| `items_multi_seller` (boolean) | Story #4 (có sẵn) | Chưa khảo sát riêng |

## Nhãn mục tiêu (không phải đặc trưng)

- `is_delayed` — Story #5, pandas nullable boolean (True/False/NA). Dùng Phương án A (loại NA) làm tập huấn luyện chính (Story #6).

## Đặc trưng LOẠI BỎ — rò rỉ dữ liệu (bắt buộc, không phải lựa chọn)

| Cột | Lý do loại |
|---|---|
| `order_delivered_customer_date` | Chính là cột dùng để **tính ra** `is_delayed` (Story #5) — rò rỉ nhãn trực tiếp |
| `order_delivered_carrier_date` | Chỉ có sau khi đơn được giao cho đơn vị vận chuyển — đơn mới chưa có |
| `review_score_avg`, `review_score_min`, `review_score_max`, `review_count` | Review chỉ có sau khi khách nhận hàng — đơn mới chưa có |
| `order_status` | Giá trị (`delivered`/`shipped`/...) đổi theo vòng đời đơn — trạng thái sau này tự rò rỉ kết quả |
| `order_purchase_timestamp`, `order_approved_at`, `order_estimated_delivery_date` (dạng raw datetime) | Không dùng trực tiếp — đã tách thành đặc trưng số ở trên (`approval_gap_hours`, `estimated_delivery_days`, `order_purchase_month`); giữ nguyên timestamp làm cột số không tổng quát hóa được |

## Chưa đưa vào — để dành cho story sau (không phải loại bỏ vĩnh viễn)

- `customer_zip_code_prefix`, `customer_city`, `primary_seller_zip_code_prefix`, `primary_seller_city`, `primary_seller_id` — độ chi tiết cao hơn state nhưng chưa khảo sát tín hiệu; state đã là tín hiệu mạnh nhất tìm được, thêm chi tiết hơn có nguy cơ overfit/thưa mẫu tương tự vấn đề đã gặp ở Task #39.
- Đặc trưng khoảng cách địa lý (lat/lng, bảng `geolocation`) — bảng chưa join do ~26% dòng trùng lặp (mục 4.8, tài liệu bàn giao); để dành nếu Story #8 cần độ chính xác cao hơn cấp state.

## Lưu ý khi diễn giải `order_purchase_month`

Dữ liệu chỉ trải ~2 năm không trọn (9/2016–10/2018), phần lớn tháng chỉ xuất hiện 1 lần trong dữ liệu. Tín hiệu biên độ lớn (2,21%→17,15%) gần như đồng nhất với chính 3 tháng bất thường đã phát hiện ở Story #6 (2017-11, 2018-02, 2018-03), **không phải bằng chứng về chu kỳ mùa vụ lặp lại hằng năm**. Đưa vào danh sách theo quyết định của User (Task #40) nhưng khi trình bày kết quả mô hình/tầm quan trọng đặc trưng, phải ghi rõ giới hạn này, tránh diễn giải sai thành quy luật mùa vụ đã được xác nhận.
