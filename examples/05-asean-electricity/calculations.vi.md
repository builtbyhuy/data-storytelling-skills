# Phép tính và căn cứ cho bản biên tập

## Nguồn đóng băng
Ember Yearly Electricity Data. CSV tải 14/10/2026, nguồn được sửa lần cuối 06/10/2026. SHA-256: `1fd193cd5f4c2eda95756233869602b578cbdd7c030813c316b11f8b91eeeed4`. Giấy phép CC BY 4.0. Phân tích, lọc và trình bày riêng, không hàm ý Ember xác nhận.

Grain: ISO + năm + nguồn điện. 200 hàng = 5 nước × 10 năm × 4 nguồn. Dòng `Wind and solar` là tổng gộp, chồng lặp `Wind` và `Solar`; tuyệt đối không cộng cả ba dòng. Tỷ trọng công bố của tổng gộp là chỉ tiêu chuẩn cho biểu đồ; mẫu số là phát điện nội địa, loại nhập khẩu ròng.

## Công thức
- Chênh lệch dài hạn (điểm phần trăm) = tỷ trọng công bố 2024 − tỷ trọng công bố 2015.
- Đối chiếu tỷ trọng = TWh gió + mặt trời ÷ TWh tổng phát điện × 100.
- Tăng sản lượng 2023–2024 (%) = (TWh 2024 ÷ TWh 2023 − 1) × 100.
- Chênh lệch giữa nước = hai tỷ trọng cùng năm trừ nhau; không lấy tỷ lệ tăng tương đối từ các nền thấp làm góc chính.
- Hiển thị tiếng Việt dùng dấu phẩy thập phân, làm tròn nửa lên đến 2 chữ số. Phép tính dùng Decimal và độ chính xác CSV.

## Số quyết định
| Nước | 2015 (%) | 2024 (%) | Tăng (điểm phần trăm) |
|---|---:|---:|---:|
| Việt Nam | 0.079 | 14.697 | 14.618 |
| Thái Lan | 1.468 | 5.802 | 4.334 |
| Malaysia | 0.182 | 3.016 | 2.834 |
| Philippines | 1.08 | 2.883 | 1.803 |
| Indonesia | 0.026 | 0.372 | 0.346 |

Việt Nam 2023–2024: gió + mặt trời 42.683 → 45.655 TWh (+6.962959492069%); tổng phát điện 282.0 → 310.633 TWh (+10.153546099291%). Tỷ trọng 15.136 → 14.697%, chênh lệch -0.439 điểm phần trăm. Khoảng cách với Thái Lan năm 2024: 8.895 điểm phần trăm.

## Kiểm tra đã thực thi khi dựng
Không trùng khóa; đủ mọi tổ hợp ISO/năm/nguồn; không thiếu hai cột quyết định; tổng phát điện dương. Cả 50 quan sát gộp đối chiếu với tổng hai thành phần và mẫu số. Dung sai 0,001 TWh hoặc 0,001 điểm phần trăm cho sai khác làm tròn. Kết quả chi tiết trong facts.json/reconciliation và annual-calculations.csv. Tỷ trọng gộp có thể lệch tổng hai tỷ trọng thành phần 0,001 điểm do làm tròn (ví dụ Việt Nam 2024).

## Căn cứ diễn giải và giới hạn
Góc chọn: khoảng cách tỷ trọng của Việt Nam mở rộng trong nhóm năm nước, nhưng tỷ trọng 2024 giảm dù sản lượng tăng. Quan hệ mẫu số đủ giải thích hiện tượng số học; dữ liệu không phân biệt nguyên nhân chính sách, điều kiện tự nhiên, huy động, báo cáo hay lưới điện. Một năm giảm không chứng minh xu hướng suy giảm dài hạn. Không đại diện toàn ASEAN; không đo tiêu thụ/công suất, độ đầy đủ điện, giá hay tác động can thiệp.

Phương pháp Ember trang vật lý 9–10 định nghĩa phát điện và loại nhập khẩu; trang 13 nêu giới hạn captive/distributed generation; trang 50 mô tả ước tính điện tự sản xuất Indonesia; trang 60/72/86–87/93 mô tả các nguồn năm. Cảnh báo điện gió Việt Nam trước 2022 ở trang 93 là cho chuỗi tháng EVN; không chuyển nó thành kết luận về mọi quan sát năm dùng ở đây.

## Vai trò và trạng thái
Bản này là đề xuất họp biên tập. Phóng viên đề xuất: đối chiếu số và phạm vi trong 2 ngày làm việc. Biên tập viên: quyết định cuối ngày 2 theo điều kiện trên trang 4. Chưa giao người cụ thể, chưa gửi câu hỏi, chưa duyệt hoặc xuất bản. Nguồn ngoài được nêu ở trang 4 là việc cần kiểm tra tiếp, không phải dữ liệu mới dùng cho bản này.
