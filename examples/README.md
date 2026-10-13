# Ví dụ dùng trong công việc

Ba tình huống giả lập, mỗi tình huống có yêu cầu có thể sao chép, dữ liệu gốc, tài liệu một trang, nguồn chỉnh sửa được và bản tính tái tạo được.

| Việc cần làm | Bản bàn giao | Mở ví dụ |
|---|---|---|
| Doanh thu tăng nhưng đóng góp giảm | Memo họp, bảng tính Excel, kế hoạch thử giao hàng và bản ghi quyết định đã điền | [01 — Quyết định lợi nhuận](01-profit-decision/README.md) |
| Tỷ lệ gộp bị dùng để kết luận coaching có tác dụng | Báo cáo sửa, phép so sánh cùng cơ cấu và câu kết luận có thể dùng ngay | [02 — So sánh sales](02-fair-comparison/README.md) |
| Ghép bảng làm tiền tăng | Minh họa tính lặp, bảng đối chiếu từng hóa đơn và audit đã thực thi | [03 — Đối chiếu hóa đơn](03-join-audit/README.md) |

## Dùng ngay

Mở PDF để đọc hoặc in; SVG giữ văn bản và hình vector để chỉnh sửa. Memo Markdown giữ nội dung để sao chép. CSV/JSON giữ số chính xác. Ví dụ1 có workbook với dữ liệu, công thức và giá trị lưu sẵn; các giá trị đã đối chiếu nguồn, chưa chạy lại bằng Excel.

Để dùng skill với dữ liệu của bạn, sao chép yêu cầu trong từng ví dụ và đưa các file nguồn phù hợp. Các script của gallery tái tạo snapshot giả lập này; kết luận, ngưỡng đề xuất và bố cục cần được xem lại nếu dữ liệu đổi. Đây không phải một mẫu quyết định tự áp vào doanh nghiệp khác.

## Tái tạo

Với Python và các thư viện có sẵn phù hợp:

```text
python examples/01-profit-decision/rebuild.py --output ./scratch/profit-v3
python examples/02-fair-comparison/rebuild.py --output ./scratch/comparison-v3
python examples/03-join-audit/rebuild.py --output ./scratch/join-v3
```

Dùng các thư mục đầu ra riêng. Script giữ nguồn và dựng lại phép tính, văn bản, SVG, PDF, PNG cùng bản tính/bảng đối chiếu liên quan. Chúng không tải thư viện hoặc gọi tài khoản/dịch vụ.

Rebuild 1 cần `reportlab`, `xlsxwriter`, `pypdf` và Poppler. Rebuild 2 cần `reportlab`, `pypdf`, `pypdfium2`. Rebuild 3 cần `reportlab`, `pypdf`, `Pillow` và Poppler; `--poppler` cho phép chỉ vị trí renderer. Các bản xuất đã kiểm dùng Arial có sẵn trên Windows, không phân phối file font. Các skill và công cụ join audit vẫn dùng được độc lập, không cần bộ dựng PDF này.

## Các ví dụ được làm như thế nào

Ba agent mới chạy bản skill đã freeze từ nguồn và brief, không nhận hình cũ hoặc đáp án. Dữ liệu là các fixture tổng hợp đã có: đây là lượt chạy lại độc lập theo cùng input, không phải holdout mới hoặc so sánh baseline. Owner tính lại nguồn riêng, xem bản xuất và cho một reviewer chỉ đọc pixels. Bản công bố bổ sung các sửa về thuật ngữ, điều kiện quyết định, bảng tổng và đường dẫn portable.

Các lượt đọc của model giúp tìm điểm mơ hồ; chúng không chứng minh người thật đã hiểu hơn hoặc chấp nhận thẩm mỹ. Không có kết quả khách hàng, phê duyệt/thực thi thử nghiệm hay lợi ích kinh doanh thực. [Kiểm tra 3.0 và giới hạn](../evals/book-aligned-v3.md). [Kết quả so sánh trước đây](../evals/README.md) được giữ nguyên.
