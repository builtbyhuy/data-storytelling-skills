# Minh An Office — ghi chú các bản xuất

**Toàn bộ tên và số liệu trong bộ này là giả lập.** Các bản xuất chốt ngày 07/08/2026, giờ Việt Nam. Tiền tệ là **VND nguyên đồng**, không phải nghìn đồng; tất cả số tiền không gồm VAT. Hai nhóm khách được xác định tại thời điểm lập hóa đơn: `B2B` là tài khoản doanh nghiệp, `DIRECT` là mua trực tiếp. Không có thay đổi phân loại khách trong hai tháng.

## `invoice_lines.csv` — ERP bán hàng

Một dòng là một dòng hàng đã ghi sổ trên hóa đơn. `line_id` là khóa duy nhất; `invoice_id` là số hóa đơn. `posted_date` là ngày ghi nhận doanh thu. File gồm toàn bộ hóa đơn hàng hóa ghi sổ trong tháng 6 và tháng 7/2026; không chứa hóa đơn nháp, hủy hoặc credit note.

`quantity` là số ram giấy đối với `PAPER-A4-500` và số chai mực đối với `INK-BLACK-100`. `net_revenue_vnd` là doanh thu dòng hàng sau ưu đãi trên hóa đơn và trước credit note phát sinh sau đó. `cogs_vnd` là giá vốn xuất kho được ghi sổ cho dòng hàng. Các số tiền là **tổng của dòng**, không phải đơn giá. Doanh thu hai tháng không có phí giao hàng thu của khách.

## `credit_lines.csv` — ERP điều chỉnh bán hàng

Một dòng là một dòng credit note đã ghi sổ, khóa `credit_line_id`. File bao gồm toàn bộ credit note ghi sổ trong tháng 6 và tháng 7/2026. `original_invoice_id` và `original_line_id` tham chiếu hóa đơn/dòng hàng gốc. `posted_date` là ngày ghi nhận điều chỉnh trong báo cáo tài chính.

`revenue_reduction_vnd` là số dương làm giảm doanh thu; `cogs_reversal_vnd` là số dương hoàn nhập giá vốn. `RETURN_RESELLABLE` là hàng trả đã nhập lại kho có thể bán; `returned_quantity` dùng cùng đơn vị với dòng hàng gốc. `SERVICE_ALLOWANCE` là khoản giảm trừ do dịch vụ, không có hàng trả lại và không hoàn nhập giá vốn. Các khoản này đã được duyệt; không cần ước lượng dự phòng trả hàng.

## `carrier_charges.csv` — báo cáo kết nối hãng vận chuyển

Một dòng là một khoản cước của một kiện hàng, khóa `shipment_charge_id`. Một hóa đơn bán hàng có thể được giao thành nhiều kiện. `invoice_id` là tham chiếu hóa đơn bán hàng; `charge_vnd` là cước ròng sau điều chỉnh của hãng. `shipped_date` là ngày giao cho hãng, `carrier_invoice_date` là ngày hãng xuất hóa đơn cước, và `expense_month` là tháng dịch vụ được kế toán ghi nhận, gồm cả phần trích trước cuối tháng.

Báo cáo này lấy hai kết nối `FleetB2B` và `StandardPost`; bao gồm đủ khoản cước thuộc tháng dịch vụ 6 và 7 đã được hai kết nối trả về tại ngày xuất. Các hãng không kết nối được kế toán nhận hóa đơn và ghi sổ trực tiếp. `STANDARD` và `EXPRESS` là mức dịch vụ ghi trên vận đơn. File không có thời gian giao thực tế, lý do chọn dịch vụ hay mức đáp ứng cam kết của khách.

## `monthly_finance.csv` — báo cáo tài chính quản trị đã khóa sổ

Một dòng là một tháng kế toán; `CLOSED` nghĩa là đã khóa sổ tại ngày xuất. File bao phủ toàn bộ hoạt động hàng hóa và cước giao ra của công ty, gồm cả hãng vận chuyển không có kết nối. Đây là nguồn tổng số chính thức cho KPI tháng.

`net_sales_vnd` là doanh thu hàng hóa sau mọi credit note được ghi nhận trong tháng. `net_cogs_vnd` là giá vốn sau hoàn nhập được ghi nhận trong tháng. `outbound_freight_vnd` là toàn bộ chi phí giao ra được ghi nhận cho tháng dịch vụ, bao gồm giao bổ sung và giao lại; không có chi phí vận chuyển đầu vào trong chỉ tiêu này.

**Lợi nhuận đóng góp sau giao hàng = net_sales_vnd − net_cogs_vnd − outbound_freight_vnd.** Tỷ suất lợi nhuận đóng góp dùng `net_sales_vnd` làm mẫu số. Chỉ tiêu này chưa trừ lương, thuê văn phòng và các chi phí vận hành chung; không phải lợi nhuận ròng của công ty.
