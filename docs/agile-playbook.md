# Cẩm nang: Cách tổ chức & tư duy Agile cho dự án cá nhân

Tài liệu này lưu lại phần thảo luận về phương pháp làm việc, để đọc lại khi cần nhắc lại cách tư duy phân rã công việc.

## 1. Mô hình Agile rút gọn kiểu Kanban-in-Sprint

Dự án do **1 thành viên** thực hiện, nên không cần đủ vai trò Scrum (Product Owner / Scrum Master / Dev Team) và không cần các nghi thức dành cho nhóm (daily standup meeting, sprint planning poker...).

Vẫn giữ lại phần cốt lõi giúp Agile hiệu quả:

- **Nhịp sprint cố định (1 tuần)** — ép tiến độ, phát hiện rủi ro sớm thay vì dồn việc đến gần deadline.
- **Sprint Goal rõ ràng** — mỗi tuần có một mục tiêu có thể tự kiểm chứng, thay vì mốc giai đoạn mơ hồ kéo dài 3-4 tuần.
- **Sprint Review/Retro rút gọn** — cuối mỗi tuần tự ghi 2-3 dòng: đạt goal chưa, cần điều chỉnh gì cho tuần sau (ghi trực tiếp trong Issue đóng milestone, không cần họp hay tập tin riêng).

## 2. Ba cấp độ phân rã công việc

```
Epic (mục tiêu lớn, kéo dài nhiều sprint)
 └── User Story (một lát cắt giá trị, hoàn thành trong một sprint)
      └── Task (việc kỹ thuật cụ thể để hoàn thành story, vài giờ)
```

- **Epic** — quá lớn để làm trong một sprint, không tự kiểm chứng được ngay. VD: "Xây dựng mô hình học máy".
- **User Story** — một đơn vị giá trị nhỏ, có thể trình diễn/kiểm chứng độc lập. Viết theo mẫu:
  > *Là [vai trò], tôi muốn [làm được gì], để [đạt giá trị gì].*
- **Task** — bước kỹ thuật để hoàn thành một story, không cần viết theo mẫu vai trò.

## 3. Nguyên tắc INVEST — kiểm tra một story có tốt không?

| Chữ cái | Ý nghĩa | Câu hỏi tự kiểm tra |
|---|---|---|
| I | Independent | Story có phụ thuộc cứng vào story khác không? |
| N | Negotiable | Story có đang mô tả "làm gì" hay đã lỡ chốt cứng "làm bằng cách nào" không? |
| V | Valuable | Story có mang lại giá trị rõ ràng (kể cả để chính mình kiểm chứng) không? |
| E | Estimable | Có ước lượng được công sức cần bỏ ra không? |
| S | Small | Có làm xong trong một sprint (1 tuần) không? |
| T | Testable | Có tiêu chí chấp nhận (Acceptance Criteria) rõ ràng để biết khi nào xong không? |

## 4. Ví dụ áp dụng: phân rã Sprint 1

Sprint 1 goal: *"Tải & khám phá cấu trúc dữ liệu Olist"* — đây là mức Epic nếu để nguyên. Phân rã thành story theo INVEST:

**Story 1.1** — *Là người phát triển, tôi muốn tải và giải nén bộ dữ liệu Olist về máy, để có dữ liệu thô sẵn sàng phân tích.*
- Tiêu chí chấp nhận: 9 file CSV của Olist tồn tại trong `data/raw/`, đọc được bằng pandas không lỗi encoding.

**Story 1.2** — *Là người phát triển, tôi muốn hiểu schema và mối quan hệ giữa các bảng, để biết cách join dữ liệu ở sprint sau.*
- Tiêu chí chấp nhận: có ghi chú quan hệ khóa chính-khóa ngoại giữa 9 bảng (orders, order_items, products, sellers, customers, geolocation...).

**Story 1.3** — *Là người phát triển, tôi muốn kiểm tra chất lượng dữ liệu thô (null, trùng lặp, kiểu dữ liệu sai), để tránh lỗi ở bước phân tích sâu.*
- Tiêu chí chấp nhận: notebook liệt kê % giá trị thiếu theo từng cột của các bảng chính.

→ 3 story nhỏ, mỗi cái làm 1-2 ngày, tổng vừa 1 sprint.

## 5. Ánh xạ khái niệm Agile sang GitHub Project

| Khái niệm Agile | GitHub |
|---|---|
| Epic | **Label** (`epic:data`, `epic:ml`, `epic:dashboard`, `epic:qa`) |
| Sprint | Trường **Iteration** trong GitHub Project (template "Iterative development") — 1 vòng lặp = 1 tuần, tự sinh sprint kế tiếp, có ngày bắt đầu/kết thúc rõ ràng |
| User Story | **Issue** (title dạng "Là... tôi muốn... để...", gán Label + thêm vào Project, có checklist Acceptance Criteria) |
| Trạng thái công việc | Trường **Status** trong Project, xem qua view board lọc theo iteration hiện tại (`Backlog → To Do → In Progress → Done`) |

## 6. Định nghĩa hoàn thành (Definition of Done)

Một Issue/Sprint được coi là hoàn thành khi:

- [ ] Code/chức năng chạy được, không lỗi khi thực thi thử
- [ ] Không có rò rỉ dữ liệu (data leakage) đối với các task liên quan đến mô hình học máy
- [ ] Đã commit/tạo Pull Request tương ứng
- [ ] Tự đánh giá lại Sprint Goal (đạt/chưa đạt) và ghi chú điều chỉnh cho sprint sau ngay trong Issue đóng milestone
