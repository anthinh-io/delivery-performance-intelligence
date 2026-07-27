# Báo cáo thu hoạch — Giai đoạn 1 & Giai đoạn 2

*Dự án IE207 — Delivery Performance Intelligence. Báo cáo tổng hợp sau Giai đoạn 1 (Phân tích & khám phá dữ liệu) và Giai đoạn 2 (Xây dựng mô hình học máy).*

---

## 1. Tóm tắt dự án & mục tiêu ban đầu

Dự án xây dựng hệ thống 2 phần kết nối qua REST API: (1) API dự đoán rủi ro giao trễ bằng học máy, huấn luyện trên bộ dữ liệu Olist Brazilian E-Commerce (~100.000 đơn hàng thật, 2016–2018); (2) Dashboard vận hành trên web (React/Next.js + FastAPI) theo dõi KPI, quản lý đơn hàng, dự đoán rủi ro thời gian thực.

Mục tiêu chất lượng mô hình ban đầu: **F1 ≥ 0.78** trên bài toán phân loại đúng hạn/trễ. Đây là con số đặt ra ở giai đoạn lập kế hoạch, trước khi có bất kỳ số liệu thực nghiệm nào — và là điểm mấu chốt của toàn bộ Giai đoạn 2 (xem mục 4).

## 2. Giai đoạn 1 — Phân tích & khám phá dữ liệu

**Công việc đã thực hiện**:

- Tải và giải nén bộ dữ liệu Olist (9 bảng CSV, ~126MB), kiểm tra chất lượng dữ liệu thô (dtype, trùng lặp, null).
- Vẽ sơ đồ quan hệ (ERD) giữa 9 bảng, ghi chú khóa chính/khóa ngoại.
- Join 9 bảng thành 1 dataset mức đơn hàng (`orders_joined.csv`), aggregate `order_items`/`order_payments` trước khi join, chọn `primary_seller` theo giá trị đơn hàng cao nhất khi 1 đơn có nhiều người bán.
- Tính nhãn mục tiêu `is_delayed` (đơn giao thực tế trễ hơn ngày dự kiến), xử lý ~2.9% đơn thiếu ngày giao thực tế.
- Phân tích tỉ lệ mất cân bằng (đơn trễ chỉ ~7–8% tổng số đơn) và xu hướng theo thời gian/vùng miền/hình thức thanh toán — phát hiện 3 tháng bất thường (2017-11, 2018-02, 2018-03) có tỉ lệ trễ cao đột biến.
- Phác thảo wireframe 3 màn hình chính (dashboard KPI, quản lý đơn hàng, biểu mẫu dự đoán), chốt danh sách đặc trưng cuối cùng (`docs/feature-list.md`) — xác định rõ ràng nhóm cột phải loại bỏ vì rò rỉ dữ liệu (VD: `order_delivered_customer_date` — chính là cột dùng để tính nhãn).

**Kết quả bàn giao**: dataset đã join + gắn nhãn (`orders_joined.csv`, `orders_labeled.csv`), ERD, wireframe, danh sách đặc trưng đã chốt kèm ràng buộc chống rò rỉ dữ liệu tường minh.

**Bài học kỹ thuật (ML)**: mất cân bằng dữ liệu (~8% lớp dương) là ràng buộc trung tâm chi phối toàn bộ lựa chọn kỹ thuật ở Giai đoạn 2 — không thể dùng accuracy làm thước đo (một model đoán "không đơn nào trễ" vẫn đạt ~92% accuracy nhưng vô dụng), phải dùng F1/Precision/Recall trên lớp thiểu số.

## 3. Giai đoạn 2 — Xây dựng mô hình học máy

**Công việc đã thực hiện**:

- Xây dựng đặc trưng: `approval_gap_hours`, `estimated_delivery_days`, `order_purchase_month`, one-hot vùng (`customer_state`, `primary_seller_state` — riêng biệt thay vì ghép cặp, tránh thưa mẫu).
- Xử lý mất cân bằng bằng `class_weight`/`scale_pos_weight` tính theo tỉ lệ nghịch đảo tần suất lớp (không resample), chia train/test 80/20 stratified theo `is_delayed`.
- Huấn luyện & so sánh 3 mô hình baseline: Logistic Regression, Random Forest, XGBoost — XGBoost tốt nhất (F1=0.312 ở ngưỡng mặc định 0.5).
- Chẩn đoán trần chất lượng thật: tinh ngưỡng phân loại qua toàn bộ đường cong Precision-Recall (F1 tối đa chỉ lên 0.353, PR-AUC 0.281) — xác nhận nghẽn không phải do chọn sai ngưỡng mà do **tín hiệu yếu** trong tập đặc trưng hiện có.
- Thử đòn bẩy nâng tín hiệu: thêm đặc trưng khoảng cách người bán↔khách hàng (haversine, join bảng `geolocation` theo `zip_code_prefix`, aggregate bằng median để né ~26% dòng trùng lặp) — chỉ cải thiện F1 thêm +0.005.
- Thử điều chỉnh `scale_pos_weight` (quét 1.0–11.32) — chỉ cải thiện thêm +0.002, nằm trong biên độ nhiễu.
- Đóng gói model cuối cùng: XGBoost, có đặc trưng khoảng cách, `scale_pos_weight=6.0`, ngưỡng quyết định 0.539 — **F1=0.353, Precision=0.303, Recall=0.423, PR-AUC=0.293**. Verify load lại từ file cho kết quả nhất quán 100% với lúc huấn luyện.

**Kết quả bàn giao**: model đã huấn luyện + đóng gói (`models/xgboost_final.pkl`, `models/final_model.json` — kèm ngưỡng quyết định và danh sách đặc trưng cho Giai đoạn 3 dùng), notebook chẩn đoán đầy đủ (21–26).

## 4. So sánh kế hoạch

| | Dự kiến | Thực tế |
|---|---|---|
| Mục tiêu F1 | ≥ 0.78 | **≥ 0.30** (đàm phán lại, đạt 0.353) |
| Căn cứ mục tiêu | Đặt trước, chưa có số liệu | 5 hướng thực nghiệm độc lập xác nhận trần thật ~0.31–0.35 |
| Kỹ thuật dự phòng dự kiến | SMOTE, điều chỉnh ngưỡng | Chỉ dùng `class_weight`/tinh ngưỡng — SMOTE không cần vì tinh ngưỡng đã đủ chứng minh giới hạn nằm ở tín hiệu, không phải kỹ thuật xử lý mất cân bằng |

**Nguyên nhân F1 thấp hơn kỳ vọng**: dữ liệu Olist ở mức đơn hàng chỉ chứa thông tin biết được tại thời điểm duyệt đơn (giá trị, vùng miền, thời điểm mua, phương thức thanh toán) — không có tín hiệu vận hành thực tế gây ra trễ giao hàng thật (tình trạng giao thông, tồn kho người bán theo ngày, hiệu suất đơn vị vận chuyển cụ thể, thời tiết). Đây là giới hạn của bản chất dữ liệu, không phải của kỹ thuật huấn luyện — đã được chứng minh bằng 3 loại model khác nhau, phân tích PR-AUC độc lập với ngưỡng, và 2 đòn bẩy bổ sung tín hiệu đều cho kết quả tương tự.

## 5. Bài học kinh nghiệm

**Về Machine Learning**:
- Tinh ngưỡng phân loại (threshold tuning) chỉ **di chuyển vị trí trên đường cong Precision-Recall đã có**, không **nâng** đường cong đó — PR-AUC mới là thước đo đúng để hỏi "model có thể tốt đến đâu", độc lập với lựa chọn ngưỡng.
- Feature importance cao không đồng nghĩa đặc trưng đó cải thiện kết quả: đặc trưng khoảng cách xếp hạng 3/76 ở Random Forest nhưng F1 gần như không đổi — vì thông tin phần lớn trùng lặp với `customer_state`/`primary_seller_state` đã có sẵn.
- Không nên suy đoán lạc quan về kết quả định lượng (F1, ceiling...) trước khi có số liệu thật — một sai lầm thực tế đã mắc phải và phải đính chính giữa dự án.

**Về quy trình Agile/Scrum**:
- Giữ kỷ luật Definition of Done (chạy thật notebook, không rò rỉ dữ liệu, ghi Retro khi đóng Sprint) giúp phát hiện sớm rằng mục tiêu F1≥0.78 bất khả thi, thay vì phát hiện muộn ở gần hạn nộp.
- Khi Sprint Goal gặp rủi ro rõ ràng (F1 xa mục tiêu), đóng Sprint đúng cam kết gốc và dời việc tinh chỉnh sang Sprint sau — tốt hơn mở rộng Goal giữa chừng để chạy theo một mục tiêu đã biết trước là bấp bênh.
- Hoàn thành sớm hơn kế hoạch tạo ra buffer thời gian thật — được tận dụng để dồn Story tiếp theo (API) lên sớm, không để trống.
