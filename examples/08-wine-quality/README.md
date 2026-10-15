# Bàn giao Wine Quality

Mở `report.html` bằng trình duyệt. Báo cáo và biểu mẫu đọc/điền ngoại tuyến; các liên kết UCI/DOI chỉ bổ sung xuất xứ, không cần tải để đọc báo cáo. `work-form.html` là biểu mẫu mới cho một hồ sơ; `review-40.csv` là danh sách 20 bản ghi dữ liệu đầu của mỗi tệp, chưa giao người thật và đang HOLD.

## Dựng lại, không cần mạng

Môi trường: Python 3.10 trở lên với thư viện chuẩn, không cần pandas, Node, pip hay thư viện tải thêm. Có thể dùng Python 3.12.14 đã được kiểm tra trên máy tác giả. Giữ nguyên toàn bộ thư mục `practical` và cấu trúc `input/source`.

Từ thư mục gói `practical`, chạy nguyên lệnh:

```sh
python build.py
```

Lệnh này kiểm tra SHA-256 của các nguồn đã giữ; đọc hai CSV; tạo lại `facts.csv`, `report.html`, `review-40.csv`, `work-record-template.csv` và `source-manifest.json` ngay trong gói. Không tự tải nguồn, không sửa nguồn. Nếu SHA-256 không khớp, lệnh dừng để tránh thay bản chụp một cách im lặng. Một thông báo mismatch không chứng minh dữ liệu mới sai; nó chỉ khác bản chụp được giao.

Lệnh dựng ghi đè các đầu ra trên. Nếu ghi việc bằng CSV, lưu bản ghi đã điền dưới tên mới; giữ `work-record-template.csv` làm mẫu trống.

`report.template.html` là mẫu giao diện có thể sửa; `build.py` giữ toàn bộ công thức. `work-form.html` là biểu mẫu tĩnh có thể chỉnh trực tiếp, không bị lệnh dựng ghi đè. `PROVENANCE.md` ghi nguồn, giấy phép và dấu nhận dạng được giao. `SELF-REVIEW.md` ghi kiểm tra đã thực hiện và giới hạn thực tế.

## Quy tắc dữ liệu

- CSV UTF-8, dấu phân cách `;`, dấu thập phân `.`. Kiểm tra đúng 12 cột và đủ trường mỗi dòng. Header không tính là một bản ghi.
- `quality` hợp lệ khi là số nguyên từ 0 tới 10. Trống và sai được đếm riêng. Chúng vẫn nằm trong mẫu số gốc nhưng không vào tử số ngưỡng. Hai bản chụp hiện có đều không gặp điểm thiếu/sai.
- Tử số là tổng bản ghi `quality <= 5`. Mẫu số là tất cả bản ghi dữ liệu trong từng tệp gốc. Phần trăm = tử/mẫu × 100. Chênh lệch điểm phần trăm = tỷ lệ đỏ − tỷ lệ trắng.
- `facts.csv` dùng đơn vị fraction cho tỷ lệ (0–1), percentage_points cho chênh lệch. Tỷ lệ chưa làm tròn; độ dài biểu diễn thập phân theo float Python. Báo cáo hiển thị 2 chữ số; phân bố nhỏ dùng 1 chữ số.
- Trùng bản ghi: so sánh nguyên 12 chuỗi giá trị sau khi phân tích CSV, không ép số, không xóa, không coi trùng là lỗi. Dòng lặp thêm = tổng (kích thước nhóm − 1). Dòng thuộc nhóm trùng tính cả lần xuất hiện đầu.
- Phân bố giữ đầy đủ bậc điểm 0–10, bao gồm các mức không xuất hiện. Không coi ordinal score là thang khoảng cách bằng nhau; không tính điểm trung bình để xếp hạng.
- Danh sách kiểm tra giữ `source_file + source_data_row`, vị trí từ 1 sau header. Đây không phải ID người/chai/mẫu vật lý. Không lấy mẫu ngẫu nhiên, không suy rộng từ 40 dòng.

## Ghi một hồ sơ

Mở biểu mẫu. Chọn tệp, ghi vị trí nguồn, trường và giá trị gốc (giữ trống nếu gốc trống). Ghi từng điều kiện và bằng chứng. Chọn một người thực sự được giao khi đã biết. Ghi lý do và hành động tiếp theo. Tải JSON trước khi đóng trang; không có tự lưu hay gửi đi. Mẫu CSV trống là phương án thay thế đơn giản.

Thiếu hoặc chưa xác nhận bản chụp, xuất xứ, phạm vi, người/sự sẵn sàng hay quyền: **HOLD**. Đủ bằng chứng trên hồ sơ: chỉ **READY FOR REVIEW**, chưa phải cho phép bắt đầu. Quyết định bắt đầu phải được người có thẩm quyền ghi riêng. Chưa có nhân sự hoặc phê duyệt thực tế nào trong gói.

Kế hoạch giả định: 40 hồ sơ × 3 phút = 120 phút công; hai người mỗi người 20 hồ sơ, khoảng 60 phút trôi qua chỉ khi cả hai thực sự làm song song. Đối chiếu hồ sơ trên máy tính; không thử nếm hoặc xác nhận chất lượng rượu.

## Bản quyền và phạm vi

Cortez và cộng sự (2009), Wine Quality, UCI, DOI 10.24432/C56S3T. Nguồn CC BY 4.0; bản giấy phép và từ điển gốc lưu cục bộ. Hai CSV nguyên byte. Báo cáo là phân tích dẫn xuất ngày 15/10/2026. Không kết luận nhân quả, thị trường hiện tại, thương hiệu, lô, giá, chi phí hoặc giao dịch từ các tệp này.
