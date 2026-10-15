# N91 — Phiếu tự kiểm tra bản bàn giao đầu tiên

Bắt đầu: 2026-10-15T11:39:23+07:00.
Mốc hoàn tất/FINAL: 2026-10-15T11:51:31.4765592+07:00.
Giới hạn được giao: 25 phút. Tác giả làm một mình; owner edits: 0. Các sửa chữa dưới đây do chính tác giả thực hiện trước FINAL. Model/sampling chính xác không được cung cấp, không suy đoán.

## Số liệu và nguồn

- Đối chiếu SHA-256 của cả năm tệp được giữ với nguồn đã giao. Hai CSV, từ điển, ZIP và giấy phép không đổi byte.
- Kiểm tra riêng bằng cách đọc dòng nguồn thô và tính phân số: đỏ 744/1599 = 46,5290806754%; trắng 1640/4898 = 33,4830543079%; chênh 13,0460263675 điểm phần trăm. Kết quả khớp facts.csv, nhãn hiển thị và độ dài thanh.
- Đối chiếu từng bậc 0–10, tổng phân bố, 0 điểm thiếu/sai của từng tệp, 240/937 dòng lặp thêm và số nhóm/thành viên trùng. Không loại dòng trùng. Điểm 9 vẫn có 5 dòng trắng và 0 dòng đỏ.
- 40 bản ghi khớp từng giá trị nguồn, vị trí 1–20 mỗi tệp; định danh file + source_data_row không trùng; người được giao còn trống và trạng thái HOLD. 40×3=120 phút công; 120/2=60 phút trôi qua chỉ dưới giả định hai người thực sự làm song song.

## Bản hiển thị và thao tác

- Dùng Chrome 155.0.8059.40 headless, đọc file cục bộ với yêu cầu mạng ngoài bị chặn. Thực sự xem các ảnh báo cáo ở 960px và 390px: phần đầu, phân bố, trùng dòng, kế hoạch, nguồn mở rộng và bảng số chính xác; xem biểu mẫu mới, điều kiện, giao việc và hướng dẫn trạng thái. Không có lỗi trang hoặc yêu cầu mạng ngoài; không tràn ngang toàn trang ở hai chiều rộng này.
- Tự sửa sau ảnh đầu: tách masthead khỏi phụ đề; giữ ký hiệu ≤ 5 cùng dòng; thay font tiêu đề biểu mẫu để tiếng Việt hiển thị liền mạch; đưa tiêu đề bảng ra ngoài vùng cuộn; rút bảng mẫu số về bốn cột để đọc trọn trên điện thoại. Bảng phân bố chi tiết vẫn có cuộn chủ động và nhãn điểm được giữ bên trái. Đã xuất lại và xem vùng bị thay đổi.
- Tra được 46,53% với 744/1.599 dòng đỏ; 33,48% với 1.640/4.898 dòng trắng; và điểm 9 của trắng là 5 dòng (0,10%). Đọc được giới hạn dòng nguồn, ngưỡng giả định và trạng thái HOLD trước thực thi. Đây là tự đọc lại của tác giả, không phải kiểm chứng hiểu của người dùng thật.
- Đo tương phản các cặp chữ/nền và thanh/nền chính: chữ đạt ít nhất 5,12:1 trong các cặp được đo; thanh thấp nhất 4,79:1. Kiểm tra tên truy cập của hai figure và ID không trùng. Tab đến liên kết đầu có viền focus 3px thấy được.
- Biểu mẫu ban đầu để người nhận trống, điều kiện unknown, giá trị gốc trống, HOLD. Thử tải JSON giữ riêng chuỗi rỗng, unknown, not done; reset trở về mặc định. Hướng dẫn thủ công giữ HOLD nếu thiếu điều kiện, chỉ READY FOR REVIEW khi đủ bằng chứng; chưa cấp quyền bắt đầu.

## Dựng lại và bàn giao

- Công thức di động giữ nguyên: python build.py, chạy từ thư mục practical; Python 3.10+ và thư viện chuẩn. Trên máy này thực thi cùng build.py qua helper Python bắt buộc, dùng Python 3.12.14.
- Đã chạy lại từ thư mục riêng với chỉ mã dựng, mẫu HTML và nguồn được giữ. Năm đầu ra report.html, facts.csv, review-40.csv, work-record-template.csv, source-manifest.json khớp SHA-256 từng byte với gói chính. Đã dọn bản sao kiểm tra; giữ receipt và ảnh làm bằng chứng tự kiểm tra.
- Các hạng mục được giao tồn tại trong practical: báo cáo, facts.csv, nguồn nguyên byte/xuất xứ/hash, mã và mẫu dựng, README, biểu mẫu mới và danh sách 40 dòng. Không dùng web, CUA, dịch vụ ngoài, cài đặt hay người phụ làm bài.

## Giới hạn thực tế

Chỉ kiểm tra Chrome cục bộ ở hai chiều rộng nêu trên, chưa kiểm tra Safari, thiết bị điện thoại thật, máy in hoặc trình đọc màn hình đầy đủ. Các đo tương phản và focus không chứng nhận toàn bộ khả năng tiếp cận. Chưa có kiểm tra của người dùng thật, nhân sự thật, quyền bắt đầu, kiểm tra hồ sơ đã thực thi hay kết quả kinh doanh. Nguồn lịch sử không có căn cứ suy rộng thị trường hoặc nhân quả; bất định đó được giữ trong báo cáo.