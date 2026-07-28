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
├── pyproject.toml
├── app/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_health.py
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

## API Reference

| Method | Path | Mô tả | Response |
|---|---|---|---|
| GET | `/health` | Health check | `{"status": "ok"}` |
