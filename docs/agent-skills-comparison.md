# Cẩm nang: So sánh `addyosmani/agent-skills` và `obra/superpowers` skills cho AI agent

## 1. Ý tưởng cốt lõi

Hai framework tối ưu cho **hai thời điểm khác nhau** trong vòng đời phát triển phần mềm:

- **agent-skills** tổ chức theo **giai đoạn** (Define → Plan → Build → Verify → Review → Ship), có checkpoint con người ở mỗi giai đoạn, và một khung eval trong CI để đảm bảo skill hoạt động đúng như mô tả.
- **superpowers** tối ưu cho các phiên làm việc **tự động, nặng suy luận**: một pipeline tuyến tính (brainstorm → plan → subagent thực thi → review), dùng git-worktree để cô lập các task chạy song song.

Không có framework nào "tốt hơn tuyệt đối" — chúng phù hợp với hai kiểu công việc khác nhau, và có thể kết hợp có chọn lọc.

| | agent-skills | superpowers |
|---|---|---|
| Ý tưởng nền tảng | Mã hóa toàn bộ vòng đời của một kỹ sư senior (từ định nghĩa yêu cầu đến triển khai) thành các skill, có một meta-skill đóng vai trò router chọn skill phù hợp | Một phương pháp phát triển hoàn chỉnh xây trên các skill kết hợp được với nhau, vận hành như một vòng lặp kỷ luật duy nhất |
| Cơ chế đặc trưng | Bảng "Common Rationalizations" (liệt kê lý do agent hay viện cớ để bỏ bước, kèm phản biện) + "Red Flags" trong mọi skill; nhiều persona review chạy song song ở bước ship | Subagent-driven development: một subagent mới thực thi từng task, một task-reviewer chấm cả spec lẫn chất lượng code, có vòng lặp tự sửa nếu bị đánh rớt |
| Cách đo chất lượng | Khung eval 3 tầng chạy trong CI (kiểm tra cấu trúc skill, kiểm tra mô tả/routing không xung đột, chấm điểm hành vi thực thi) | Coi trọng "pressure-testing" (thử nghiệm áp lực) như triết lý cốt lõi, nhưng bộ eval hiện đã tách sang một repo riêng, không còn nằm trong repo chính |

## 2. Nguyên tắc tổ chức

- **agent-skills**: tổ chức theo **các giai đoạn của SDLC**. Mỗi giai đoạn có một slash command tương ứng 1:1 (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`), cộng thêm chế độ `/build auto` để chạy trọn một plan đã duyệt trong một lượt. Người dùng có thể bỏ qua các giai đoạn đầu nếu việc đã rõ ràng, đi thẳng vào `/build` → `/test` → `/review`.
- **superpowers**: tổ chức theo **một chuỗi skill nối tiếp, có thứ tự cố định** — `brainstorming` → `writing-plans` → `subagent-driven-development`. Đây không phải một router chọn skill theo tình huống, mà là một quy trình bạn đi qua tuần tự cho mọi việc, dù lớn hay nhỏ.

Sự khác biệt nguyên tắc quan trọng nhất: agent-skills **định tuyến** (routing) — chọn đúng skill cho đúng việc; superpowers **tuần tự hóa** (sequencing) — luôn đi qua cùng một chuỗi bước.

## 3. So sánh chi tiết: Strengths và Weaknesses

### agent-skills

**Strengths:**
- Độ phủ rộng nhất trong ba framework: không chỉ code mà còn bảo mật, hiệu năng, CI/CD, observability, launch.
- Có eval ngay trong repo, chạy trong CI — phát hiện sớm nếu một skill bị hỏng cách kích hoạt/route.
- Có "gear nhẹ" cho việc nhỏ (bỏ qua các giai đoạn đầu khi không cần).
- Persona review song song (code, security, performance, test) trước khi ship.

**Weaknesses:**
- Không có một "đường chạy" tự động, kỷ luật cao — nghĩa là ít phù hợp khi muốn giao việc lớn rồi để agent tự chạy dài hơi không cần can thiệp.
- Vòng làm rõ yêu cầu (`/spec`) không sâu bằng cơ chế thẩm vấn chuyên biệt của các framework khác.

### superpowers

**Strengths:**
- Đầu tư mạnh vào suy luận kiến trúc hoặc làm rõ vấn đề trước khi code (brainstorm kiểu Socratic).
- Subagent-driven execution + task reviewer tự động: giao việc lớn, mơ hồ, nhận lại kết quả đã được chấm điểm.
- Cô lập bằng git-worktree khi nhiều task chạy song song.
- Guardrail mạnh chống việc agent "lách" quy trình.

**Weaknesses:**
- Phạm vi hẹp — chỉ là methodology cho vòng lặp build nội bộ, không bao quát bảo mật/hiệu năng/launch.
- Pipeline một chuỗi cố định có thể nặng nề, không cần thiết với thay đổi nhỏ.
- Không có eval trong repo chính để tự kiểm tra skill.
- Backlog đóng góp cộng đồng còn tồn đọng; chưa có tính năng multi-agent team execution mà cộng đồng hay yêu cầu.
