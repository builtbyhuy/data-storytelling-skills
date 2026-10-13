# Nguồn DfE và phạm vi sử dụng

Source: Department for Education, *Pupil absence in schools in England — Autumn term 2025/26*, dataset **Absence by geographic level - autumn term**, công bố **6 August 2026**, tải **13 October 2026**.

- [Catalogue và metadata](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/407a4c0a-260f-4bd0-8b6d-0f49febb207c).
- [CSV chính thức](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/407a4c0a-260f-4bd0-8b6d-0f49febb207c/csv).
- [Release](https://explore-education-statistics.service.gov.uk/find-statistics/pupil-absence-in-schools-in-england/2025-26-autumn-term/explore).
- [Phương pháp](https://explore-education-statistics.service.gov.uk/methodology/pupil-absence-statistics-methodology).
- [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

Contains public sector information licensed under the Open Government Licence v3.0. Phép tính và giải thích tiếng Việt là phần thực hiện của ví dụ độc lập này; DfE không bảo chứng dự án hay đề xuất.

`rebuild/source/raw/absence-geographic-autumn.csv` giữ đủ 6.182.665 byte tải xuống, SHA-256 `8adc8086fcb3dea7d201087e370165de95ab60f98d422ece6d52d825a98440ff`, 11.254 bản ghi. Cấu hình chọn England, Local Authority, state-funded primary/secondary, Autumn term 2024/25 và 2025/26: 608 dòng, 304 cặp địa phương–nhóm và 153 mã địa phương. Hai nhóm có 152 địa phương mỗi nhóm nhưng không cùng tập mã: Scilly-primary và City-of-London-secondary không có dòng, không được thêm thành số 0.

Vắng thường xuyên ≥10% và vắng nặng ≥50% dùng mẫu số lượt ghi danh; vắng nặng nằm trong vắng thường xuyên. Tỷ lệ buổi vắng/lý do dùng số buổi nửa ngày có thể tham dự. Tổng hợp dùng tổng tử số chia tổng mẫu số. Lượt ghi danh có thể lặp do chuyển trường, không phải trẻ hay gia đình duy nhất. Dữ liệu học kỳ mang tính chỉ báo; bản năm đầy đủ mới cho góc nhìn dứt khoát. Không dùng Total có special hoặc suy ra nhu cầu, khả năng tham gia, nguyên nhân cá nhân hay hiệu quả dịch vụ từ các tỷ lệ này.

[Schema nguyên bản](rebuild/source/source-schema.md) giữ định nghĩa chi tiết. Nó nhắc HTML phương pháp được lưu riêng; các URL trên là đường đọc công khai. HTML website, HTTP/provenance đầy đủ và runtime receipts được giữ trong hồ sơ riêng, không phân phối logo/asset website hay đường dẫn máy. Chúng không phải dependency của recipe; [manifest công bố](PUBLICATION.json) giữ nguồn, hash, phạm vi và kết quả kiểm tra thiết yếu.
