# Bản soạn nội bộ: sửa đối chiếu hóa đơn và tiền thu

**Dữ liệu giả lập để minh họa; chưa gửi, chưa thay báo cáo vận hành.**

Doanh thu hóa đơn đúng là **1.200 USD**, tiền đã thu **1.050 USD**, còn phải thu **150 USD**. Khoản tăng sau phép nối là lỗi đếm lặp. Cộng riêng từng nguồn theo `invoice_id`, rồi ghép với danh sách hóa đơn làm gốc sẽ giữ đủ bốn hóa đơn, gồm INV-1004 chưa trả.

| Hóa đơn | Dòng hóa đơn × khoản thu | Doanh thu đúng | Doanh thu sau nối trong | Phần cộng lặp | Tiền đã thu đúng | Còn phải thu |
|---|---:|---:|---:|---:|---:|---:|
| INV-1001 | 2 × 2 | 300 | 600 | 300 | 300 | 0 |
| INV-1002 | 2 × 3 | 500 | 1.500 | 1.000 | 500 | 0 |
| INV-1003 | 1 × 1 | 250 | 250 | 0 | 250 | 0 |
| INV-1004 | 2 × 0 | 150 | 0 (bị bỏ) | 0 | 0 | 150 |

Đơn vị: USD. Hai dòng 450 và 50 USD của INV-1002 ghép với ba khoản thu 250, 150 và 100 USD thành sáu tổ hợp. Mỗi dòng hóa đơn được tính ba lần: 500 thành 1.500 USD. INV-1001 tạo thêm 300 USD; tổng phần lặp là **1.300 USD**. Đây là nhiều dòng hàng và nhiều lần thu hợp lệ, không phải bản ghi nguồn trùng cần xóa.

Nếu dùng nối trong (INNER), INV-1004 bị loại vì chưa có khoản thu: **1.200 + 1.300 - 150 = 2.350 USD**, cao hơn nguồn 1.150 USD. Nếu dùng nối trái (LEFT) trực tiếp trên hai CSV, hóa đơn chưa trả được giữ nhưng doanh thu vẫn bị lặp: **2.500 USD**, cao hơn 1.300 USD. Cả hai cách cũng làm tiền thu thành **1.850 USD** thay vì 1.050 USD, thừa 800 USD vì khoản thu lặp theo số dòng hóa đơn. Chưa có truy vấn hoặc loại phép nối thực tế của người dùng; đây là hai hành vi đã tái tạo từ nguồn.

**Đề xuất để kế toán duyệt:** người phụ trách báo cáo cộng 7 dòng hóa đơn thành 4 tổng doanh thu, cộng 6 phân bổ thanh toán thành 3 tổng tiền thu, kiểm mỗi bảng có một dòng cho mỗi hóa đơn, rồi LEFT JOIN hai bảng tổng hợp. Chỉ đặt tiền thu bằng 0 khi hóa đơn thực sự không có khoản thu theo nguồn đầy đủ; không thay tiền lỗi hoặc thiếu bằng 0. Không dùng DISTINCT hoặc bỏ các dòng hợp lệ để chữa phép nối.

**Điều kiện trước khi thay báo cáo cho lần chốt này:** kế toán xác nhận đủ 4 mã hóa đơn, tổng doanh thu/tiền thu/còn phải thu lần lượt 1.200/1.050/150 USD, INV-1004 còn 150 USD, không có phân bổ vào hóa đơn ngoài nguồn và không có mã trùng trong bảng tổng. Nếu bất kỳ điều kiện nào lệch, giữ báo cáo chưa thay và đối chiếu nguồn trước. Đây là vai trò đề xuất, chưa phải phân công hoặc triển khai đã được phê duyệt.

Nguồn có thẩm quyền trong ví dụ: `inputs/source-notes.md`, `inputs/invoice-lines.csv`, `inputs/payment-allocations.csv`. Doanh thu trong bài là tổng giá trị hóa đơn sau giảm giá, chưa thuế; không suy rộng thành chính sách ghi nhận doanh thu thực tế. Nguồn quy định cùng mốc chốt nhưng không cho ngày lịch, không có hoàn tiền/hủy/số dư đầu kỳ/hóa đơn ngoài danh sách. Chi tiết số và dấu vân tay SHA-256 nằm trong `calculations.json`; kết quả audit và kiểm tái tạo nằm trong `audit/` và `audit-result.json`.
