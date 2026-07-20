# Delivery Performance Intelligence

**Ứng dụng web quản lý và dự đoán hiệu suất giao hàng bằng học máy**

Dự án môn học IE207 — giải quyết bài toán thiếu công cụ dữ liệu có hệ thống để giám sát hiệu suất giao hàng và dự đoán rủi ro giao trễ trong lĩnh vực hậu cần và quản lý chuỗi cung ứng.

## 1. Tổng quan

Hệ thống gồm hai thành phần song song, kết nối qua giao diện lập trình ứng dụng (API) dạng REST:

- **Bảng điều khiển vận hành trên nền web** — theo dõi chỉ số hiệu suất chính (KPI), quản lý đơn hàng, trực quan hóa xu hướng giao hàng.
- **Giao diện lập trình ứng dụng dự đoán bằng học máy** — phân loại rủi ro giao hàng (đúng hạn / trễ) bằng mô hình huấn luyện trên bộ dữ liệu [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (~100.000 đơn hàng).

Người dùng nhập thông tin đơn hàng và nhận dự đoán rủi ro giao trễ theo thời gian thực ngay trên giao diện.

## 2. Công nghệ sử dụng

| Tầng | Công nghệ |
|---|---|
| Giao diện người dùng | React / Next.js |
| Hệ thống phía máy chủ | FastAPI |
| Mô hình học máy | Scikit-learn, XGBoost |
| Xử lý dữ liệu | Pandas, NumPy |
| Trực quan hóa dữ liệu | Recharts / Chart.js |
| Bộ dữ liệu | Olist Brazilian E-Commerce (Kaggle) |

## 3. Kết quả kỳ vọng

- Ứng dụng web hoạt động hoàn chỉnh, thay thế quy trình quản lý hậu cần thủ công.
- Mô hình học máy đạt điểm F1 ≥ 0.78 trên bài toán phân loại giao trễ.
- Giao diện lập trình ứng dụng cho phép dự đoán thời gian thực từ giao diện web.
- Nền tảng mở rộng trong tương lai: tối ưu tuyến đường, trợ lý trí tuệ nhân tạo, hệ thống quản lý chuỗi cung ứng đầy đủ.

## 4. Lộ trình

- [ ] **Giai đoạn 1** — Phân tích & khám phá dữ liệu
- [ ] **Giai đoạn 2** — Xây dựng mô hình học máy
- [ ] **Giai đoạn 3** — Xây ứng dụng web
- [ ] **Giai đoạn 4** — Kiểm thử & hoàn thiện

## 5. Giấy phép

Dự án được thực hiện cho mục đích giáo dục, phục vụ môn học IE207. Không sử dụng cho mục đích thương mại.
