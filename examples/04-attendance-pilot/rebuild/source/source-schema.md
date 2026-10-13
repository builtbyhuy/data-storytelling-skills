# Nguồn, phạm vi và đơn vị

Nguồn là **Department for Education (DfE), Pupil absence in schools in England — Autumn term 2025/26**, bộ **Absence by geographic level - autumn term**. Trang công bố và catalogue ghi ngày công bố/cập nhật **6/8/2026**, trạng thái **Accredited official statistics**; đây là bản mới nhất của bộ dữ liệu khi lấy ngày 13/10/2026. Không có cờ final/provisional riêng cho từng dòng. Số liệu mới nhất của bài là **học kỳ thu 2025**, không phải quan sát đang diễn ra tháng 10/2026.

Tệp tải nguyên bản chứa 11.254 dòng ở nhiều năm, cấp địa lý và nhóm trường. Phạm vi đã đăng ký trước khi tải tệp: học kỳ thu của **2024/25 và 2025/26**, mọi Local Authority của England trong nguồn, chỉ `State-funded primary` và `State-funded secondary`. Có **153 mã Local Authority khác nhau**, **304 cặp địa bàn–nhóm trường được nguồn cung cấp**, và **608 dòng nguồn cho hai kỳ**. Mỗi nhóm có 152 dòng trong một kỳ, nhưng hai tập địa bàn không hoàn toàn giống nhau. Nguồn không có dòng `State-funded primary` của **Isles of Scilly (E06000053)** và không có dòng `State-funded secondary` của **City of London (E09000001)** ở cả hai kỳ. Những cặp này được ghi trong manifest, không thêm thành dòng số 0; không suy ra tỷ lệ hay caseload từ một dòng không tồn tại.

Bản trích có **304 dòng so sánh**; mọi cặp thực sự có trong nguồn đều khớp qua hai kỳ, không có đổi tên/mã/vùng trong các trường nhận diện đã kiểm tra. Không lựa chọn địa bàn theo mức cao/thấp. Có 40 dòng National/Regional của đúng hai nhóm/kỳ này, để riêng làm bối cảnh. Phạm vi dịch vụ trong brief là hai loại trường; sự vắng mặt của một cặp ở dữ liệu không tự chứng minh nhu cầu bằng 0 hoặc xác nhận một đối tác đủ điều kiện tại địa bàn đó.

## Các tệp đầu vào

- `raw/absence-geographic-autumn.csv`: CSV chính thức, giữ nguyên byte, gồm cả dữ liệu ngoài phạm vi. Không sửa hay bù số trong tệp này.
- `authority-phase-cohort.csv`: bản trích thuận tiện, mỗi dòng có khóa `new_la_code` và `education_phase`. Mọi trường nguồn khác được giữ dưới dạng chuỗi với hậu tố `__202425` hoặc `__202526`; không làm tròn lại. `source_row_present__...` chỉ là cờ có dòng nguồn, không phải chỉ tiêu vắng học.
- `published-context.csv`: các dòng National/Regional ở đúng hai nhóm/kỳ; không cộng lại với Local Authority.
- `source-extract-manifest.json`: số dòng, hash, vị trí dòng nguồn, dấu thiếu/not applicable, kiểm tra khóa và thay đổi nhận diện.
- `cohort-config.json`, `rebuild-source-extract.py`: bộ lọc và cách trích lại bằng đường dẫn tương đối hoặc `--config`, `--source`, `--output-dir`; không phân tích hay đề xuất địa bàn.
- `provenance-receipt.json`: URL, thời gian, byte/hash, phạm vi, nguồn định nghĩa và giấy phép.
- Các HTML trong `raw/`: trang catalogue, release/data guidance, phương pháp và chính sách giấy phép đã tải để đối chiếu.

## Khái niệm và mẫu số

| Trường hoặc nhóm trường | Nghĩa và đơn vị |
| --- | --- |
| `time_period`, `time_identifier` | Mã năm học `202425`/`202526`; luôn là `Autumn term` trong phạm vi này, không phải cả năm học |
| `geographic_level`, `new_la_code`, `old_la_code`, `la_name`, `region_code`, `region_name` | Cấp địa lý, mã và nhãn của nguồn; dùng mã mới để ghép, giữ cả mã cũ/tên/vùng mỗi kỳ |
| `education_phase` | Phân loại trường của DfE, không chỉ là nhóm tuổi; trường all-through được xếp vào nhóm secondary trong phương pháp |
| `num_schools` | Số trường trong tập hợp nguồn |
| `enrolments` | **Lượt ghi danh**, không phải số trẻ duy nhất hay số gia đình |
| `sess_possible` | Số buổi có thể tham dự; một session bằng **nửa ngày học** |
| `sess_overall`, `sess_authorised`, `sess_unauthorised` | Số session vắng tổng/có phép/không phép; tổng gồm hai nhóm sau |
| `sess_overall_percent`, `sess_authorised_percent`, `sess_unauthorised_percent` | % **session có thể tham dự**, không phải % trẻ vắng học |
| `enrolments_pa_10_exact`, `enrolments_pa_10_exact_percent` | Lượt ghi danh vắng ít nhất 10% session riêng của lượt đó, và % trên tổng enrolments |
| `enrolments_pa_50_exact`, `enrolments_pa_50_exact_percent` | Lượt ghi danh vắng ít nhất 50% session riêng của lượt đó, và % trên tổng enrolments |
| `sess_auth_*`, `sess_unauth_*` | Số session được ghi theo từng lý do; không phải số trẻ có lý do đó |
| Các trường `*_rate` theo lý do | % trên **sess_possible**; không mặc nhiên là tỷ trọng của session vắng |
| `sess_y_exceptional`, `sess_q_la_arrangements` và mã đặc biệt | Các mã theo định nghĩa nguồn; không tự cộng vào session vắng đã công bố |

Các chỉ tiêu chính áp dụng cho tuổi **5–15 tại ngày 31/8 đầu năm học**. DfE tính và công bố theo enrolment: trẻ chuyển trường có thể có hơn một lượt ghi danh. Lượt ghi danh ngắn vẫn có thể đạt ngưỡng vắng cao; không suy ra mức độ của từng trẻ từ tổng cấp địa bàn. Severe absence nằm trong persistent absence theo ngưỡng, không phải nhóm tách rời để cộng hai số thành caseload duy nhất. Địa lý/tập hợp trường trong nguồn không tự xác nhận nơi cư trú, vùng phục vụ của một đối tác hay danh sách gia đình sẵn sàng tham gia.

Source `Total` bao gồm primary, secondary **và special**, nên không đồng nghĩa với phạm vi hai nhóm của bài. Không cộng các dòng Local Authority, Regional và National như các quan sát độc lập. Khi ghép hoặc tổng hợp, giữ rõ nhóm trường và mẫu số thích hợp; tỷ lệ session và tỷ lệ enrolment dùng hai mẫu số khác nhau.

## Quy ước, so sánh và tình trạng dữ liệu

Data guidance ghi không áp dụng suppression cho bộ dữ liệu này; số tỷ lệ trong thông cáo thường hiển thị hai chữ số thập phân, file nguồn có độ chính xác cao hơn. Quy ước `x` = chưa có dữ liệu, `z` = không áp dụng. Tập hợp đã chọn có **3.648 ô `z`** và không có `x`; những ký hiệu này được giữ nguyên, không đổi thành 0. Tỷ lệ lưu bằng chuỗi thập phân, có thể có phần đuôi biểu diễn số thực; các trường/kỳ không luôn dùng cùng số chữ số thập phân. Không suy ra độ chính xác thực tế hơn nguồn cho phép.

Cả hai kỳ so sánh đều là autumn và đều sau thay đổi mã từ tháng 9/2024. Mã authorised holiday cũ không còn dùng từ thời điểm đó; extended holiday và COVID cũng có lịch sử riêng. Từ autumn 2024, nguồn yêu cầu ghi lý do cho mọi absence; exceptional circumstance Y được tách và có thêm Q. Không coi mã không áp dụng là số trường hợp bằng 0; nếu mở rộng về kỳ trước phải đọc lại thay đổi mã/mẫu số. Độ dài kỳ, số possible sessions và số enrolments có thể khác nhau dù cùng mùa; dữ liệu không theo dõi cùng một nhóm trẻ qua hai kỳ.

**Lưu ý của DfE ([phương pháp, mục 1.8 “Termly publications”](https://explore-education-statistics.service.gov.uk/methodology/pupil-absence-statistics-methodology)):** số liệu vắng học theo học kỳ chỉ mang tính chỉ báo, có thể chịu ảnh hưởng đáng kể của độ dài kỳ và cần diễn giải thận trọng; chỉ bản công bố cả năm mới cho cái nhìn có tính kết luận về tình hình vắng học.

Phương pháp chính thức được lưu ở `raw/methodology.html`, cập nhật **26/3/2026**. Nó giải thích kiểm tra và loại dữ liệu đầu nguồn, dual registration và chuyển đổi academy; đó là xử lý của DfE, không phải bù thiếu của người chuẩn bị. Không có thông tin chương trình hỗ trợ, chi phí, partner capacity, hoàn cảnh hay căn nguyên của từng gia đình trong tập hợp này. Ký hiệu reason do nhà trường ghi không chứng minh một cơ chế nhân quả hay hiệu quả can thiệp.

## Tái sử dụng và cập nhật

[Catalogue dữ liệu chính thức](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/407a4c0a-260f-4bd0-8b6d-0f49febb207c), [GOV.UK terms](https://www.gov.uk/help/terms-conditions) và [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) đã được kiểm tra từ trang thật. Dữ liệu công khai và ví dụ dẫn xuất có ghi nguồn có thể sao chép/sửa/phân phối, kể cả trên GitHub. Không ngụ ý DfE bảo chứng, không suy ra quyền dùng riêng logo hoặc tài sản của bên thứ ba.

Ghi nhận: “Nguồn: Department for Education, Pupil absence in schools in England — Autumn term 2025/26, công bố 6/8/2026, bản tải 13/10/2026. Contains public sector information licensed under the Open Government Licence v3.0. Phép tính và giải thích tiếng Việt do nhóm thực hiện.”

Không có lịch công bố tương lai được xác nhận trong bộ biên nhận này. Khi có bản công bố hoặc bản sửa mới, lưu snapshot/hash mới, đọc status/guidance, kiểm tra mã/tên/phạm vi và thay đổi mẫu số/mã absence. Xác nhận kỳ mới trước khi sửa cấu hình, giữ riêng những khóa không khớp, rồi dựng lại các tổng hợp và cả ba tệp đầu ra cần cập nhật. Không chỉ đổi nhãn năm hoặc ghi đè tệp gốc dùng cho bản đã bàn giao.
