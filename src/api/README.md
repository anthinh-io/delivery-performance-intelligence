# Giao diện lập trình ứng dụng (API)

Giao diện lập trình ứng dụng (API) dạng REST dự đoán rủi ro giao trễ đơn hàng, phục vụ tích hợp cho ứng dụng web và các dịch vụ bên ngoài.

## Tổng quan

Giao diện lập trình ứng dụng dự đoán bằng học máy đảm nhiệm việc cung cấp dự đoán rủi ro giao trễ, tách biệt khỏi phần xử lý dữ liệu và huấn luyện mô hình.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| Test | pytest, httpx |
| Package manager | `uv` (workspace member) |

## Cấu trúc thư mục

```
src/api/
├── pyproject.toml                 # cấu hình gói thư viện
├── postman_collection.json        # bộ sưu tập request để test thủ công
├── app/
│   ├── __init__.py
│   ├── main.py                    # khởi tạo ứng dụng, định nghĩa route
│   ├── schemas.py                 # định nghĩa schema dữ liệu vào/ra
│   ├── preprocessing.py           # xử lý dữ liệu đầu vào
│   ├── model.py                   # dự đoán bằng model
│   └── db.py                      # nạp dữ liệu đơn hàng lịch sử vào SQLite
├── data/
│   └── orders.sqlite3             # (gitignored) build lại bằng `python -m app.db`
└── tests/
    ├── __init__.py
    ├── test_health.py             # test route health
    ├── test_schemas.py            # test schema dữ liệu
    ├── test_preprocessing.py      # test xử lý dữ liệu đầu vào
    ├── test_model.py              # test dự đoán
    ├── test_predict_endpoint.py   # test route predict
    ├── test_db.py                 # test nạp dữ liệu vào SQLite
    └── fixtures/
        ├── golden_order.json      # dữ liệu mẫu dùng cho test
        └── orders_sample.csv      # CSV mẫu dùng cho test nạp SQLite
```

## Cài đặt

Gói thư viện được quản lý qua `uv` workspace, dùng chung một lockfile duy nhất, đảm bảo phụ thuộc luôn nhất quán trong toàn bộ dự án.

Chạy lệnh sau ở thư mục gốc để đồng bộ:

```bash
uv sync
```

Chạy ứng dụng:

```bash
uv run --project src/api uvicorn app.main:app --app-dir src/api --reload
```

- Server: `http://127.0.0.1:8000`
- Swagger UI (docs tương tác): `http://127.0.0.1:8000/docs`

Kiểm tra bằng curl:

```bash
curl http://127.0.0.1:8000/health
```

Kỳ vọng: `{"status":"ok"}`, mã 200.

Chạy test:

```bash
uv run --project src/api pytest src/api
```

Build (hoặc build lại) cơ sở dữ liệu SQLite dùng cho trang danh sách/chi tiết đơn hàng, từ `data/processed/orders_labeled.csv`:

```bash
cd src/api
uv run python -m app.db
```

Kết quả: `src/api/data/orders.sqlite3` (gitignored, ~38MB — tái tạo lại được từ CSV đã có trong git, không cần commit).

Kiểm tra thủ công `POST /predict` bằng Postman: xem `postman_collection.json` (import vào Postman/Postman VSCode extension, có sẵn test script tự động).

## API Reference

| Method | Path | Mô tả | Response |
|---|---|---|---|
| GET | `/health` | Health check | `{"status": "ok"}` |
| POST | `/predict` | Dự đoán rủi ro giao trễ + nhóm nguyên nhân | `{"is_delayed": bool, "probability": float, "risk_groups": [{"name": str, "contribution_pct": float}]}` |
