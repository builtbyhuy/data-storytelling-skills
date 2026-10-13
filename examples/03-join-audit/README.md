# Tiền bị tính lặp ở đâu khi ghép bảng?

[PDF một trang](brief.pdf) · [SVG sửa được](brief.svg) · [CSV kế toán](invoice-reconciliation.csv) · [Memo](memo.md)

![Ma trận 6 tổ hợp cho thấy một hóa đơn bị lặp, bridge giải thích hóa đơn chưa trả bị bỏ, bảng đối chiếu giữ đủ 4 hóa đơn](brief.png)

## Yêu cầu mẫu

Đưa hai CSV và [source contract](inputs/source-notes.md):

> Tôi nối dòng hóa đơn với phân bổ thanh toán theo invoice_id và doanh thu nhảy lên. Kiểm hai CSV, giải thích tiền dư xuất hiện ở đâu, rồi đưa bảng đối chiếu doanh thu–tiền đã thu đáng tin để kế toán dùng; giữ hóa đơn chưa thanh toán. Kèm bản giải thích một trang ngắn, đẹp, dễ hiểu để gửi nội bộ. Chỉ soạn, không gửi. Hình hoặc bảng phải giúp thấy lỗi và cách sửa cụ thể.

Nguồn đúng trong ví dụ: giá trị hóa đơn 1.200 USD, đã thu 1.050, còn 150. Ghép thô và giữ mọi hóa đơn báo 2.500; chỉ giữ hóa đơn có thanh toán báo 2.350 và bỏ hóa đơn chưa trả 150. Cả hai còn cộng tiền đã thu thành 1.850. Bốn hóa đơn có nhiều dòng/nhiều khoản thu hợp lệ; không xóa chúng để chữa lỗi.

**Sửa:** cộng riêng theo từng hóa đơn, rồi ghép các tổng với danh sách hóa đơn làm gốc. Kế toán kiểm query thực tế và tổng trước khi thay báo cáo. Loại query thực tế chưa được cung cấp, nên ví dụ tái tạo cả INNER và LEFT.

## Công cụ đã chạy

[Audit report](audit/report.json) và [key-level evidence](audit/key-audit.csv) được tạo bằng helper canonical. Quan hệ many-to-many là đúng nhưng không làm phép cộng sau ghép trở nên hợp lệ. Script vật liệu hóa hai phép ghép nhỏ độc lập để kiểm row count, tiền lặp và hóa đơn bị bỏ. [Phép tính](calculations.json) · [Kết quả checks](audit-result.json).

## Tái tạo

```text
python examples/03-join-audit/rebuild.py --output ./scratch/join-v3
```

[Dependencies và giới hạn](../README.md). Chỉ chạy audit chuẩn-library độc lập:

```text
python skills/business-insight-diagnosis/scripts/join_audit.py --left examples/03-join-audit/inputs/invoice-lines.csv --right examples/03-join-audit/inputs/payment-allocations.csv --left-key invoice_id --right-key invoice_id --expect many-to-many --left-measure net_amount_usd --out ./scratch/join-audit
```

Dữ liệu giả lập, snapshot không có ngày lịch được cung cấp. Đây là bản soạn và đối chiếu theo source contract, chưa sửa production hoặc xác nhận chính sách kế toán tổ chức khác. Lượt độc lập mới dùng diagnosis/composition/chart/narrative 3.0; bản công bố có sửa ngôn ngữ và bàn giao theo đọc trang.
