# “Tăng 50%” chưa chứng minh coaching có hiệu quả

[PDF một trang](brief.pdf) · [SVG sửa được](brief.svg) · [Câu kết luận sửa và memo](memo.md) · [Phép tính chính xác](calculations.json)

![Báo cáo sửa so sánh tỷ lệ gộp với cùng cơ cấu lead, giữ mẫu số và giới hạn nhân quả](brief.png)

## Yêu cầu mẫu

Đưa [data.csv](data.csv) và yêu cầu:

> Báo cáo sales đang kết luận: “Coaching của B làm tỷ lệ chốt tăng 50%, nên triển khai cho A.” Kiểm kết luận từ CSV, sửa cách so sánh và đưa ra việc trưởng nhóm nên quyết tiếp theo. Làm tài liệu một trang đẹp, rõ, dùng được trong cuộc họp mà không cần nghe thuyết minh mới hiểu. Giữ những số đúng, cho thấy cơ sở so sánh và giới hạn bằng chứng. Không có thông tin thêm về thời gian hoặc cách phân coaching ngoài CSV.

A 24/80 = 30%; B 36/80 = 45%. Chênh lệch15 điểm phần trăm tương đương 50% so với A, nhưng không phải hiệu quả coaching. B có nhiều lead High hơn; trong từng tier B đều thấp hơn 5 điểm. Cơ cấu chung 50/50 lấy từ 80 High và 80 Low của 160 lead: A 40%, B 35%. Đây là so sánh mô tả, không phải số thắng mới hoặc hiệu quả nhân quả.

**Việc cần quyết:** chuẩn bị phép thử coaching có đối chứng, chốt trước mẫu, cửa sổ, ngưỡng, chi phí và quy tắc dừng. Chưa nhân rộng từ dữ liệu này. Không có bằng chứng coaching của A tốt hơn hoặc B có hại; nhãn High/Low chưa được định nghĩa.

## Tái tạo

```text
python examples/02-fair-comparison/rebuild.py --output ./scratch/comparison-v3
```

[Dependencies và giới hạn](../README.md). Script dùng exact fractions, kiểm tỷ lệ/mẫu số và từ chối thay đổi bốn dòng trước khi xem lại narrative.

Ví dụ giả lập. Lượt thực thi mới dùng redteam, chart và narrative 3.0 từ input gốc; bản công bố sửa thêm thuật ngữ và cách đặt việc cần quyết theo reviewer chỉ đọc pixels. Không có thử nghiệm đã làm, khách hàng hoặc chứng minh vượt baseline.
