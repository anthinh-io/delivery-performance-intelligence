# Model artifacts

File `.pkl` trong thư mục này **không commit vào git** (xem `.gitignore`) — model 153MB (Random Forest) vượt giới
hạn 100MB/file của GitHub, và cả 3 model đều tái tạo lại được 100% từ dữ liệu + code đã có sẵn trong repo (cùng
`random_state=42`, cùng phiên bản thư viện pin qua `uv.lock`).

## Tái tạo lại model

Chạy notebook huấn luyện, model sẽ được lưu lại vào thư mục này:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/20_train_baseline_models.ipynb
```

Sinh ra:
- `logistic_regression.pkl`, `random_forest.pkl`, `xgboost.pkl` — model đã huấn luyện trên `orders_features_train.csv`
- `training_times.json` — có commit vào git (thời gian huấn luyện mỗi model, dùng cho bảng so sánh Task #50)
