# Dựng lại và cập nhật

Các tệp PPTX, PDF và XLSX bên cạnh thư mục này mở được ngay, không cần dựng lại. PPTX dùng chữ, bảng và ba biểu đồ PowerPoint gốc. Biểu đồ chứa workbook snapshot để sửa số trong PowerPoint. Chúng không liên kết tự động với XLSX hoặc CSV nguồn.

## Lệnh đã kiểm thử

Chuyển toàn bộ thư mục `rebuild`, bao gồm `source`, tới vị trí mới. Mở PowerShell 7.3 trở lên tại thư mục có `Build.ps1`, rồi chạy:

```powershell
pwsh -NoProfile -File ./Build.ps1 -SourceDir ./source -BuildDir ./build-06 -OutputDir ./generated-06
```

Dùng một `OutputDir` mới mỗi lần. Recipe không ghi đè snapshot đã bàn giao. Các đường dẫn nguồn/build/output tính từ thư mục làm việc hiện tại. Mã dựng nằm cạnh recipe, không phụ thuộc đường dẫn ổ đĩa ban đầu. Lệnh trên đã chạy thành công tại `work/scratch/recipe-verified` trong case này sau khi sao chép code và nguồn tới đó; thư mục kiểm thử là bản sao tạm, không phải phụ thuộc của bản bàn giao. Lệnh đã hoàn tất phân tích, tạo PPTX/XLSX, xuất PDF từ chính PPTX bằng PowerPoint và kiểm tra số. Receipt trong `receipts/handoff-verification.json` ghi lệnh, thư mục làm việc và hash của các tệp đã bàn giao.

## Runtime cần có

Windows, PowerShell 7.3+, PowerPoint và Excel desktop có COM, Arial. Node 24 với `@oai/artifact-tool`, bộ helper presentations và Python có `openpyxl`, `pypdf`, `pypdfium2`. Phiên bản đã chạy: Codex runtime 26.1009.11318, Python 3.12.14. Không cần LibreOffice, tài khoản đám mây hay cài thêm gói.

Recipe tìm bundle Codex theo thư mục hồ sơ của người chạy và tìm helper presentations đã cài. Nếu vị trí khác, cung cấp đường dẫn runtime sẵn có:

```powershell
pwsh -NoProfile -File ./Build.ps1 -SourceDir ./source -BuildDir ./build-02 -OutputDir ./generated-02 -NodeExe "D:/runtime/node.exe" -NodeModules "D:/runtime/node_modules" -PythonExe "D:/runtime/python.exe" -PythonLauncher "D:/tools/Invoke-CodexPython.ps1" -PresentationSkill "D:/skills/presentations"
```

Các đường dẫn `D:/...` là ví dụ cấu hình, không phải phụ thuộc cố định. Có thể bỏ `PythonLauncher` nếu không có launcher Codex, khi đó recipe gọi trực tiếp Python đã cung cấp với UTF-8. Trong môi trường Codex hiện tại, launcher được gọi như script với `-B`. Có thể lấy vị trí chính xác bằng công cụ `load_workspace_dependencies`; không thay PATH, locale hay execution policy. Recipe dừng nếu thiếu khả năng cần thiết. Đây là recipe đã kiểm thử trên runtime ghi trên, không cam kết tương thích mọi bản artifact-tool hay nền tảng khác.

Junction `node_modules` tồn tại tạm tại thư mục recipe trong lúc chạy. Recipe chỉ xóa entry mà nó tạo, không xóa hay đi vào thư mục dependency dùng chung. Nếu đã có entry, recipe dừng để tránh thay dữ liệu của người khác.

## Luồng tính và phạm vi cập nhật

`source/raw/absence-geographic-autumn.csv` giữ nguyên byte tải DfE. `cohort-config.json` xác định toàn bộ Local Authority và hai nhóm trường, hai kỳ thu. `analyze.py` đọc raw, kiểm tra khóa, trường số được dùng, PA chứa severe, tổng buổi vắng bằng có phép cộng không phép, và đối chiếu tổng địa bàn với dòng National riêng của từng nhóm/kỳ. `build.mjs` dùng `facts.json` cho mọi số trên slide, ghi workbook với công thức và nhãn. `office-check.ps1` mở chính tệp, xuất PDF và render, sửa một bản PPTX riêng để kiểm tra số biểu đồ/chữ/kích thước qua lưu-mở lại, và thay/khôi phục đầu vào Excel để kiểm tra tính lại. `verify.py` tính lại tỷ lệ bằng Decimal từ raw, đối chiếu 304 dòng tính Excel và quét lỗi công thức, kiểm tra PDF chín trang.

XLSX có `Tong hop` cho các bảng dùng trong slide và trần nguồn lực, `Dia ban` cho toàn bộ 304 so sánh, `Nguon` cho số đếm và nguồn. Tỷ lệ dùng tổng tử số chia tổng mẫu số. PA và severe dùng lượt ghi danh, lý do và tổng vắng dùng buổi có thể tham dự. Giữ riêng hai cặp địa bàn–nhóm không có dòng, không thêm số 0. Không dùng source `Total` chứa special. Số 10% đến dưới 50% vẫn là lượt ghi danh, chưa là số trẻ hoặc gia đình duy nhất.

Workbook giữ công thức từ số đếm với độ chính xác đầy đủ. Snapshot biểu đồ PowerPoint làm tròn tỷ lệ dạng 0–1 tới 6 chữ số thập phân để Excel giữ được số, tương đương 0,0001 điểm phần trăm. Nhãn vẫn hiển thị hai chữ số phần trăm như bảng. Sai số hình học nhỏ hơn 0,00005 điểm phần trăm, thấp hơn độ phân giải nhãn. Sau khi sửa số trong PowerPoint, kiểm tra lại nhãn, mẫu số và định dạng phần trăm trước xuất PDF.

Kiểm tra sửa biểu đồ đã lưu giá trị mới trong workbook nhúng và đồng bộ series từ các ô mới, rồi lưu/mở lại bản PPTX riêng. Chưa xác nhận tự động làm mới cache biểu đồ khi chỉ sửa ô qua COM. Khi đổi dữ liệu nguồn, cách đã kiểm thử là dựng lại cả bộ bằng recipe. Không sắp xếp riêng vùng đầu vào hoặc thêm dòng trực tiếp mà không xem lại các tham chiếu. Không có cam kết cập nhật tự động sau sửa mọi cấu trúc hoặc mọi kỳ.

Các receipt giữ riêng kiểm tra cấu trúc, kiểm tra số và thao tác Office. Bộ kiểm tra bố cục có một cảnh báo ước lượng chiều cao bảng ở slide 7; bản render PowerPoint và trang PDF tương ứng đã được xem trực tiếp, bảng và câu bên dưới không chồng nhau. Không có kiểm thử với người đọc thực tế hoặc chứng nhận khả năng tiếp cận toàn diện.

Recipe tái tạo snapshot hiện tại. Khi DfE sửa nguồn, giữ bản raw/receipt/hash mới riêng, đọc release status và phương pháp. Kiểm tra số dòng, mã mới/cũ, tên địa bàn, nhóm trường, trường all-through, độ tuổi 5–15, mẫu số, ký hiệu x/z, mã lý do và độ dài kỳ. Xem lại lựa chọn địa bàn và nội dung khuyến nghị. Mã sẽ dừng nếu thứ hạng làm cơ sở cho lựa chọn hiện tại thay đổi. Bản sửa cùng cấu trúc và cùng kỳ vẫn cần xem lại mọi kết quả và render trước bàn giao.

Thay kỳ không chỉ đổi nhãn: bộ dựng hiện khóa hai kỳ 202425/202526 và dừng khi khác. Phải rà lại mã lý do, mẫu số và coverage, cập nhật công thức/nhãn/narrative và xem lại shortlist trước khi bỏ khóa. `rebuild-source-extract.py` gốc được giữ để có thể trích lại với `--config`, `--source`, `--output-dir` sau khi người phụ trách đã rà cấu hình. Không có lịch công bố tương lai được xác nhận và không có tự động tải/cập nhật nền.

## Điều kiện tại địa phương trước quyết định

Đề xuất vẫn chưa duyệt, chưa triển khai và chưa đo kết quả. Giám đốc dịch vụ giữ quyền quyết định. Nhóm hợp tác xác nhận trường phù hợp và cam kết thời gian, đầu mối địa phương. Quản lý ngân sách và giám đốc xác nhận bốn người được phân công cho học kỳ, đi lại/công cụ, quyền truy cập và trần chi. Đội hỗ trợ xác nhận tiếp nhận, bảo vệ trẻ em, tuyến chuyển tiếp, sự tham gia của gia đình và danh sách khử trùng lặp. Người phụ trách đo chốt cửa sổ baseline/theo dõi, nhóm so sánh, tiêu chí giảm tối thiểu có ý nghĩa và thời điểm trường xác nhận dữ liệu. Thiếu điều kiện thì hoãn hoặc sửa phạm vi.

Đối chiếu trước/sau trên cohort đầy đủ chỉ là tín hiệu để quyết định thử tiếp, chưa chứng minh tác động nhân quả. Quy mô tối đa 60 gia đình đồng thời không suy ra tổng gia đình học kỳ, số buổi khôi phục, tiết kiệm hay hiệu quả. Không có các kết quả này trong dữ liệu DfE.

Nguồn: Department for Education, Pupil absence in schools in England, Autumn term 2025/26, công bố 6/8/2026, bản tải 13/10/2026. Contains public sector information licensed under the Open Government Licence v3.0. Phép tính và giải thích tiếng Việt của bản bàn giao này không ngụ ý DfE bảo chứng.
