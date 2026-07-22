# Nghiệp vụ và quy trình nghiệp vụ

Tài liệu này tổng hợp phân tích nghiệp vụ (business process) của dự án Delivery Performance Intelligence, nghiên cứu bằng NotebookLM (nguồn: tài liệu tổng quan dự án + trang mô tả dataset Olist trên Kaggle + các bài phân tích/nghiên cứu công khai về logistics/e-commerce Brazil).

Mục tiêu: làm rõ ai làm gì, khi nào, dữ liệu nào ra vào — làm nền cho việc thiết kế API, giao diện và mô hình học máy.

## 1. Tổng quan nghiệp vụ

Ứng dụng phục vụ nghiệp vụ **giám sát và quản lý rủi ro giao hàng** trong hậu cần. Người dùng là **nhân viên vận hành** và **quản lý hậu cần**. Có 3 nghiệp vụ chính:

1. **Giám sát hiệu suất giao hàng** — theo dõi KPI để đánh giá chất lượng vận hành.
2. **Tra cứu và quản lý đơn hàng** — tìm kiếm, xem trạng thái đơn.
3. **Đánh giá rủi ro giao trễ** — dự đoán trước khi đơn được giao để can thiệp sớm (nghiệp vụ lõi).

Cả 3 quy trình vận hành trên nền vòng đời đơn hàng thực tế: khách đặt hàng → thanh toán được xác nhận → người bán chuẩn bị và đóng gói hàng → hàng được bàn giao cho đơn vị vận chuyển → đơn vị vận chuyển giao hàng đến khách → khách được mời đánh giá trải nghiệm. Một đơn được coi là **trễ** khi ngày giao hàng thực tế muộn hơn ngày giao hàng dự kiến đã cam kết với khách.

## 2. Quy trình 1: Giám sát hiệu suất (Performance Monitoring)

- **Tác nhân:** Quản lý hậu cần
- **Đầu vào:** Dữ liệu đơn hàng lịch sử, dữ liệu đánh giá của khách hàng
- **Đầu ra:** Báo cáo KPI, quyết định điều chỉnh vận hành

**Mô tả quy trình:** Quản lý đăng nhập và mở bảng điều khiển tổng quan → hệ thống truy vấn dữ liệu, tính toán và hiển thị bộ KPI gồm: tỷ lệ giao đúng hạn, số đơn trễ, **thời gian xử lý trung bình của người bán** (từ lúc đặt hàng đến lúc bàn giao cho đơn vị vận chuyển) và **thời gian vận chuyển trung bình** (từ lúc bàn giao đến lúc khách nhận hàng) tách riêng theo trách nhiệm, **tỷ lệ đánh giá thấp có liên quan đến giao trễ**, phân bố theo vùng, xu hướng theo thời gian → quản lý chọn bộ lọc (khoảng thời gian, khu vực) để phân tích sâu → hệ thống cập nhật biểu đồ theo bộ lọc → quản lý nhận diện vấn đề (ví dụ: vùng X có tỷ lệ trễ cao, hoặc thời gian xử lý của người bán kéo dài bất thường trong một giai đoạn) và ra quyết định điều chỉnh.

Việc tách riêng thời gian xử lý của người bán và thời gian vận chuyển giúp quản lý xác định chính xác điểm nghẽn nằm ở khâu chuẩn bị hàng hay khâu vận chuyển, thay vì chỉ nhìn một con số tổng thời gian gộp. Việc đưa thêm tỷ lệ đánh giá thấp liên quan đến trễ vào bộ KPI giúp gắn hiệu suất vận hành nội bộ với trải nghiệm thực tế của khách hàng.

| # | Hoạt động | Tài nguyên thực hiện | Đầu vào | Đầu ra |
|---|---|---|---|---|
| A1.1 | Mở bảng điều khiển | Quản lý hậu cần | — | Yêu cầu xem bảng điều khiển |
| A1.2 | Truy vấn & tính toán KPI | API phía máy chủ | Dữ liệu đơn hàng lịch sử, dữ liệu đánh giá khách hàng | Bộ chỉ số KPI |
| A1.3 | Hiển thị KPI & biểu đồ | Ứng dụng web | Bộ chỉ số KPI | Bảng điều khiển trực quan |
| A1.4 | Chọn bộ lọc phân tích | Quản lý hậu cần | Bảng điều khiển | Điều kiện lọc |
| A1.5 | Cập nhật biểu đồ theo bộ lọc | API + Ứng dụng web | Điều kiện lọc | Biểu đồ đã lọc |
| A1.6 | Phân tích & nhận diện vấn đề | Quản lý hậu cần | Biểu đồ đã lọc | Nhận định vấn đề |
| A1.7 | Ra quyết định điều chỉnh vận hành | Quản lý hậu cần | Nhận định vấn đề | Quyết định điều chỉnh |

**Sự kiện:** bắt đầu — quản lý cần đánh giá hiệu suất (theo nhu cầu hoặc định kỳ); trung gian — dữ liệu KPI được trả về từ API; kết thúc — quyết định vận hành được đưa ra.

**Đối tượng nghiệp vụ:** Báo cáo hiệu suất (được tạo → được phân tích → dẫn đến quyết định); Dữ liệu đơn hàng lịch sử và dữ liệu đánh giá khách hàng (kho dữ liệu); Bộ chỉ số KPI (tỷ lệ đúng hạn, số đơn trễ, thời gian xử lý của người bán, thời gian vận chuyển, tỷ lệ đánh giá thấp do trễ, phân bố vùng, xu hướng); Điều kiện lọc.

## 3. Quy trình 2: Quản lý đơn hàng (Order Management)

- **Tác nhân:** Nhân viên vận hành
- **Đầu vào:** Yêu cầu tra cứu (mã đơn, trạng thái, khoảng thời gian)
- **Đầu ra:** Thông tin chi tiết đơn hàng

**Mô tả quy trình:** Nhân viên mở trang quản lý đơn, nhập điều kiện tìm kiếm/lọc → hệ thống truy vấn và trả về danh sách đơn phù hợp → nhân viên chọn một đơn để xem chi tiết → hệ thống hiển thị thông tin sản phẩm, người bán, địa chỉ giao, ngày dự kiến/thực tế, trạng thái đúng hạn/trễ.

| # | Hoạt động | Tài nguyên thực hiện | Đầu vào | Đầu ra |
|---|---|---|---|---|
| A2.1 | Nhập điều kiện tìm kiếm/lọc | Nhân viên vận hành | Nhu cầu tra cứu | Điều kiện truy vấn |
| A2.2 | Truy vấn danh sách đơn | API phía máy chủ | Điều kiện truy vấn | Danh sách đơn phù hợp |
| A2.3 | Hiển thị danh sách kết quả | Ứng dụng web | Danh sách đơn | Bảng đơn hàng trên giao diện |
| A2.4 | Chọn đơn cần xem | Nhân viên vận hành | Bảng đơn hàng | Mã đơn được chọn |
| A2.5 | Truy vấn chi tiết đơn | API phía máy chủ | Mã đơn | Dữ liệu chi tiết đơn |
| A2.6 | Hiển thị chi tiết đơn | Ứng dụng web | Dữ liệu chi tiết | Trang chi tiết đơn |

**Sự kiện:** bắt đầu — phát sinh nhu cầu tra cứu đơn hàng; trung gian — kết quả truy vấn được trả về; kết thúc — nhân viên nhận được thông tin đơn cần tìm.

**Đối tượng nghiệp vụ:** Đơn hàng (được tra cứu → được xem chi tiết); Điều kiện tìm kiếm; Danh sách đơn; Chi tiết đơn (sản phẩm, người bán, địa chỉ, ngày dự kiến/thực tế, trạng thái).

## 4. Quy trình 3: Dự đoán rủi ro giao trễ (Risk Prediction)

- **Tác nhân:** Nhân viên vận hành
- **Đầu vào:** Thông tin đơn hàng mới (cân nặng, danh mục, hình thức thanh toán, cặp vùng người bán–người mua, thời điểm đặt hàng...)
- **Đầu ra:** Kết quả phân loại đúng hạn/trễ + xác suất + nhóm nguyên nhân rủi ro chính (chuẩn bị hàng chậm hay vận chuyển chậm)

**Mô tả quy trình:** Nhân viên nhập thông tin đơn mới vào biểu mẫu dự đoán, bao gồm cả **hình thức thanh toán** (thanh toán qua thẻ tín dụng có thể phải chờ ngân hàng xác nhận trước khi đơn được xử lý, nên cũng là một yếu tố rủi ro), **cặp vùng gửi–nhận cụ thể** (không chỉ khoảng cách đường chim bay — thực tế cho thấy tuyến từ Paraná đến Distrito Federal giao dưới 10 ngày, trong khi tuyến từ Minas Gerais đến Rio Grande do Sul hoặc đến Paraná có thể mất hơn 40 ngày, và các bang Roraima/Amapá có độ trễ trung bình cao nhất) và **thời điểm đặt hàng** (để nhận diện các mùa cao điểm như tháng 10–11, khi khối lượng đơn tăng đột biến và gây áp lực lên chuỗi cung ứng) → hệ thống kiểm tra tính hợp lệ dữ liệu đầu vào → giao diện gửi yêu cầu đến REST API → API tiền xử lý dữ liệu và xây dựng đặc trưng (bao gồm cặp vùng gửi–nhận, hình thức thanh toán, mùa vụ), đưa vào mô hình học máy → mô hình trả về kết quả đúng hạn/trễ kèm xác suất **và nhóm nguyên nhân rủi ro chính** (để phân biệt rủi ro nằm ở khâu người bán chuẩn bị hàng hay khâu vận chuyển, thay vì chỉ một nhãn "trễ" gộp chung) → hệ thống hiển thị kết quả → xử lý nghiệp vụ theo kết quả: rủi ro thấp → xử lý đơn bình thường; rủi ro cao → can thiệp **đúng theo nguyên nhân** (nhắc/ưu tiên người bán nếu rủi ro ở khâu chuẩn bị hàng, đổi đơn vị vận chuyển nếu rủi ro ở khâu giao hàng, hoặc chủ động thông báo khách hàng).

Việc phân tách nguyên nhân rủi ro (người bán hay vận chuyển) là cải tiến quan trọng so với việc chỉ dự đoán một nhãn "trễ" chung — nếu không phân tách, nhân viên vận hành có thể chọn sai biện pháp can thiệp (ví dụ đổi đơn vị vận chuyển trong khi lỗi thực chất nằm ở người bán chuẩn bị hàng chậm).

| # | Hoạt động | Tài nguyên thực hiện | Đầu vào | Đầu ra |
|---|---|---|---|---|
| A3.1 | Nhập thông tin đơn mới | Nhân viên vận hành | Thông tin đơn thực tế (cân nặng, danh mục, hình thức thanh toán, cặp vùng gửi–nhận, thời điểm đặt hàng) | Bộ tham số đầu vào |
| A3.2 | Kiểm tra tính hợp lệ dữ liệu | Ứng dụng web / API | Bộ tham số đầu vào | Dữ liệu hợp lệ (hoặc báo lỗi) |
| A3.3 | Gửi yêu cầu dự đoán | Ứng dụng web | Dữ liệu hợp lệ | Yêu cầu đến API |
| A3.4 | Tiền xử lý & xây dựng đặc trưng | API dự đoán học máy | Yêu cầu | Vec-tơ đặc trưng (gồm cặp vùng gửi–nhận, hình thức thanh toán, mùa vụ) |
| A3.5 | Chạy mô hình dự đoán | API dự đoán học máy | Vec-tơ đặc trưng | Nhãn + xác suất + nhóm nguyên nhân rủi ro chính |
| A3.6 | Hiển thị kết quả rủi ro | Ứng dụng web | Kết quả dự đoán | Kết quả trên giao diện |
| A3.7 | Đánh giá mức rủi ro | Nhân viên vận hành | Kết quả trên giao diện | Quyết định xử lý |
| A3.8a | Xử lý đơn bình thường | Nhân viên vận hành | Quyết định (rủi ro thấp) | Đơn vào luồng thường |
| A3.8b | Thực hiện biện pháp can thiệp đúng nguyên nhân | Nhân viên vận hành | Quyết định (rủi ro cao) kèm nhóm nguyên nhân | Đơn được ưu tiên xử lý / đổi vận chuyển / thông báo khách — chọn đúng biện pháp theo nguyên nhân |

Giữa A3.7 và A3.8a/A3.8b có **cổng rẽ nhánh loại trừ (exclusive gateway — XOR)** theo mức rủi ro.

**Sự kiện:** bắt đầu — đơn hàng mới cần đánh giá rủi ro; trung gian — nhận kết quả từ API học máy, hoặc dữ liệu không hợp lệ (quay lại nhập); kết thúc 1 — đơn được xử lý theo luồng bình thường; kết thúc 2 — đã thực hiện can thiệp rủi ro.

**Đối tượng nghiệp vụ:** Đơn hàng (mới → đã đánh giá rủi ro → đã xử lý thường/can thiệp); Bộ tham số đầu vào (cân nặng, danh mục, hình thức thanh toán, cặp vùng gửi–nhận, thời điểm đặt hàng); Vec-tơ đặc trưng; Kết quả dự đoán (nhãn đúng hạn/trễ + xác suất + nhóm nguyên nhân rủi ro); Mô hình học máy (tệp đã huấn luyện, được API nạp).

**Giá trị nghiệp vụ** nằm ở bước A3.7→A3.8: dự đoán chỉ có ý nghĩa khi dẫn đến hành động can thiệp sớm và đúng nguyên nhân, biến quy trình từ **phản ứng** (khách phàn nàn mới biết trễ) sang **chủ động** (biết trước rủi ro để xử lý).
