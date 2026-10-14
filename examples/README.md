# Ví dụ dùng trong công việc

Hai lượt chạy nguyên bản trên dữ liệu thật và ba tình huống giả lập được biên tập. Mỗi ví dụ có yêu cầu, nguồn, file dùng được và cách tái tạo; phạm vi kiểm tra được ghi riêng.

| Việc cần làm | Bản bàn giao | Mở ví dụ |
|---|---|---|
| Chọn góc bản tin từ dữ liệu phát điện, giữ ngoại lệ và mẫu số | HTML đọc trên desktop/điện thoại, PDF/SVG vector, phép tính và việc kiểm tra trong hai ngày | [05 — Lượt chạy mới, không sửa tay](05-asean-electricity/README.md) |
| Ưu tiên hỗ trợ chuyên cần khi nguồn lực địa phương chưa xác minh | 9 trang PowerPoint/PDF, Excel công thức, điều kiện mở/hoãn và recipe nguyên bản | [04 — Lượt chạy dữ liệu thật, không sửa tay](04-attendance-pilot/README.md) |
| Doanh thu tăng nhưng đóng góp giảm | Memo họp, bảng tính Excel, kế hoạch thử giao hàng và bản ghi quyết định đã điền | [01 — Quyết định lợi nhuận](01-profit-decision/README.md) |
| Tỷ lệ gộp bị dùng để kết luận coaching có tác dụng | Báo cáo sửa, phép so sánh cùng cơ cấu và câu kết luận có thể dùng ngay | [02 — So sánh sales](02-fair-comparison/README.md) |
| Ghép bảng làm tiền tăng | Minh họa tính lặp, bảng đối chiếu từng hóa đơn và audit đã thực thi | [03 — Đối chiếu hóa đơn](03-join-audit/README.md) |

## Dùng ngay

Ví dụ04 giữ nguyên byte PPTX/PDF/XLSX, mã dựng và README của lần bàn giao đầu tiên. Nó dùng DfE thật, còn dịch vụ/ngân sách là giả lập; đề xuất chưa duyệt hoặc triển khai. Mở ba file để đọc/họp/đối chiếu, không cần dựng lại. [Nguồn và OGL](04-attendance-pilot/SOURCES.md).

Mở PDF để đọc hoặc in; SVG giữ văn bản và hình vector để chỉnh sửa. Memo Markdown giữ nội dung để sao chép. CSV/JSON giữ số chính xác. Ví dụ1 có workbook với dữ liệu, công thức và giá trị lưu sẵn; các giá trị đã đối chiếu nguồn, chưa chạy lại bằng Excel.

Để dùng skill với dữ liệu của bạn, sao chép yêu cầu trong từng ví dụ và đưa các file nguồn phù hợp. Các script của gallery tái tạo snapshot giả lập này; kết luận, ngưỡng đề xuất và bố cục cần được xem lại nếu dữ liệu đổi. Đây không phải một mẫu quyết định tự áp vào doanh nghiệp khác.

## Tái tạo

Ví dụ04 cần runtime Windows/Office mô tả trong [recipe](04-attendance-pilot/rebuild/README.md). Chuyển cả thư mục `rebuild` tới nơi khác, mở PowerShell tại đó và chạy `pwsh -NoProfile -File ./Build.ps1 -SourceDir ./source -BuildDir ./build-06 -OutputDir ./generated-06` vào thư mục đầu ra mới. Snapshot biểu đồ và kỳ nguồn có giới hạn cập nhật đã nêu rõ.

Với Python và các thư viện có sẵn phù hợp:

```text
python examples/01-profit-decision/rebuild.py --output ./scratch/profit-v3
python examples/02-fair-comparison/rebuild.py --output ./scratch/comparison-v3
python examples/03-join-audit/rebuild.py --output ./scratch/join-v3
```

Dùng các thư mục đầu ra riêng. Script giữ nguồn và dựng lại phép tính, văn bản, SVG, PDF, PNG cùng bản tính/bảng đối chiếu liên quan. Chúng không tải thư viện hoặc gọi tài khoản/dịch vụ.

Rebuild 1 cần `reportlab`, `xlsxwriter`, `pypdf` và Poppler. Rebuild 2 cần `reportlab`, `pypdf`, `pypdfium2`. Rebuild 3 cần `reportlab`, `pypdf`, `Pillow` và Poppler; `--poppler` cho phép chỉ vị trí renderer. Các bản xuất đã kiểm dùng Arial có sẵn trên Windows, không phân phối file font. Các skill và công cụ join audit vẫn dùng được độc lập, không cần bộ dựng PDF này.

## Các ví dụ được làm như thế nào

Ví dụ04: source author, executor mới, oracle số liệu và hai lượt đọc độc lập có vai trò riêng. Nguồn, brief và skill 3.1.2 được freeze trước output; owner không xem nháp, không gợi ý nội dung và không sửa đầu ra/mã dựng sau bàn giao. Hai lượt trước không đạt được giữ lại, sửa skill rồi đổi bộ dữ liệu. Năm nhóm kiểm tra của lượt thứ ba đạt; [hồ sơ đầy đủ về phạm vi và giới hạn](../evals/forward-v3.1.md). Wrapper công bố giải thích các HTML/receipt riêng bị loại, không sửa các file bàn giao.

Ba agent mới chạy bản skill đã freeze từ nguồn và brief, không nhận hình cũ hoặc đáp án. Dữ liệu là các fixture tổng hợp đã có: đây là lượt chạy lại độc lập theo cùng input, không phải holdout mới hoặc so sánh baseline. Owner tính lại nguồn riêng, xem bản xuất và cho một reviewer chỉ đọc pixels. Bản công bố bổ sung các sửa về thuật ngữ, điều kiện quyết định, bảng tổng và đường dẫn portable.

Các lượt đọc của model giúp tìm điểm mơ hồ; chúng không chứng minh người thật đã hiểu hơn hoặc chấp nhận thẩm mỹ. Không có kết quả khách hàng, phê duyệt/thực thi thử nghiệm hay lợi ích kinh doanh thực. [Kiểm tra 3.0 và giới hạn](../evals/book-aligned-v3.md). [Kết quả so sánh trước đây](../evals/README.md) được giữ nguyên.
