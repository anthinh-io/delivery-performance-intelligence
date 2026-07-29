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

| Sprint | Thời gian | Mục tiêu | Giá trị mang lại |
|---|---|---|---|
| 1 | 16/7 – 22/7 | Tải & khám phá cấu trúc dữ liệu Olist, join các bảng, tính nhãn trễ, phân tích mất cân bằng & xu hướng | Có bằng chứng định lượng về đặc điểm bài toán, làm căn cứ chọn đúng kỹ thuật xử lý mất cân bằng dữ liệu |
| 2 | 23/7 – 29/7 | Chốt phạm vi (wireframe + đặc trưng) → xây dựng bộ đặc trưng và xử lý mất cân bằng dữ liệu → huấn luyện & so sánh 3 mô hình baseline trên tập thử nghiệm | Chốt phạm vi trước khi code; có bộ dữ liệu sẵn sàng huấn luyện; biết mô hình nào khả thi nhất sớm hơn kế hoạch gốc — phát hiện F1 trần thực tế (~0.35, PR-AUC ~0.28) cách xa mục tiêu 0.78 cam kết ban đầu, dẫn tới quyết định dời phần tinh chỉnh mô hình |
| 3 | 30/7 – 5/8 | Xây dựng giao diện lập trình ứng dụng (API) dạng REST → mở rộng dữ liệu lịch sử qua SQLite, xây dựng trang quản lý danh sách đơn hàng: tìm kiếm/lọc theo mã đơn/trạng thái/khoảng ngày, phân trang, xem chi tiết một đơn hàng | Mô hình trở thành dịch vụ gọi được qua HTTP; người vận hành tra cứu được đơn hàng thật qua giao diện web |
| 4 | 6/8 – 12/8 | Xây dựng Dashboard KPI tổng quan theo đúng wireframe đã chốt (5 KPI cốt lõi + 2 biểu đồ xu hướng/khu vực), kèm bộ lọc thời gian/khu vực | Người quản lý xem được hiệu suất giao hàng trực quan, thay thế theo dõi thủ công |
| 5 | 13/8 – 19/8 | Biểu mẫu dự đoán tích hợp API + kiểm thử toàn trình (end-to-end) | Hoàn thành nghiệp vụ lõi: dự đoán rủi ro thời gian thực — biến quy trình từ phản ứng sang chủ động |
| 6 | 20/8 – 26/8 | Sửa lỗi, tối ưu trải nghiệm người dùng (UX), báo cáo cuối kỳ, trình diễn | Đảm bảo đủ tin cậy để bàn giao |
| 7 | 27/8 – 2/9 | *(Buffer dự phòng — không cam kết trước)* | — |
| 8 | 3/9 – 9/9 | *(Buffer dự phòng — không cam kết trước)* | — |
| 9 | 10/9 – 16/9 | *(Buffer dự phòng — không cam kết trước)* | — |
| 10 | 17/9 – 23/9 | *(Buffer dự phòng — không cam kết trước)* | — |
