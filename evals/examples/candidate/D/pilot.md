# Pilot báo cáo hoàn tiền trong 10 ngày làm việc — đề xuất, chưa chạy

**Quyết định ngày 10:** ưu tiên checklist chứng từ, quy tắc bàn giao Operations–Finance hay sửa dữ liệu trước? Xác định hồ sơ hoàn tiền đang kẹt ở bước nào, bao lâu, tiền nào đã được Finance xác nhận. Chưa có dữ liệu từng hồ sơ hay kết quả can thiệp; số nền và lợi ích còn chưa biết.

**Nguồn.** Dùng CSV thứ Hai; đề xuất ngày 1 và 6 là hai bản xuất, lưu thời điểm/phiên bản. Trong file làm việc, cần mã hồ sơ/mã đơn, ngày yêu cầu hoàn, trạng thái, lý do chờ, bước tiếp theo/người phụ trách; Finance xác nhận tiền, tiền tệ và ngày ghi nhận. Các cột này chưa được cung cấp. Ngày 10 dùng cập nhật thủ công có giờ kiểm tra, không giả là bản xuất hệ thống. Không có dữ liệu hồ sơ hoặc khóa đối soát thì dừng định lượng, ghi dữ liệu thiếu và sửa nguồn trước.

**Định nghĩa.** Finance có quyền định nghĩa doanh thu thuần theo ngày ghi nhận, sau hoàn tiền. Ops giữ doanh thu đặt chỗ gộp theo ngày tạo đơn; không đổi tên thành doanh thu thuần hay so trực tiếp hai tổng. Ngày 2 Finance chốt phân kỳ hoàn, khóa và tiền tệ; Ops đối chiếu đơn–hồ sơ. Tuổi hồ sơ tính từ ngày yêu cầu hoàn. Thiếu dữ liệu ghi “chưa biết”, đếm riêng, không điền 0; không cộng tiền đơn lặp qua nhiều hồ sơ. `metric-contract.csv` là đề xuất đến khi chủ chỉ số duyệt; tranh chấp hiện cạnh kết luận.

**Vai trò và nhịp làm việc** (thời lượng đề xuất, cần hai người xác nhận khả năng):

| Ngày | Việc và người chịu trách nhiệm |
|---|---|
| 1 | Ops kiểm tra hồ sơ/khóa, Finance kiểm tra hoàn; chọn phạm vi và số nền hoặc ghi thiếu dữ liệu. Tối đa 30 phút/người. |
| 2 | Finance chốt nghĩa; Ops đối chiếu tranh chấp. Chưa thống nhất thì chưa so doanh thu. |
| 3–5 | Mỗi người tối đa 10 phút/ngày cập nhật bước tiếp theo/xác nhận tiền; ngày 5 cùng xem điểm nghẽn 15 phút. |
| 6 | Finance đối soát tiền, Ops kiểm tra trạng thái bản xuất mới: đóng, mở, mới và chưa biết. |
| 7–9 | Ghi bước đã làm, trở ngại và phản chứng; chưa triển khai cải tiến chưa duyệt. |
| 10 | Ops tóm tắt một trang. Manager xem 20 phút, chọn bước tiếp theo/trì hoãn có căn cứ; ghi sau quyết định thật. |

**Cách chọn.** Phân nhóm lý do chờ đã xác minh: thiếu chứng từ → checklist; đủ chứng từ nhưng chờ xác nhận/chuyển giao → quy tắc bàn giao; khóa/phân loại không đáng tin → sửa dữ liệu. Chọn theo số hồ sơ và tuổi chờ, bổ sung tiền đã xác nhận. Cờ quá 5 ngày làm việc là đề xuất kiểm tra, chưa phải SLA.

**Có ích khi:** hai người đối soát cùng định nghĩa/phiên bản; hồ sơ mở có bước tiếp theo hoặc lý do chưa thể xác định; manager ghi lựa chọn/trì hoãn có căn cứ; công sức trong mức thỏa thuận. Có bằng chứng dùng báo cáo thì tiếp tục một cải tiến nhỏ được duyệt; thiếu dữ liệu/công sức vượt khả năng thì thu hẹp hoặc dừng. Theo dõi hồ sơ mở ngày 1 đóng đến ngày 10 cùng cohort, tách hồ sơ mới; đây là mô tả, không phải tác động nhân quả. Chưa có kết quả hay mục tiêu giảm tồn cam kết.

Ops chỉ đề xuất và theo dõi. Manager phải duyệt mọi thay đổi chi quảng cáo; pilot không có ngân sách mới, engineer, kho dữ liệu, cài hệ thống hay dịch vụ chạy nền. Bản ghi đầu tiên là PROPOSED; các trường duyệt, triển khai và kết quả để trống đến khi có bằng chứng.
