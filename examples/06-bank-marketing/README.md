# Báo cáo vận hành tiếp thị

Mở `report.html` trực tiếp bằng Chrome để đọc offline; `report.pdf` là bản độc lập 4 trang. HTML chứa toàn bộ kiểu chữ hệ thống và SVG, không tải tài nguyên qua mạng. Bảng rộng trên điện thoại có thể vuốt ngang hoặc chọn bảng bằng Tab rồi dùng phím mũi tên.

## Gói giữ lại

- `report.html`, `report.pdf`: báo cáo tiếng Việt.
- `charts/`: hai biểu đồ chính, mỗi biểu đồ có bản desktop và phone, đều là SVG có chữ thật chỉnh được.
- `evidence/calculations.json` và bốn CSV: số nguyên, tỷ lệ chưa làm tròn, đối chiếu theo lịch sử, số lần và loại liên lạc cuối.
- `evidence/browser-checks.json`, `evidence/verification.json`: các kiểm tra đã chạy, không phải chứng nhận hiểu biết hoặc hiệu quả chiến dịch.
- `source/`: năm tệp nguồn đóng băng được sao chép nguyên byte để dựng lại khi chuyển gói. CSV không bị gán nhãn hoặc viết lại. Kiểm tra hash đối chiếu với contract trước mỗi lần dựng.
- `calculate.py`, `build.py`, `render.mjs`, `verify.py`, `rebuild.ps1`: mã tính, trình bày, xuất và kiểm tra.
- `method-use.json`: xuất xứ phương pháp và hành động đã thực hiện. Không dùng tệp này làm dữ liệu báo cáo.

`history-by-attempts.csv` là kiểm tra bổ sung, không phải chính sách trần gọi. `history-by-contact.csv`: `success` là poutcome = success; `not_success` là failure + other + unknown, không có nghĩa mọi hồ sơ đã thất bại. Các nhóm campaign là 1; 2 đến 3; 4 đến 6; từ 7. Không bỏ dòng nào. Tỷ lệ tổng dùng tổng yes / tổng hồ sơ, không lấy trung bình tỷ lệ nhóm. Đơn vị là hồ sơ gốc, không phải người duy nhất. Hàng CSV tổng hợp là bản phái sinh; dữ liệu gốc không đổi.

## Dựng lại sau khi chuyển thư mục

Cần Windows, PowerShell 7.3+, Python 3.12 có pandas 3.0.1, pypdf 6.10.0 và pdfplumber 0.11.9; Node và Playwright đã cài sẵn; Chrome; Poppler (`pdftoppm.exe`). Không cần Matplotlib, font tải ngoài hoặc kết nối mạng. Không cài thêm hoặc sửa cấu hình toàn máy. Python được gọi qua launcher đã có, ví dụ Invoke-CodexPython.ps1; launcher phải chuyển tiếp các đối số Python và có chế độ UTF-8.

Đặt gói ở vị trí mới, mở PowerShell tại thư mục gói. Điền đường dẫn runtime hiện có trên máy nhận; các đường dẫn đó không nằm trong mã. `$PackageRoot` là thư mục vừa chuyển đến. Chọn một thư mục đầu ra mới để giữ nguyên bản bàn giao.

```powershell
$PackageRoot = (Get-Location).Path
$PythonLauncher = 'ĐƯỜNG_DẪN_LAUNCHER_PYTHON.ps1'
$NodeRuntime = 'ĐƯỜNG_DẪN_NODE.exe'
$NodeModules = 'THƯ_MỤC_NODE_MODULES_CÓ_PLAYWRIGHT'
$ChromeRuntime = 'ĐƯỜNG_DẪN_CHROME.exe'
$PopplerRuntime = 'THƯ_MỤC_CHỨA_PDFTOPPM.exe'
& (Join-Path $PackageRoot 'rebuild.ps1') `
  -PythonLauncher $PythonLauncher -Node $NodeRuntime -Modules $NodeModules `
  -Chrome $ChromeRuntime -PopplerBin $PopplerRuntime `
  -Source (Join-Path $PackageRoot 'source/bank-full.csv') `
  -Out (Join-Path $PackageRoot 'rebuilt')
```

Không phải thay mã khi chuyển gói. Source có thể ở vị trí khác nhưng phải kèm `source-contract.json`, `bank-names.txt`, `PROVENANCE.md`, `brief.vi.md` trong cùng thư mục. Mã từ chối hash CSV khác nguồn đóng băng này. Các đường dẫn trong HTML và giữa các tệp gói đều tương đối. SVG giữ phông Segoe UI/Arial; nếu máy nhận thiếu phông, cần kiểm tra lại cách hiển thị sau khi dựng.

Lệnh dựng xuất report.html, report.pdf, charts, evidence, source và `_inspection/` (ảnh kiểm tra tạm). So sánh `evidence/verification.json` sau khi dựng; kiểm tra trực quan bốn ảnh PDF và các trang HTML ở cả hai chiều rộng trước khi dùng bản mới. PDF có metadata thời gian tạo nên không cam kết hash PDF giống nhau giữa các lần dựng; số liệu, chữ và bố cục phải khớp. Mã nguồn và HTML đã được thử sau khi sao chép sang thư mục khác, không sửa đường dẫn trong mã.

## Giới hạn sử dụng

Đây là hồi cứu trên nguồn 2008-2010, không phải mô hình dự báo hoặc lệnh triển khai. Kiểm tra hình và tên trợ năng là kiểm tra tác giả; chưa thử với người đọc hoặc phần mềm đọc màn hình thực tế. Chưa có quyền truy cập hồ sơ vận hành, quyền gọi, danh sách hiện hành, khung giờ hay ngân sách. Việc kiểm tra 60 hồ sơ là đề xuất chẩn đoán có điều kiện, chưa được thực hiện.
