# Bản phân tích cho cuộc họp biên tập

Mở `energy-editorial.vi.html` bằng trình duyệt để đọc trên máy tính hoặc điện thoại. Tệp tự chứa, không cần mạng. `energy-editorial.vi.pdf` là bản A4 bốn trang để gửi qua email. `charts/` có ba biểu đồ SVG và ba bố cục tương ứng cho màn hình hẹp; chữ và đường biểu đồ có thể sửa trực tiếp. `previews/` chỉ là ảnh PNG xem trước của PDF.

Góc đề xuất: Việt Nam mở rộng khoảng cách tỷ trọng điện gió và mặt trời trong nhóm năm nước; tỷ trọng năm 2024 giảm nhẹ dù sản lượng tăng, vì tổng phát điện tăng nhanh hơn. Đây là mô tả lịch sử, không phải kết luận về nguyên nhân hoặc toàn ASEAN. Trang cuối có một việc giao phóng viên trong hai ngày và điều kiện để biên tập viên sử dụng kết quả.

## Kiểm tra hoặc sửa số

- `annual-calculations.csv`: 50 quan sát gộp, thành phần, mẫu số và thay đổi theo năm, giữ khóa ISO.
- `facts.json`: số liệu chuẩn dùng chung và kết quả đối chiếu.
- `calculations.vi.md`: công thức, căn cứ, giới hạn và trạng thái đề xuất.
- `source/`: CSV, hợp đồng nguồn, dấu vết tải và phương pháp Ember nguyên trạng. Tải 14/10/2026; CSV nguồn cập nhật 06/10/2026; CC BY 4.0. Phân tích/trình bày riêng, không hàm ý Ember xác nhận.

## Dựng lại ngoại tuyến

Giữ `source/` và `recipe/` cạnh nhau. Có thể chuyển cả gói sang thư mục khác. Từ thư mục chứa tệp README này, trong PowerShell 7.3 trở lên:

```powershell
& .\recipe\rebuild.ps1 -OutputDir (Join-Path $env:TEMP 'energy-editorial-rebuilt')
```

Recipe dùng runtime Codex đã có trong hồ sơ Windows và Chrome đã cài. Nếu nằm ở vị trí khác, truyền rõ các tham số; đường dẫn không bị gắn với hồ sơ người tạo:

```powershell
& .\recipe\rebuild.ps1 -PythonLauncher 'D:\runtime\Invoke-CodexPython.ps1' -NodeExe 'D:\runtime\node.exe' -ModuleDir 'D:\runtime\node_modules' -Browser 'D:\browser\chrome.exe' -OutputDir 'D:\results\energy-rebuilt'
```

Các đường dẫn trong ví dụ thứ hai cần thay bằng vị trí thực tế. Yêu cầu có sẵn Python 3.10+ (thư viện chuẩn để phân tích; `pypdf`, `pdfplumber` để kiểm tra PDF), Node 18+, Playwright và Chrome/Chromium. Không tải hoặc cài phụ thuộc khi chạy. Python launcher là script gọi Python hiện có ở chế độ UTF-8. Trên nền tảng khác, có thể chạy trực tiếp:

```text
python recipe/analyze_build.py --source source --out rebuilt
node recipe/export_web.mjs --input rebuilt/energy-editorial.vi.html --out rebuilt/previews --module-dir /actual/node_modules --browser /actual/chrome --widths 1280,390,360 --min-essential 16 --pdf /absolute/rebuilt/energy-editorial.vi.pdf
python recipe/verify_outputs.py --source source --out rebuilt --receipt rebuilt/previews/browser-export.json
```

Các bước kiểm tra SHA-256 của CSV, tính số, dựng HTML/SVG, xuất từ HTML thực bằng trình duyệt và kiểm tra nội dung/vector PDF. CSV khác bản đóng băng sẽ làm bước dựng dừng rõ ràng. Sửa nội dung/bố cục trong `recipe/analyze_build.py`; không sửa số nguồn để đạt một kết luận có sẵn.

## Những gì đã được kiểm tra trong lần bàn giao này

Đã đối chiếu khóa/phạm vi, tổng hai thành phần và mẫu số; tính lại độc lập các số quyết định; so nhãn SVG và chữ trích từ PDF với số nguồn. Đã xem các trang HTML ở 1280 px và điện thoại 360/390 px, mở bảng chi tiết bằng bàn phím, xem riêng sáu SVG và bốn trang PDF bằng bộ render PDF. PDF có chữ tìm kiếm được và đường vector, không có ảnh raster; SVG giữ các phần tử `text` và không có `image`. Các màu chữ/dữ liệu được kiểm tra tương phản với nền.

Đã chạy recipe từ một thư mục sao chép riêng: dựng HTML, SVG, tính toán, PDF và kiểm tra lại kết quả. HTML/SVG và tính toán tái tạo trùng bản bàn giao; PDF tái tạo cùng nội dung và bốn bản render trang trùng. Receipt chi tiết ở `verification.json`, `verification-claims.json`, `checks-browser.json` và `checks/`.

Các kiểm tra này chứng minh phần đã kiểm tra trên máy cục bộ. Chưa có phản hồi độc giả, duyệt biên tập, xuất bản hoặc kết quả của việc giao phóng viên. Các nguồn ngoài nêu ở trang 4 chỉ là đề xuất kiểm tra tiếp, chưa được dùng để thay dữ liệu đóng băng.
