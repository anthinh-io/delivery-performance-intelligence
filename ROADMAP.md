# Lộ trình dự án (Agile)

Dự án được thực hiện theo mô hình Agile, phù hợp quy mô cá nhân: giữ nhịp sprint hàng tuần để ép tiến độ và phát hiện rủi ro sớm, nhưng bỏ các nghi thức cần nhiều người (daily standup meeting, sprint planning poker...).

## Cấu trúc công việc

```
Epic (mục tiêu lớn, kéo dài nhiều sprint)
 └── User Story (một lát cắt giá trị, hoàn thành trong một sprint)
      └── Task (việc kỹ thuật cụ thể để hoàn thành story)
```

Việc theo dõi chi tiết (User Story, Task) được quản lý bằng **GitHub Issues** và **GitHub Projects**, không lặp lại trong tập tin này:

- **Epic** → gắn bằng Label (`epic:data`, `epic:ml`, `epic:dashboard`, `epic:qa`)
- **Sprint** → trường **Iteration** trong GitHub Project (template "Iterative development"), mỗi vòng lặp dài 1 tuần, tự động sinh sprint kế tiếp
- **User Story** → 1 Issue, đặt tên theo mẫu *"Là..., tôi muốn..., để..."*, có tiêu chí chấp nhận (Acceptance Criteria) dạng checklist, được thêm vào Project
- **Trạng thái công việc** → trường **Status** trong Project, xem qua view board lọc theo iteration hiện tại

Xem chi tiết tại [GitHub Issues](https://github.com/anthinh-io/delivery-performance-intelligence/issues) và [GitHub Projects](https://github.com/anthinh-io/delivery-performance-intelligence/projects).

## Định nghĩa hoàn thành (Definition of Done)

Một Issue/Sprint được coi là hoàn thành khi:

- [ ] Code/chức năng chạy được, không lỗi khi thực thi thử
- [ ] Không có rò rỉ dữ liệu (data leakage) đối với các task liên quan đến mô hình học máy
- [ ] Đã commit/tạo Pull Request tương ứng
- [ ] Tự đánh giá lại Sprint Goal (đạt/chưa đạt) và ghi chú điều chỉnh cho sprint sau ngay trong Issue khi kết thúc iteration

## Bảng phân rã công việc theo Sprint

| Sprint | Thời gian | Mục tiêu | Giá trị mang lại | Epic |
|---|---|---|---|---|
| 1 | 16/7 – 22/7 | Tải & khám phá cấu trúc dữ liệu Olist | Xác nhận dữ liệu đủ chất lượng và có cấu trúc dùng được, trước khi đầu tư công sức phân tích sâu | Phân tích & khám phá dữ liệu |
| 2 | 23/7 – 29/7 | Phân tích khám phá dữ liệu (EDA): kết nối các bảng, tính nhãn trễ, phân tích mất cân bằng & xu hướng | Có bằng chứng định lượng về đặc điểm bài toán, làm căn cứ chọn đúng kỹ thuật xử lý mất cân bằng ở Sprint 4 | Phân tích & khám phá dữ liệu |
| 3 | 30/7 – 5/8 | Bản phác thảo giao diện (wireframe) 3 màn hình + chốt danh sách đặc trưng | Chốt phạm vi trước khi code, tránh làm lại giao diện; danh sách đặc trưng là input rõ ràng cho Epic 2 | Phân tích & khám phá dữ liệu |
| 4 | 6/8 – 12/8 | Xây dựng đặc trưng (feature engineering) + xử lý mất cân bằng dữ liệu | Có bộ dữ liệu sẵn sàng huấn luyện — điều kiện tiên quyết để bắt đầu huấn luyện mô hình thật | Xây dựng mô hình học máy |
| 5 | 13/8 – 19/8 | Huấn luyện & so sánh mô hình (Hồi quy Logistic → Rừng ngẫu nhiên → XGBoost) | Biết mô hình nào khả thi nhất với con số F1 cụ thể, phát hiện sớm nếu cần đổi hướng | Xây dựng mô hình học máy |
| 6 | 20/8 – 26/8 | Tinh chỉnh đạt F1 ≥ 0.78, đóng gói mô hình | Xác nhận đạt ngưỡng chất lượng đã cam kết — rủi ro kỹ thuật lớn nhất được giải quyết sớm | Xây dựng mô hình học máy |
| 7 | 27/8 – 2/9 | Xây dựng giao diện lập trình ứng dụng (API) dạng REST | Mô hình trở thành dịch vụ gọi được qua HTTP — mở khóa việc tích hợp cho Epic 3 | Xây dựng mô hình học máy |
| 8 | 3/9 – 9/9 | Bảng điều khiển KPI + trang quản lý đơn hàng | Người dùng lần đầu nhìn thấy hiệu suất giao hàng trực quan, thay thế theo dõi thủ công | Xây ứng dụng web |
| 9 | 10/9 – 16/9 | Biểu mẫu dự đoán tích hợp API + kiểm thử toàn trình (end-to-end) | Hoàn thành nghiệp vụ lõi: dự đoán rủi ro thời gian thực — biến quy trình từ phản ứng sang chủ động | Xây ứng dụng web / Kiểm thử & hoàn thiện |
| 10 | 17/9 – 23/9 | Sửa lỗi, tối ưu trải nghiệm người dùng (UX), báo cáo cuối kỳ, trình diễn | Đảm bảo đủ tin cậy để bàn giao | Kiểm thử & hoàn thiện |
