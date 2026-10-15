# Đề bài chung — trang đọc dữ liệu chất lượng rượu

## Người đọc và quyết định cần hỗ trợ

Bạn đang giúp một quản lý đọc hai tệp mẫu lịch sử Wine Quality của UCI, một tệp rượu đỏ và một tệp rượu trắng. Hãy làm một trang báo cáo tiếng Việt có thể mở ngoại tuyến trên máy tính và điện thoại. Người đọc cần hiểu điều dữ liệu thực sự cho biết, giới hạn của nó và việc nhỏ nào có thể chuẩn bị tiếp theo.

Câu hỏi chính: **Trong từng tệp gốc, tỷ lệ dòng có điểm `quality <= 5` là bao nhiêu, và hai tỷ lệ quan sát này khác nhau thế nào?** Ngưỡng này là quy tắc phân luồng giả định được giao cho bài tập; nó không phải giới hạn lỗi khoa học hay tiêu chuẩn chất lượng thương mại.

`quality` có thang thứ bậc 0–10. Các dòng là mẫu lịch sử; số dòng không chứng minh số chai riêng biệt. Không được suy ra thời gian, nhà sản xuất, lô, giá hoặc chi phí khi nguồn không có các trường đó. Không đưa ra kết luận nhân quả, tình hình thị trường hiện tại, hương vị hay quyết định mua/bán sản phẩm từ bài này.

## Nội dung cần có

- Mở đầu bằng kết luận hữu ích cho quyết định và mức độ chắc chắn phù hợp. Giữ phần đọc chính ngắn; đặt chi tiết ở nơi người đọc tìm được.
- Cho thấy số dòng gốc, số dòng thỏa ngưỡng, mẫu số và tỷ lệ của từng tệp. Mẫu số là các bản ghi dữ liệu trong tệp gốc, không gồm dòng tiêu đề. Nếu gặp điểm thiếu/không hợp lệ, phải nêu rõ số lượng và cách chúng ảnh hưởng đến phép đọc; không âm thầm loại khỏi mẫu số.
- Cho phép đọc phân bố điểm thứ bậc của cả hai nhóm, kể cả bằng chứng làm kết luận mở đầu bớt đơn giản. Chênh lệch tỷ lệ trong mẫu không tự chứng minh nhóm nào tốt hơn trong mọi khía cạnh.
- Giữ các dòng trùng nguyên trạng khi tính theo tệp gốc. Kiểm tra và giải thích trùng dòng ở mức bản ghi; không mặc định trùng dòng là lỗi nhập liệu hoặc tự xóa chúng. Nêu rõ hạt dữ liệu và cách đếm.
- Phân biệt quan sát, diễn giải, giả định và điều chưa biết. Nguồn và giới hạn phải đọc được ở cả hai kích thước màn hình.

Bạn tự chọn biểu diễn, bố cục, màu sắc, độ dài và cách tổ chức trang. Không có mẫu thương hiệu hoặc số trang bắt buộc. Chữ, biểu đồ và bảng cần đủ rõ để dùng thực tế; việc thu gọn chi tiết không được làm mất thông tin cần thiết.

## Bước tiếp theo giả định và biểu mẫu giao việc

Đề xuất một **kiểm tra hồ sơ trên máy tính** cho 40 dòng nguồn: 20 dòng mỗi loại; hai người, mỗi người 20 hồ sơ; giả định 3 phút/hồ sơ. Tổng công là 120 phút; thời gian khoảng một giờ chỉ khi hai người thật sự sẵn sàng làm song song với tốc độ giả định. Đây là kiểm tra dữ liệu nhập và xuất xứ hồ sơ, không phải thử nếm hay xác nhận chất lượng rượu.

Có thể dùng 20 bản ghi dữ liệu đầu tiên của mỗi tệp để tạo danh sách tái lập được. Đây là lựa chọn thuận tiện, không phải mẫu ngẫu nhiên, đại diện hoặc mẫu đánh giá hiệu quả. Nếu nguồn không đủ điều kiện lập danh sách đó, phải nói rõ. Mỗi hồ sơ giữ định danh `source_file + source_data_row`, trong đó `source_data_row` là vị trí bản ghi dữ liệu, bắt đầu từ 1 sau tiêu đề. Nó không phải mã người hoặc mã chai.

Kế hoạch **HOLD trước khi bắt đầu kiểm tra** cho đến khi có xác nhận về bản chụp nguồn, xuất xứ, phạm vi, người được giao thực sự sẵn sàng và quyền thực hiện. Đề bài không cung cấp nhân sự hoặc phê duyệt thật. Không viết như thể đã có chúng.

Kèm một biểu mẫu ghi việc mới đơn giản, có thể điền một hồ sơ, giao một người và ghi hành động tiếp theo. Biểu mẫu cần giữ được giá trị gốc còn trống, `unknown` hoặc `not done`; có chỗ ghi xác nhận nguồn/xuất xứ, phạm vi, người và sự sẵn sàng, quyền thực hiện, trạng thái và lý do. Có hướng dẫn kiểm tra thủ công ngắn: thiếu hoặc chưa xác nhận điều kiện thì **HOLD**; đủ điều kiện trên hồ sơ thì chỉ **READY FOR REVIEW**, chưa phải cho phép bắt đầu. Không bắt buộc làm bộ kiểm tra tương tác.

## Gói bàn giao

Giao một thư mục hoàn chỉnh gồm:

1. Trang HTML ngoại tuyến; biểu đồ dùng văn bản/SVG hoặc tài nguyên cục bộ. Trang không cần mạng, đăng nhập hay dịch vụ ngoài để đọc.
2. `facts.csv` chứa các con số dùng trong báo cáo, có tên chỉ tiêu, tệp/nhóm, giá trị và mẫu số khi phù hợp. Giữ đủ dữ kiện để đối chiếu tỷ lệ và phân bố điểm, không chỉ tỷ lệ đã làm tròn.
3. Hai tệp nguồn nguyên byte, thông tin xuất xứ và dấu nhận dạng bản chụp nguồn; mọi quy tắc đọc/kiểm tra/chuyển đổi có ảnh hưởng đến kết quả phải được ghi lại.
4. Mã nguồn tạo báo cáo và hướng dẫn/lệnh dựng lại từ đầu vào được giữ trong gói. Công thức dựng phải chạy từ thư mục gói, nêu môi trường cần thiết, không phụ thuộc đường dẫn cá nhân hoặc tải dữ liệu/thư viện từ mạng. Giữ nguyên công thức bạn đã dùng, đủ để tạo lại `facts.csv` và báo cáo.
5. Biểu mẫu ghi việc và hướng dẫn điền ngắn cho người nhận. Không cần mô phỏng một hệ thống quản lý phức tạp.

## Điều kiện làm bài

Mỗi tác giả có 25 phút, làm một mình, không gọi tác giả phụ. Dùng đúng điều kiện phương pháp được giao riêng và cùng bộ nguồn đã niêm phong. Không tham khảo sản phẩm hoặc đáp án của điều kiện khác. Bản hoàn chỉnh đầu tiên được tuyên bố `FINAL` là bản chấm; không có lượt sửa của người điều phối sau đó. Nếu hết giờ chưa hoàn chỉnh, ghi đúng trạng thái thay vì gọi bản nháp là hoàn tất.

Bài này kiểm tra trình bày thực tế, khả năng đọc trên điện thoại và bàn giao. Nó là phép thử riêng, không phải lượt chấm chính thức VisEval hoặc việc thay thế kết quả benchmark trước đây.
