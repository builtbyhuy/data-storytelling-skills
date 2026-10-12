# Pilot 10 ngày làm việc: chọn một cải tiến xử lý hoàn tiền

**Câu hỏi:** hồ sơ hoàn tiền đang mở bị kẹt ở bước nào, và một thay đổi nhỏ nào giúp xử lý chúng rõ ràng hơn? Chỉ lập kế hoạch; chưa có dữ liệu hồ sơ, chưa bắt đầu pilot hay chứng minh kết quả.

**Phạm vi:** giả định bắt đầu vào thứ Hai sau khi quản lý duyệt. Dùng bản xuất CSV chung sẵn có vào ngày 1 và 6; giữ nguyên bản xuất, làm việc trên bản sao với vài cột theo dõi thủ công. Không cần kỹ sư, kho dữ liệu hay ngân sách mới. Không đề nghị thay đổi chi quảng cáo trong pilot.

**Vai trò:** Operations sở hữu danh sách hồ sơ, trạng thái, người xử lý và bước tiếp theo; có quyền đề xuất, không duyệt chi. Finance chốt định nghĩa, xác minh hoàn tiền và đối soát nguồn. Quản lý duyệt pilot và thay đổi quy trình; mọi thay đổi chi tiêu phải được quản lý duyệt riêng. Hai người không tự ghi đề xuất thành quyết định đã duyệt.

**Giải quyết khác biệt định nghĩa ngày 1:** Finance sở hữu doanh thu thuần theo ngày ghi nhận, sau hoàn tiền. Operations giữ gross booked theo ngày tạo đơn dưới tên riêng; không trộn vào doanh thu thuần hoặc so sánh hai số như cùng chỉ tiêu. Finance chốt quy tắc kỳ ghi nhận hoàn tiền. Tuổi hồ sơ tính theo ngày yêu cầu hoàn tiền đến thời điểm chụp trạng thái, bằng ngày lịch; khác với lịch 10 ngày làm việc. Cả hai ký nhận phiên bản định nghĩa trước khi tính; quy tắc chưa chốt hoặc trường thiếu phải ghi “chưa có”, không thay bằng 0/ngày tạo đơn.

| Thời điểm | Việc làm và đầu ra để ra quyết định |
|---|---|
| Ngày 1 | Kiểm kê cột CSV và hồ sơ; tạo mã hồ sơ duy nhất, ngày yêu cầu, trạng thái, lý do kẹt, chủ xử lý, việc tiếp theo/hạn. Finance xác minh bằng chứng hoàn tiền. Chụp baseline, không tự điền số thiếu. |
| Ngày 2–3 | Operations rà hồ sơ mở 15 phút/ngày, cập nhật bằng chứng và lý do kẹt; Finance kiểm tra ngoại lệ. Xác định một nút thắt từ hồ sơ thực tế. |
| Ngày 4–5 | Quản lý chọn thử một cải tiến không thêm chi phí, ví dụ một chủ xử lý + hạn bước tiếp theo, nếu đúng nút thắt. Ghi nhóm hồ sơ áp dụng, thời điểm và lý do; chưa đủ bằng chứng thì tiếp tục đo. |
| Ngày 6 | Finance đối soát bản xuất thứ Hai mới trong 30 phút, giải thích chênh lệch; Operations chụp trạng thái và cập nhật hồ sơ mở. |
| Ngày 7–9 | Theo dõi cùng cohort mở ngày 1 và tách hồ sơ mới; không lấy việc thêm hồ sơ làm mức xử lý kém đi. |
| Ngày 10 | Chụp trạng thái đã xác minh. Hai người trình một trang: backlog, tuổi, cohort đã xử lý, nút thắt và chi phí thời gian. Quản lý ghi quyết định giữ/sửa/dừng thử hoặc hoãn vì thiếu dữ liệu. |

**Cách biết có ích:** định nghĩa đã được hai người xác nhận; hồ sơ được rà có mã và bằng chứng, không đếm trùng; 100% hồ sơ mở có chủ xử lý và bước tiếp theo hoặc ngoại lệ được giải thích; quản lý ra hoặc chủ động hoãn một quyết định có dẫn chứng trong log. Operations ghi thời gian duy trì thực tế, mục tiêu không quá 15 phút/ngày. Đây là ngưỡng pilot đề xuất, chưa phải kết quả. Giảm backlog/tuổi hồ sơ là tín hiệu mô tả; 10 ngày không chứng minh nhân quả hay tăng doanh thu. Nếu thiếu ngày/trạng thái/bằng chứng ở ngày 1, thu hẹp thành kiểm kê và hoãn kết luận cải tiến.
