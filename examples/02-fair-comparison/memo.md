# Báo cáo sales: sửa kết luận về coaching

**Quyết định đề xuất:** chưa nhân rộng coaching của B cho A từ CSV này. Trưởng nhóm nên thiết kế một phép thử có đối chứng trước khi quyết định triển khai đại trà.

## Câu kết luận có thể dùng ngay

> Trong dữ liệu được cung cấp, B chốt 36/80 lead (45%), A chốt 24/80 lead (30%). Tỷ lệ gộp của B cao hơn A 15 điểm phần trăm, tương đương cao hơn 50% so với A. Tuy nhiên, B có 75% lead High, A có 25%; trong cả High và Low, B đều thấp hơn A 5 điểm phần trăm. Khi tính với cùng cơ cấu 50% High và 50% Low, B đạt 35%, A đạt 40%. CSV không có thời gian quan sát hoặc cách phân coaching, nên chưa xác định được hiệu quả của coaching. Đề xuất thử nghiệm có đối chứng trong A trước khi nhân rộng coaching của B.

## Cơ sở so sánh

| Cơ sở | A | B | B trừ A |
|---|---:|---:|---:|
| Gộp theo cơ cấu thực tế | 24/80 = 30% | 36/80 = 45% | +15 điểm %; +50% tương đối |
| High | 12/20 = 60% | 33/60 = 55% | -5 điểm % |
| Low | 12/60 = 20% | 3/20 = 15% | -5 điểm % |
| Cơ cấu chung 50/50 | 0,5 × 60% + 0,5 × 20% = 40% | 0,5 × 55% + 0,5 × 15% = 35% | -5 điểm % |

50/50 lấy từ tổng 80 High và 80 Low. Tỷ lệ chuẩn hóa là phép so sánh tính lại, không phải số chốt mới quan sát. Với mọi cơ cấu High/Low chung, chênh lệch vẫn là -5 điểm %.

## Việc trưởng nhóm nên quyết tiếp theo

- Đề xuất phân ngẫu nhiên nhân sự đủ điều kiện trong A vào coaching của B và đối chứng; cân bằng High/Low, tránh coaching lan giữa hai nhóm.
- Chốt trước số mẫu, cửa sổ quan sát đủ thời gian chốt, ngưỡng cải thiện tối thiểu, chi phí và quy tắc dừng/kéo dài. CSV không cho căn cứ để ấn định số tuần hay số mẫu.
- Đo tỷ lệ chốt theo tier và theo cùng cơ cấu; đánh giá độ bất định theo cách phân nhóm. Chỉ nhân rộng khi lợi ích đạt ngưỡng với độ bất định chấp nhận được.

Không có dữ liệu trước/sau, thời gian, phân coaching, định nghĩa tier hoặc khác biệt còn lại trong từng tier. Không thể suy ra coaching của A tốt hơn hay coaching của B có hại. Thử nghiệm là đề xuất, chưa thực hiện.

**Nguồn:** data.csv, 4 dòng, 160 lead. Dữ liệu giả lập phục vụ học tập, không phải kết quả khách hàng. Tính toán chính xác: calculations.json; dựng lại: rebuild.py.
