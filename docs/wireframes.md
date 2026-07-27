# Wireframe 3 màn hình chính

**Phân biệt quan trọng:** Dashboard KPI và Danh sách đơn hàng dùng **dữ liệu lịch sử đã hoàn tất** (được phép dùng `review_score`, `order_delivered_*_date` vì đơn đã xong) — khác với Biểu mẫu dự đoán chỉ được dùng đặc trưng hợp lệ tại thời điểm đơn mới (theo ràng buộc chống rò rỉ dữ liệu ở `docs/feature-list.md`).

---

## Màn hình 1 — Dashboard KPI (Quy trình 1: Giám sát hiệu suất, `business-processes.md` mục 2)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Delivery Performance Intelligence           [Bộ lọc: khoảng thời gian ▾] [vùng ▾] │
├──────────────────────────────────────────────────────────────────────┤
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐          │
│ │ Tỉ lệ trễ  │ │ Số đơn trễ │ │ TG xử lý   │ │ TG vận     │          │
│ │  8,11%     │ │  7.827     │ │ trung bình │ │ chuyển TB  │          │
│ │  (PA A)    │ │            │ │ (người bán)│ │            │          │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘          │
│ ┌────────────────────────────────┐                                   │
│ │ Tỉ lệ đánh giá thấp do trễ     │                                   │
│ └────────────────────────────────┘                                   │
├──────────────────────────────────────────────────────────────────────┤
│  Xu hướng tỉ lệ trễ theo tháng (line chart)                           │
│  ▁▂▂▃▇▇█▃▂▁▂▃  ← đỉnh 2017-11, 2018-02, 2018-03 (Story #6)            │
├──────────────────────────────────────────────────────────────────────┤
│  Tỉ lệ trễ theo bang (bar/heatmap, top rủi ro cao nhất)               │
│  AL ██████████ 23,93%   AL, MA, SE... (Story #6)                     │
│  SP ███ 5,89%                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

**Thành phần chính:**
- Bộ lọc dùng chung cho toàn trang: khoảng thời gian, vùng (bang) — tương ứng hoạt động A1.4/A1.5 trong `business-processes.md`.
- 5 thẻ KPI: tỉ lệ giao đúng hạn/trễ (Phương án A), số đơn trễ tuyệt đối, **thời gian xử lý trung bình của người bán** (`order_purchase_timestamp` → `order_delivered_carrier_date`, tách riêng khỏi vận chuyển — nghiệp vụ yêu cầu tách rõ điểm nghẽn), **thời gian vận chuyển trung bình** (`order_delivered_carrier_date` → `order_delivered_customer_date`), tỉ lệ đánh giá thấp (`review_score` ≤ 2) liên quan đến đơn trễ.
- Biểu đồ đường: xu hướng tỉ lệ trễ theo tháng — tái dùng kết quả `notebooks/12_delay_trend_over_time.ipynb`.
- Biểu đồ theo vùng: tỉ lệ trễ theo `customer_state`, ghi chú cỡ mẫu — tái dùng `notebooks/13_delay_by_region_and_payment.ipynb`.

**Nguồn dữ liệu:** lịch sử đơn đã có kết quả giao hàng — được phép dùng toàn bộ 42 cột `orders_labeled.csv` (không bị ràng buộc chống rò rỉ như biểu mẫu dự đoán).

---

## Màn hình 2 — Danh sách đơn hàng (Quy trình 2: Quản lý đơn hàng, `business-processes.md` mục 3)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Danh sách đơn hàng                                                  │
│  [Tìm mã đơn...] [Trạng thái: Tất cả ▾] [Vùng ▾] [Khoảng ngày ▾] [Tìm]│
├──────────────────────────────────────────────────────────────────────┤
│ Mã đơn      │ Ngày mua   │ Vùng    │ Dự kiến giao │ Trạng thái       │
│ e481f51...  │ 2018-01-05 │ SP      │ 2018-01-18   │ ✅ Đúng hạn       │
│ 53cdb2f...  │ 2018-02-11 │ AL      │ 2018-02-25   │ 🔴 Trễ            │
│ 47770eb...  │ 2018-03-02 │ RJ      │ 2018-03-15   │ ⏳ Chưa xác định  │
│ ...         │            │         │              │  [xem chi tiết →]│
├──────────────────────────────────────────────────────────────────────┤
│  ◂ Trang 1 / 1971  ▸                                                  │
└──────────────────────────────────────────────────────────────────────┘

  Chi tiết đơn (mở rộng khi bấm 1 dòng):
  ┌──────────────────────────────────────────────┐
  │ Sản phẩm: ... | Người bán: ... (bang XX)      │
  │ Địa chỉ giao: ... (bang YY)                   │
  │ Ngày dự kiến: ... | Ngày giao thực tế: ...    │
  │ Trạng thái: Trễ / Đúng hạn / Chưa xác định    │
  └──────────────────────────────────────────────┘
```

**Thành phần chính:**
- Thanh tìm kiếm/lọc: theo mã đơn, trạng thái (đúng hạn/trễ/chưa xác định — phản ánh 3 trạng thái `is_delayed`), vùng, khoảng thời gian — đáp ứng AC Story #12 "ít nhất 1 chức năng lọc/tìm kiếm".
- Bảng danh sách: phân trang, cột trạng thái dùng badge màu (không chỉ nhị phân — phải thể hiện được nhóm "chưa xác định" NA, tránh nhầm là lỗi dữ liệu).
- Panel chi tiết đơn (mở rộng dòng hoặc trang riêng) — theo đúng luồng A2.4-A2.6 trong `business-processes.md`: sản phẩm, người bán, địa chỉ giao, ngày dự kiến/thực tế, trạng thái.

---

## Màn hình 3 — Biểu mẫu dự đoán rủi ro (Quy trình 3: Dự đoán rủi ro, `business-processes.md` mục 4)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Dự đoán rủi ro giao trễ — Đơn hàng mới                              │
├──────────────────────────────────────────────────────────────────────┤
│  Vùng người mua (bang):      [SP ▾]                                  │
│  Vùng người bán (bang):      [MG ▾]                                  │
│  Số lượng sản phẩm:          [__]      Tổng khối lượng (g): [____]   │
│  Tổng giá trị đơn (R$):      [______]  Phí vận chuyển (R$): [____]   │
│  Số category sản phẩm:       [__]                                    │
│  Hình thức thanh toán:       [ ] Thẻ tín dụng  [ ] Boleto  [ ] Voucher [ ] Thẻ ghi nợ │
│  Số kỳ trả góp tối đa:       [__]                                     │
│  Ngày đặt hàng:              [____-__-__]                             │
│  Ngày duyệt thanh toán:      [____-__-__]  (đã duyệt — dùng để tính approval_gap_hours) │
│  Ngày giao dự kiến (cam kết):[____-__-__]                             │
│  Nhiều người bán trong đơn:  [ ] Có                                   │
│                                                                        │
│                         [ Dự đoán rủi ro ]                            │
├──────────────────────────────────────────────────────────────────────┤
│  Kết quả:                                                             │
│  ┌────────────────────────────────────────┐                          │
│  │  ⚠ Rủi ro CAO — xác suất trễ: 68%      │                          │
│  │                                          │                          │
│  │  Nhóm nguyên nhân chính:                │                          │
│  │   🔵 Vận chuyển (60%)  🟢 Chuẩn bị & thanh toán (25%)  │            │
│  │   🟡 Yếu tố thời điểm (15%)              │                          │
│  │                                          │                          │
│  │  → Gợi ý: cân nhắc đổi đơn vị vận chuyển │                          │
│  └────────────────────────────────────────┘                          │
└──────────────────────────────────────────────────────────────────────┘
```

**Thành phần chính:**
- Form input — **mỗi trường tương ứng trực tiếp 1 đặc trưng đã chốt ở `docs/feature-list.md`**, không thêm trường nào ngoài danh sách đó để tránh vượt phạm vi đã rà soát rò rỉ dữ liệu:
  - `customer_state`, `primary_seller_state` (dropdown 27/22 bang)
  - `items_num_items`, `items_num_products`, `items_num_sellers`, `items_num_categories`, `items_total_price`, `items_total_freight`, `items_total_weight_g`
  - `payment_has_*` (checkbox nhiều lựa chọn), `payment_total_value`, `payment_num_rows`, `payment_num_types`, `payment_max_installments`
  - `items_multi_seller` (checkbox)
  - Ngày đặt hàng + ngày duyệt thanh toán → hệ thống tự tính `approval_gap_hours`, `order_purchase_month`
  - Ngày giao dự kiến → hệ thống tự tính `estimated_delivery_days`
- Nút "Dự đoán rủi ro" → gọi `POST /predict` (Story #11), hiển thị trạng thái loading (AC Story #13 yêu cầu phản hồi "trong vài giây").
- Panel kết quả: xác suất trễ (%), phân loại rủi ro (Thấp/Trung bình/Cao — ngưỡng cụ thể chốt ở Story #9/#10), **và bắt buộc có nhóm nguyên nhân rủi ro chính** (🔵 Vận chuyển / 🟢 Chuẩn bị & thanh toán / 🟡 Yếu tố thời điểm) — đây là giá trị nghiệp vụ cốt lõi được nhấn mạnh ở `business-processes.md` mục 4 ("phân tách nguyên nhân rủi ro là cải tiến quan trọng"), quyết định biện pháp can thiệp nào (A3.8b).

**Cơ chế tính "nhóm nguyên nhân rủi ro chính" (đã chốt qua spike thử nghiệm, xem `notebooks/27_risk_group_shap_spike.ipynb`)**: SHAP values tính riêng cho từng đơn (`TreeExplainer` trên XGBoost), gộp `|SHAP|` theo 3 nhóm — 🔵 Vận chuyển (`seller_customer_distance_km`, `estimated_delivery_days`, state đang áp dụng cho đơn), 🟢 Chuẩn bị & thanh toán (đổi tên từ "Chuẩn bị hàng" vì nhóm này gồm cả `payment_*`, chiếm ~30% trọng số nhóm, không chỉ độ phức tạp đơn), 🟡 Yếu tố thời điểm (`order_purchase_month` riêng — ban đầu định loại hẳn vì là confound mùa vụ đã xác nhận, không phải nguyên nhân hành động được, nhưng dữ liệu thật cho thấy nó là driver mạnh nhất ở 60% đơn dự đoán trễ nên tách thành nhóm thứ 3 công khai thay vì ẩn đi). 3 nhóm luôn cộng đủ 100%, tỷ lệ % biến thiên thật theo từng đơn (đã kiểm chứng trên tập test, không degenerate).
