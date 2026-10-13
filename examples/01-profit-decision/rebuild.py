"""Rebuild the synthetic Minh An Office handoff from the five untouched input files.

Run with the bundled Windows Python launcher, -B, and this script path.
No network calls. Requires existing reportlab, xlsxwriter, pypdf, and Poppler.
"""
from pathlib import Path
from collections import defaultdict, Counter
import argparse, csv, hashlib, json, time, subprocess, shutil, math
from datetime import datetime, timezone
from xml.sax.saxutils import escape
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE
START = time.perf_counter()
STAMP = datetime.now(timezone.utc).isoformat()
parser = argparse.ArgumentParser()
parser.add_argument('--inputs', type=Path, default=ROOT/'inputs')
parser.add_argument('--output', type=Path, default=HERE)
args = parser.parse_args()
INPUT = args.inputs.resolve()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
files = ['invoice_lines.csv','credit_lines.csv','carrier_charges.csv','monthly_finance.csv','source-notes.md']
hashes = {f:hashlib.sha256((INPUT/f).read_bytes()).hexdigest() for f in files}
EXPECTED_HASHES = {
 'invoice_lines.csv':'ac2f746936beb2780e3967f07774cfd1ca5a88ee91002b481cf5b24bfd2b89e8',
 'credit_lines.csv':'843ff693ee472d17130e5b1a1e9c7d8d87685215a4de9cf0ab25a628df2e4bc4',
 'carrier_charges.csv':'672a36715f6e729e6fff990e7b437867f884fb1f6c5cd6b8d74468d621d3e590',
 'monthly_finance.csv':'78a6cedf342d4fdd024dc91d3dd218999bf5fd851ec38b25b8adacba075e1a92',
 'source-notes.md':'783003e731b21246c3a8e81cc54173941a6f4475455c276e9248499775b60fbd'}
if hashes != EXPECTED_HASHES:
    raise ValueError('This memo is bound to the supplied synthetic snapshot. Changed input requires claim/decision review; refusing to regenerate a stale narrative. The workbook formulas remain editable.')
raw = {f[:-4]:list(csv.DictReader((INPUT/f).open(encoding='utf-8-sig',newline=''))) for f in files if f.endswith('.csv')}
L,C,S,F = [raw[k] for k in ['invoice_lines','credit_lines','carrier_charges','monthly_finance']]
checks=[]
def check(name, condition, detail=''):
    checks.append({'check':name,'passed':bool(condition),'detail':detail})
    if not condition: raise AssertionError(name+': '+detail)
for rows,key in [(L,'line_id'),(C,'credit_line_id'),(S,'shipment_charge_id'),(F,'accounting_month')]:
    check('unique_'+key, len({r[key] for r in rows}) == len(rows))
check('required_cells_present',all(all(v is not None and v!='' for v in r.values()) for rows in [L,C,S,F] for r in rows))
lines={r['line_id']:r for r in L}
invoices={r['invoice_id']:r for r in L}
check('credit_references_valid',all(r['original_line_id'] in lines and lines[r['original_line_id']]['invoice_id']==r['original_invoice_id'] for r in C))
check('shipment_references_valid',all(r['invoice_id'] in invoices for r in S))
check('invoice_attributes_consistent',all(len({(r['posted_date'],r['customer_segment'],r['customer_id']) for r in L if r['invoice_id']==i})==1 for i in invoices))
periods=sorted(r['accounting_month'] for r in F)
groups=defaultdict(Counter)
products=defaultdict(Counter)
invoice_sets=defaultdict(set)
for r in L:
    m=r['posted_date'][:7]; seg=r['customer_segment']; p=r['sku']
    invoice_sets[m,seg].add(r['invoice_id'])
    for dest,src in [('invoice_revenue','net_revenue_vnd'),('invoice_cogs','cogs_vnd')]:
        groups[m,seg][dest]+=int(r[src]); products[m,seg,p][dest]+=int(r[src])
    products[m,seg,p]['invoice_quantity']+=int(r['quantity'])
for r in C:
    orig=lines[r['original_line_id']];m=r['posted_date'][:7];seg=orig['customer_segment'];p=orig['sku']
    for dest,src in [('credits','revenue_reduction_vnd'),('cogs_reversals','cogs_reversal_vnd')]:
        groups[m,seg][dest]+=int(r[src]);products[m,seg,p][dest]+=int(r[src])
for r in S:
    groups[r['expense_month'],invoices[r['invoice_id']]['customer_segment']]['connected_freight']+=int(r['charge_vnd'])
for (m,seg),a in groups.items():
    a['net_sales']=a['invoice_revenue']-a['credits'];a['net_cogs']=a['invoice_cogs']-a['cogs_reversals']
    a['gross_profit']=a['net_sales']-a['net_cogs'];a['partial_contribution']=a['gross_profit']-a['connected_freight']
    a['invoice_count']=len(invoice_sets[m,seg])
finance={}
for r in F:
    m=r['accounting_month'];a={k:int(r[k+'_vnd']) for k in ['net_sales','net_cogs','outbound_freight']}
    a['gross_profit']=a['net_sales']-a['net_cogs'];a['contribution']=a['gross_profit']-a['outbound_freight']
    a['margin']=a['contribution']/a['net_sales'];a['gross_margin']=a['gross_profit']/a['net_sales']
    a['connected_freight']=sum(g['connected_freight'] for (month,seg),g in groups.items() if month==m)
    a['unallocated_freight']=a['outbound_freight']-a['connected_freight'];finance[m]=a
    check('sales_reconcile_'+m,sum(g['net_sales'] for (month,seg),g in groups.items() if month==m)==a['net_sales'])
    check('cogs_reconcile_'+m,sum(g['net_cogs'] for (month,seg),g in groups.items() if month==m)==a['net_cogs'])
    check('freight_gap_nonnegative_'+m,a['unallocated_freight']>=0)
    check('finance_closed_'+m,r['close_status']=='CLOSED')
m0,m1=periods
d={k:finance[m1][k]-finance[m0][k] for k in ['net_sales','net_cogs','gross_profit','outbound_freight','contribution','connected_freight','unallocated_freight']}
d['sales_percent']=d['net_sales']/finance[m0]['net_sales']*100
d['contribution_percent']=d['contribution']/finance[m0]['contribution']*100
d['margin_pp']=(finance[m1]['margin']-finance[m0]['margin'])*100
check('contribution_bridge',finance[m0]['contribution']+d['gross_profit']-d['outbound_freight']==finance[m1]['contribution'])
check('segment_bridge',sum(groups[m1,s]['partial_contribution']-groups[m0,s]['partial_contribution'] for s in ['B2B','DIRECT'])-d['unallocated_freight']==d['contribution'])
services=[]
for m in periods:
    for seg in ['B2B','DIRECT']:
        for svc in ['STANDARD','EXPRESS']:
            rows=[r for r in S if r['expense_month']==m and invoices[r['invoice_id']]['customer_segment']==seg and r['service']==svc]
            if rows:
                n=len({r['invoice_id'] for r in rows});v=sum(int(r['charge_vnd']) for r in rows)
                services.append({'month':m,'segment':seg,'service':svc,'charges':len(rows),'invoices':n,'freight_vnd':v,'freight_per_invoice_vnd':v/n})
cross=sum(1 for r in C if r['posted_date'][:7]!=lines[r['original_line_id']]['posted_date'][:7])
late=sum(1 for r in S if r['carrier_invoice_date'][:7]!=r['expense_month'])
cross_credit=sum(int(r['revenue_reduction_vnd']) for r in C if r['posted_date'][:7]!=lines[r['original_line_id']]['posted_date'][:7])
product_rows=[]
for (m,seg,p),a in sorted(products.items()):
    product_rows.append({'month':m,'segment':seg,'sku':p,**dict(a),'invoice_realized_price':a['invoice_revenue']/a['invoice_quantity']})
definitions={
 'status':'All names and data synthetic; proposal not approved or executed.',
 'snapshot':'2026-08-07; Vietnam time; June and July 2026 closed accounting periods.',
 'currency':'Whole VND, excluding VAT. Display in million VND where explicitly labeled.',
 'authority':'monthly_finance.csv governs whole-company monthly KPI; invoice and credit postings reconcile sales/COGS; connected carrier export covers only two carriers.',
 'grain':'Invoice line is unique by line_id; credits by credit_line_id; charges by shipment_charge_id. Aggregate each additive source before joining totals.',
 'contribution':'net_sales - net_cogs - outbound_freight; not net company profit; excludes overhead.',
 'credits':'Use credit posted month for monthly P&L; original line supplies segment only. July includes credits on June invoices.',
 'freight':'Use expense_month, not carrier_invoice_date or invoice posted month.',
 'segment_contribution':'Gross profit minus connected freight ONLY; unconnected freight is not assigned by an invented rule.',
 'price':'Invoice realized revenue / invoice quantity, before later credits; no list price or discount rule in the input.',
 'causality':'Descriptive comparison, no causal intervention effect or recoverable savings established.'}
analysis={'synthetic':True,'snapshot':definitions['snapshot'],'source_hashes_sha256':hashes,'row_counts':{k:len(v) for k,v in raw.items()},'definitions':definitions,'finance':finance,'change':d,'display':{'july_contribution_million':finance[m1]['contribution']/1e6,'june_contribution_million':finance[m0]['contribution']/1e6,'contribution_change_million':d['contribution']/1e6,'gross_profit_change_million':d['gross_profit']/1e6,'freight_change_million':d['outbound_freight']/1e6,'july_gap_million':finance[m1]['unallocated_freight']/1e6},'segments':[{'month':m,'segment':s,**dict(a)} for (m,s),a in sorted(groups.items())],'products':product_rows,'services':services,'coverage':{'unallocated_july_vnd':finance[m1]['unallocated_freight'],'july_connected_share':finance[m1]['connected_freight']/finance[m1]['outbound_freight'],'credit_cross_month_rows':cross,'credit_cross_month_reduction_vnd':cross_credit,'carrier_invoice_month_differs_rows':late},'sensitivity':{'B2B_change_if_all_gap_allocated_to_B2B_vnd':groups[m1,'B2B']['partial_contribution']-groups[m0,'B2B']['partial_contribution']-d['unallocated_freight'],'unallocated_does_not_prove_group_loss':True},'checks':checks}
(OUT/'analysis.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2),encoding='utf-8')

def vn(v, decimals=2): return f'{v:,.{decimals}f}'.replace(',','X').replace('.',',').replace('X','.')
def million(v):return vn(v/1_000_000)

memo='''# Minh An Office - Bản ghi nhớ quyết định\n\n**Toàn bộ tên và số liệu giả lập. Đề xuất, chưa phê duyệt hoặc thực hiện.**\n\n**Chọn thử thay đổi giao hàng có giới hạn trước.** Giữ bán B2B trong phạm vi hiện tại; đối soát cước còn thiếu và kiểm tra cam kết giao trước khi đổi EXPRESS sang STANDARD. Chưa đủ bằng chứng để giảm toàn bộ B2B hoặc kết luận ưu đãi gây ra mức giảm.\n\nDoanh thu thuần tháng 6 → tháng 7/2026 tăng **156,70 → 200,80 triệu VND** (+44,10 triệu; +28,1%). Lãi gộp tăng **43,85 → 46,65 triệu**, nhưng cước giao ra tăng **8,85 → 15,70 triệu**. Vì thế lợi nhuận đóng góp sau giao hàng giảm **35,00 → 30,95 triệu** (-4,05 triệu; -11,6%). Tỷ suất giảm **22,34% → 15,41%** (-6,92 điểm phần trăm). Chỉ tiêu chưa trừ chi phí chung.\n\n| Phần đóng góp theo tháng ghi sổ, triệu VND | T6 | T7 | Chênh |\n|---|---:|---:|---:|\n| B2B, sau cước đã kết nối | 18,90 | 20,70 | +1,80 |\n| DIRECT, sau cước đã kết nối | 16,10 | 13,25 | -2,85 |\n| Trừ cước ngoài kết nối chưa gán nhóm | 0,00 | -3,00 | -3,00 |\n| Tổng chính thức | 35,00 | 30,95 | -4,05 |\n\n**Giới hạn quyết định:** 3,00 triệu cước tháng 7 (19,1% tổng cước) chưa phân bổ theo nhóm. Nếu toàn bộ khoản này thuộc B2B, thay đổi đóng góp của B2B sẽ là -1,20 triệu thay vì +1,80 triệu. Đây là phép thử nhạy cảm, không phải phân bổ đã xác nhận. Không kết luận B2B tốt hơn DIRECT hoặc giải thích toàn bộ mức giảm bằng EXPRESS.\n\nTrong phần cước kết nối tháng 7, B2B EXPRESS là **5,10 triệu trên 60 hóa đơn** (85.000 VND/hóa đơn); STANDARD là **6,00 triệu trên 100 hóa đơn** (60.000 VND/hóa đơn). Hai nhóm khác nhau, chưa có trọng lượng, tuyến đường, lý do chọn dịch vụ hoặc thời gian giao thực tế; chênh 25.000 VND không phải khoản tiết kiệm có thể thu hồi chắc chắn.\n\nGiá thực thu trên dòng hóa đơn B2B giảm từ 50.000 xuống 48.000 VND/ram giấy và từ 300.000 xuống 290.000 VND/chai mực. Không có bảng giá hoặc điều kiện ưu đãi nên chưa tách được giá, khuyến mãi và cơ cấu khách. Lãi gộp B2B vẫn tăng 24,90 → 31,80 triệu; DIRECT giảm 18,95 → 14,85 triệu.\n\n**Quyết tại cuộc họp:** duyệt nguyên tắc một thử nghiệm giao STANDARD cho các yêu cầu B2B có cam kết cho phép, cùng một nhóm giữ hiện trạng; chốt người phụ trách, ngân sách và tiêu chí trước khi bắt đầu. Ưu đãi giữ nguyên trong thử nghiệm để dễ đọc kết quả. Nếu đối soát tìm ra cước giao lại hoặc hãng ngoài kết nối là nguyên nhân ưu tiên, đổi phạm vi thử trước khi triển khai.\n\nĐề xuất: chủ doanh nghiệp phê duyệt và quyết giữ/dừng; phụ trách giao hàng thực hiện; kế toán làm chủ định nghĩa và đối soát. Bốn tuần nhận tối đa 60 yêu cầu hợp lệ, ngừng nhận khi hết hạn hoặc chạm giới hạn 1 triệu VND chi phí tăng thêm. Dừng sớm khi thay đổi dịch vụ làm trễ cam kết. Đọc đóng góp trên **mọi yêu cầu đã phân nhóm**, cả đơn hủy/từ chối, sau credit và toàn bộ cước. Cuối tuần 4 dừng nhận và chưa mở rộng nếu kết quả chưa chốt. Tổng kết khi đơn cuối được theo dõi tối thiểu 14 ngày và kế toán xác nhận dữ liệu đủ; 14 ngày không bảo đảm mọi trả hàng đã phát sinh.\n\nNguồn: bản xuất chốt 07/08/2026; monthly_finance.csv là nguồn tổng số; dòng hóa đơn và credit theo ngày ghi sổ; cước theo expense_month. Bản tính và định nghĩa ở analysis.xlsx / analysis.json; cách thử và quy tắc ở test-plan.md; trạng thái ở decision-record.csv.\n'''
(OUT/'memo.md').write_text(memo,encoding='utf-8')

plan='''# Thử bốn tuần - thay đổi giao hàng B2B\n\n**Ví dụ giả lập. Toàn bộ vai trò, giới hạn, lịch và ngưỡng dưới đây là đề xuất; chưa có phê duyệt, phân nhóm, triển khai hoặc kết quả.** T0 là thứ Hai sau khi chủ doanh nghiệp phê duyệt; chưa ấn định ngày. Không tự kéo dài thử nghiệm khi thiếu dữ liệu.\n\n## Quyết định và điều kiện mở thử\n\nThử STANDARD thay cho EXPRESS khi cam kết khách cho phép. Không đổi ưu đãi đồng thời. Kế toán phải phân bổ hoặc giải thích 3.000.000 VND cước ngoài kết nối tháng 7, xác nhận nguồn từng hóa đơn/cước và ghi những phần vẫn không gán được. Nếu phần đối soát chỉ ra giao lại, tách kiện hoặc hãng ngoài kết nối là vấn đề khác, chủ doanh nghiệp quyết lại phạm vi trước khi mở thử; không xem thí điểm EXPRESS là lời giải đã được chứng minh.\n\nKhông mở thử nếu chưa có báo giá STANDARD cho đúng tuyến/kiện, thời hạn giao cam kết của khách, người chịu trách nhiệm theo dõi, khả năng lấy đủ dữ liệu và giới hạn rủi ro được duyệt. Các điều kiện này chưa nằm trong bộ xuất.\n\n## Thiết kế và giới hạn đề xuất\n\n- Đơn vị phân nhóm: tài khoản B2B, để một khách không nhận hai chính sách gây lẫn. Ghép cặp tài khoản tương đương về giá trị đơn, cơ cấu hàng, tuyến, trọng lượng/kiện và hạn giao; bốc thăm một tài khoản sang STANDARD, một giữ hiện trạng. Lưu hạt giống, nhóm và lý do đủ điều kiện trước khi biết kết quả. Không chọn các đơn dễ sau khi thử bắt đầu.\n- Chỉ nhận yêu cầu mà cả hai cách giao đều có khả năng đáp ứng cam kết và có giá cước xác nhận; loại yêu cầu gấp bắt buộc EXPRESS trước phân nhóm, lưu lý do loại. Tối đa 20 tài khoản, 60 yêu cầu hợp lệ tổng cả hai nhóm trong bốn tuần; đạt giới hạn thì dừng nhận. Đó là trần rủi ro đề xuất, không phải mẫu đã chứng minh đủ lực thống kê.\n- Dự toán thời gian: vận hành tối đa 2 giờ/tuần cho xác minh, phân nhóm và ghi nhận; kế toán tối đa 2 giờ/tuần đối soát. Đây là giới hạn cần xác nhận, chưa biết năng lực nhân sự. Chạm giới hạn thì dừng nhận thêm thay vì bỏ ghi nhận.\n- Tổng chi phí tăng thêm do thử tối đa 1.000.000 VND, gồm cước tăng thêm, bồi hoàn và công làm thêm thực trả; không có ngân sách được cấp trong dữ liệu. Chủ doanh nghiệp xác nhận trần trước khi triển khai. Ghi riêng thời gian làm việc, kể cả thời gian không tạo khoản chi.\n- Dừng chuyển dịch vụ ngay khi có một đơn trễ cam kết do chuyển sang STANDARD, khi chất lượng/cam kết không được bảo đảm, vượt trần chi phí, hoặc thiếu dữ liệu khiến không kiểm soát được rủi ro. Trở lại quy trình cũ cho yêu cầu mới; không xóa các yêu cầu đã phân nhóm khỏi mẫu. Dừng thử không có nghĩa số liệu kết quả đã chốt.\n\n## Lịch công việc\n\n| Thời điểm | Việc và người phụ trách đề xuất | Điểm kiểm tra |\n|---|---|---|\n| Trước T0 | Chủ DN quyết phạm vi/ngân sách; kế toán đối soát 3 triệu và chốt định nghĩa; vận hành kiểm tra SLA, giá, tuyến và lập cặp khách | Không mở thử khi điều kiện còn thiếu |\n| Tuần 1 | Vận hành phân nhóm, lưu mọi yêu cầu và ngoại lệ; kế toán kiểm tra liên kết credit/cước | Chủ DN duyệt các sai lệch; xem rủi ro hằng ngày |\n| Tuần 2 | Tiếp tục trong trần; đọc chi phí và cam kết, chưa tuyên bố hiệu quả | Không thay tiêu chí theo kết quả sớm |\n| Tuần 3 | Kiểm tra thực thi, dữ liệu thiếu và thời gian nhân sự | Thiếu nguồn trọng yếu thì dừng nhận; kế toán nêu ngày có thể bổ sung |\n| Tuần 4 | Kết thúc nhận yêu cầu vào hết ngày Chủ nhật T0+27; chủ DN quyết dừng nhận/giữ phạm vi cũ | Không mở rộng dựa trên đơn hoàn tất sớm |\n| Sau tuần 4 | Theo dõi toàn bộ nhóm, tối thiểu 14 ngày sau yêu cầu cuối; kế toán chốt toàn bộ cước/credit và tháng cuối | Đọc vào ngày muộn hơn của kết thúc theo dõi và xác nhận khóa nguồn. Không tự coi 14 ngày là đủ mọi trả hàng |\n\nNếu dữ liệu chưa chốt 7 ngày sau cửa sổ theo dõi tối thiểu, chủ DN quyết đóng thử với trạng thái **chưa kết luận**, ghi phần thiếu và chỉ duyệt bổ sung nếu cần. Không tiếp tục thử hoặc chi quá trần để chờ kết quả. Số liệu kế toán khóa tháng có thể tới sau ngày này; ghi là theo dõi bổ sung được đề xuất, không dời điểm dừng vận hành.\n\n## Định nghĩa và người giữ số liệu\n\n| Chỉ số / nguồn | Định nghĩa dùng lại | Người giữ số liệu / nhịp |\n|---|---|---|\n| Đóng góp công ty theo tháng | Doanh thu thuần - giá vốn thuần - toàn bộ cước giao ra; VND nguyên, chưa trừ chi phí chung. Finance đã khóa sổ là tổng chính thức | Kế toán; cập nhật sau khóa sổ, xác nhận ngày chốt thực tế |\n| Kết quả chính của thử | Tổng doanh thu ghi nhận từ các yêu cầu đã phân nhóm, trừ mọi credit liên quan, giá vốn sau hoàn nhập, mọi cước và chi phí tiền mặt tăng thêm của thử, chia **tất cả yêu cầu đủ điều kiện đã phân nhóm** | Kế toán; lưu request_id → invoice_id → credit/shipment. Đơn hủy/từ chối không có doanh thu vẫn ở mẫu; ghi chi phí thực tế |\n| Cam kết giao | Số yêu cầu giao trễ hạn hứa ban đầu / tất cả yêu cầu phân nhóm; đơn chưa hoàn tất là chưa quan sát, không xem là đúng hạn | Vận hành; kiểm tra hằng ngày, lưu promised_at / delivered_at / lý do |\n| Thực thi và nguồn thiếu | Số yêu cầu đúng chính sách / số đã phân nhóm; số thiếu liên kết, cước chưa xác nhận, credit còn chờ | Vận hành + kế toán; cập nhật hằng tuần |\n| Tác dụng lên nhu cầu | Yêu cầu, chấp nhận, hủy/từ chối và doanh thu trên tài khoản được phân nhóm | Kinh doanh cung cấp, kế toán kiểm tra; không chỉ nhìn hóa đơn đã bán |\n\nBốn nguồn CSV hiện tại không có yêu cầu hủy/từ chối, tuyến/trọng lượng, thời gian giao, hạn hứa, giờ nhân sự, ngân sách hoặc bảng giá ưu đãi. Cần bổ sung các trường này khi được duyệt; không giả định dữ liệu đã tồn tại. Tolerance đối soát VND: 0 đồng cho tổng khóa sổ; mọi sai lệch phải có dòng giải thích, không âm thầm bỏ qua. Chủ DN duyệt thay đổi định nghĩa; kế toán cập nhật phiên bản và ảnh chụp nguồn.\n\n## Cách đọc và quyết sau thử\n\nTrước khi mở thử, chốt mức cải thiện tối thiểu đề xuất **5.000 VND đóng góp/yêu cầu** so với nhóm giữ hiện trạng, sau chi phí tăng thêm. Đây là ngưỡng kinh doanh đề xuất, không phải mức tác động dự báo. Chọn vì cần một phần chênh lệch thực dụng thay vì mở rộng vì tăng vài đồng; chủ DN có thể thay trước thử theo chi phí vận hành thực tế.\n\nBáo cáo chênh lệch trung bình trên yêu cầu với số yêu cầu/tài khoản mỗi nhóm, tổng đóng góp, tổng chi phí, tỷ lệ trễ và hủy/từ chối, số liệu thiếu và sai lệch cơ cấu. Giữ phân nhóm ban đầu khi phân tích, kể cả chuyển lại EXPRESS do ngoại lệ. Kiểm tra kết quả theo từng cặp khách; nếu tổng tăng chỉ do một tài khoản lớn hoặc cơ cấu lệch thì kết luận có điều kiện.\n\n**Đề xuất tiếp tục trong phạm vi nhỏ** nếu chênh lệch ≥5.000 VND/yêu cầu, không có trễ cam kết do đổi dịch vụ, không vượt trần, nguồn đủ và không thấy tác hại nhu cầu. **Dừng/điều chỉnh** nếu tác hại hoặc chi phí vượt trần; **chưa kết luận** nếu thiếu dữ liệu, chênh lệch nhỏ hoặc không nhất quán. Một mẫu tối đa 20 tài khoản chưa có kiểm định/lực thống kê; không tuyên bố tác động toàn bộ B2B. Chỉ quyết mở rộng sau một phép thử lớn hơn được duyệt hoặc bằng chứng bổ sung phù hợp.\n\nTrong cuộc họp, ghi riêng: người đọc có nêu được lựa chọn và giới hạn không; chủ DN đã quyết gì; vận hành có thực hiện đúng không; kết quả trưởng thành và tác hại là gì. Không dùng việc tạo PDF, ký quyết định hoặc thực hiện đúng quy trình làm bằng chứng lợi nhuận đã tăng. Dùng decision-record.csv để cập nhật các trạng thái; giữ ảnh chụp nguồn và lịch sử thay đổi cần thiết.\n'''
(OUT/'test-plan.md').write_text(plan,encoding='utf-8')
records=[
 {'record_id':'SYN-ANALYSIS-01','synthetic':'TRUE','question':'Vì sao doanh thu tháng 7 tăng nhưng đóng góp giảm?','evidence_snapshot':'07/08/2026; 5 nguồn; SHA256 trong analysis.json','proposal':'Thử thay đổi giao hàng có giới hạn; đối soát 3 triệu chưa gán nhóm','evidence_completed':'Đã đối soát sales/COGS, tính bridge +2,80 -6,85 = -4,05 triệu','decision_owner_proposed':'Chủ doanh nghiệp','metric_steward_proposed':'Kế toán','executor_proposed':'Phụ trách giao hàng','approval_state':'CHUA_PHE_DUYET','actual_decision':'CHUA_QUAN_SAT','execution_state':'CHUA_THUC_HIEN','eligible_scope':'Tối đa 20 tài khoản / 60 yêu cầu B2B; SLA cho phép STANDARD','window':'4 tuần từ T0 chưa ấn định; dừng nhận T0+27','comparison':'Phân nhóm theo cặp tài khoản; STANDARD vs hiện trạng','outcome':'Đóng góp/yêu cầu sau mọi credit, cước và chi phí tăng thêm','guardrails':'1 triệu chi phí tăng thêm; dừng khi trễ cam kết do thay đổi; 2h/tuần/vai trò','mature_readout':'Muộn hơn: yêu cầu cuối +14 ngày và kế toán xác nhận đủ cước/credit; chưa biết ngày','observed_result':'CHUA_QUAN_SAT','decision_rule_proposed':'>=5.000 VND/yêu cầu, đủ nguồn, không hại SLA/nhu cầu; chỉ tiếp tục nhỏ','next_step':'Chủ DN chốt người/trần; kế toán phân bổ 3 triệu; vận hành xác minh cam kết','reader_understanding':'CHUA_CO_PHAN_HOI_NGUOI_DOC'},
 {'record_id':'SYN-DATA-02','synthetic':'TRUE','question':'Cước ngoài kết nối tháng 7 thuộc nhóm/hoạt động nào?','evidence_snapshot':'Finance 15,70 triệu - carrier export 12,70 triệu','proposal':'Lấy hóa đơn hãng ngoài kết nối, liên kết đơn và lý do giao lại','evidence_completed':'Đã tính chênh lệch 3.000.000 VND; chưa có nguồn để phân bổ','decision_owner_proposed':'Chủ doanh nghiệp','metric_steward_proposed':'Kế toán','executor_proposed':'Kế toán','approval_state':'CHUA_PHE_DUYET','actual_decision':'CHUA_QUAN_SAT','execution_state':'CHUA_THUC_HIEN','eligible_scope':'Toàn bộ cước giao ra tháng dịch vụ 7/2026','window':'Trước T0; ngày chưa ấn định','comparison':'Đối soát với tổng khóa sổ, tolerance 0 VND hoặc giải thích riêng','outcome':'Số tiền gán được nhóm và cước chưa gán','guardrails':'Không chia tỷ lệ doanh thu để giả tạo số chính xác','mature_readout':'Khi kế toán xác nhận nguồn đủ; chưa có ngày','observed_result':'CHUA_QUAN_SAT','decision_rule_proposed':'Nếu nguyên nhân ưu tiên khác EXPRESS thì xét lại phạm vi trước mở thử','next_step':'Kế toán yêu cầu nguồn nội bộ sau khi chủ DN phê duyệt','reader_understanding':'CHUA_CO_PHAN_HOI_NGUOI_DOC'}]
with (OUT/'decision-record.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)

# Workbook keeps additive grains separate and includes live formulas plus cached values.
wb=xlsxwriter.Workbook(OUT/'analysis.xlsx')
wb.set_properties({'title':'Minh An Office - dữ liệu giả lập','comments':'Proposal only; no observed business impact.'})
fmt_head=wb.add_format({'bold':True,'bg_color':'#E9EDF0','font_color':'#192F40','text_wrap':True,'border':0})
fmt_int=wb.add_format({'num_format':'#,##0;[Red](#,##0)'})
fmt_pct=wb.add_format({'num_format':'0.00%'})
fmt_title=wb.add_format({'bold':True,'font_size':16,'font_color':'#192F40'})
fmt_wrap=wb.add_format({'text_wrap':True,'valign':'top'})
numfields={'quantity','net_revenue_vnd','cogs_vnd','returned_quantity','revenue_reduction_vnd','cogs_reversal_vnd','charge_vnd','net_sales_vnd','net_cogs_vnd','outbound_freight_vnd'}
def rawsheet(name,rows,extra):
    sh=wb.add_worksheet(name);keys=list(rows[0])+list(extra)
    sh.write_row(0,0,keys,fmt_head);sh.freeze_panes(1,0);sh.set_row(0,32);sh.set_column(0,len(keys)-1,19)
    for idx,r in enumerate(rows,1):
        for col,k in enumerate(keys):
            val=r[k] if k in r else extra[k](r)
            if k in numfields:sh.write_number(idx,col,int(val),fmt_int)
            else:sh.write(idx,col,val)
    sh.autofilter(0,0,len(rows),len(keys)-1)
    return sh
rawsheet('Invoice',L,{'posted_month':lambda r:r['posted_date'][:7]})
rawsheet('Credit',C,{'posted_month':lambda r:r['posted_date'][:7],'segment':lambda r:lines[r['original_line_id']]['customer_segment'],'sku':lambda r:lines[r['original_line_id']]['sku']})
rawsheet('Carrier',S,{'segment':lambda r:invoices[r['invoice_id']]['customer_segment']})
rawsheet('Finance',F,{})
summary=wb.add_worksheet('Summary');summary.write(0,0,'Minh An Office - giả lập, VND nguyên đồng',fmt_title)
summary.activate()
headers=['Tháng','DT hóa đơn','Credit theo ngày ghi sổ','Doanh thu thuần','GV hóa đơn','Hoàn GV','Giá vốn thuần','Lãi gộp','Cước kết nối','Cước toàn công ty','Cước chưa gán nhóm','Đóng góp chính thức','Tỷ suất','Sai lệch DT','Sai lệch GV']
summary.write_row(2,0,headers,fmt_head);summary.set_row(2,43);summary.freeze_panes(3,1);summary.set_column(0,0,12);summary.set_column(1,14,18)
for idx,m in enumerate(periods,3):
    a=finance[m];rr=idx+1;fr=idx-1
    summary.write(idx,0,m)
    vals=[sum(g['invoice_revenue'] for (mm,s),g in groups.items() if mm==m),sum(g['credits'] for (mm,s),g in groups.items() if mm==m),a['net_sales'],sum(g['invoice_cogs'] for (mm,s),g in groups.items() if mm==m),sum(g['cogs_reversals'] for (mm,s),g in groups.items() if mm==m),a['net_cogs'],a['gross_profit'],a['connected_freight'],a['outbound_freight'],a['unallocated_freight'],a['contribution'],a['margin'],0,0]
    formulas=[f'SUMIF(Invoice!J:J,A{rr},Invoice!H:H)',f'SUMIF(Credit!I:I,A{rr},Credit!G:G)',f'B{rr}-C{rr}',f'SUMIF(Invoice!J:J,A{rr},Invoice!I:I)',f'SUMIF(Credit!I:I,A{rr},Credit!H:H)',f'E{rr}-F{rr}',f'D{rr}-G{rr}',f'SUMIF(Carrier!E:E,A{rr},Carrier!H:H)',f'Finance!D{fr}',f'J{rr}-I{rr}',f'H{rr}-J{rr}',f'L{rr}/D{rr}',f'D{rr}-Finance!B{fr}',f'G{rr}-Finance!C{fr}']
    for col,(form,val) in enumerate(zip(formulas,vals),1):summary.write_formula(idx,col,'='+form,fmt_pct if col==12 else fmt_int,val)
summary.write(7,0,'Tổng số: Finance khóa sổ. Credit dùng tháng ghi sổ; cước dùng expense_month. Cước thiếu không chia tỷ lệ doanh thu.',fmt_wrap)
summary.merge_range(7,0,8,10,'Tổng số: Finance khóa sổ. Credit dùng tháng ghi sổ; cước dùng expense_month. Cước thiếu không chia tỷ lệ doanh thu.',fmt_wrap)
segsh=wb.add_worksheet('Segments');segsh.set_column(0,1,14);segsh.set_column(2,7,23);segsh.freeze_panes(1,2)
segsh.write_row(0,0,['Tháng','Nhóm','Số hóa đơn','DT thuần','GV thuần','Lãi gộp','Cước kết nối','Đóng góp SAU CƯỚC KẾT NỐI'],fmt_head);segsh.set_row(0,40)
for i,((m,s),a) in enumerate(sorted(groups.items()),1):
    rr=i+1;segsh.write_row(i,0,[m,s,a['invoice_count']])
    fs=[f'SUMIFS(Invoice!H:H,Invoice!J:J,A{rr},Invoice!E:E,B{rr})-SUMIFS(Credit!G:G,Credit!I:I,A{rr},Credit!J:J,B{rr})',f'SUMIFS(Invoice!I:I,Invoice!J:J,A{rr},Invoice!E:E,B{rr})-SUMIFS(Credit!H:H,Credit!I:I,A{rr},Credit!J:J,B{rr})',f'D{rr}-E{rr}',f'SUMIFS(Carrier!H:H,Carrier!E:E,A{rr},Carrier!I:I,B{rr})',f'F{rr}-G{rr}']
    for c,(form,key) in enumerate(zip(fs,['net_sales','net_cogs','gross_profit','connected_freight','partial_contribution']),3):segsh.write_formula(i,c,'='+form,fmt_int,a[key])
price=wb.add_worksheet('Price');price.write_row(0,0,['Tháng','Nhóm','SKU','SL hóa đơn','DT hóa đơn','Giá thực thu/đơn vị, trước credit'],fmt_head);price.set_row(0,42);price.set_column(0,1,14);price.set_column(2,2,22);price.set_column(3,5,25)
for i,r in enumerate(product_rows,1):
    rr=i+1;price.write_row(i,0,[r['month'],r['segment'],r['sku']])
    for col,(source,val) in enumerate([('G',r['invoice_quantity']),('H',r['invoice_revenue'])],3):price.write_formula(i,col,f'=SUMIFS(Invoice!{source}:{source},Invoice!J:J,A{rr},Invoice!E:E,B{rr},Invoice!F:F,C{rr})',fmt_int,val)
    price.write_formula(i,5,f'=E{rr}/D{rr}',fmt_int,r['invoice_realized_price'])
defs=wb.add_worksheet('Definitions');defs.set_column(0,0,25);defs.set_column(1,1,110);defs.write_row(0,0,['Mục','Định nghĩa / SHA256'],fmt_head)
for i,(k,v) in enumerate(list(definitions.items())+list(hashes.items()),1):defs.write(i,0,k);defs.write(i,1,v,fmt_wrap);defs.set_row(i,42)
log=wb.add_worksheet('Decision_log');log.write_row(0,0,list(records[0]),fmt_head);log.set_column(0,len(records[0])-1,28);log.set_row(0,45);log.freeze_panes(1,1)
for i,r in enumerate(records,1):log.write_row(i,0,list(r.values()),fmt_wrap);log.set_row(i,150)
wb.close()

# A single editable drawing specification produces both PDF and text-based SVG.
FONT=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('ArialLocal',str(FONT/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialBoldLocal',str(FONT/'arialbd.ttf')))
W,H=595.276,841.890
INK='#192F40';MUTED='#4C606D';ACCENT='#9B432A';GREEN='#24644E';PALE='#F1F3F3';WHITE='#FFFFFF';RULE='#B9C3C8'
c=canvas.Canvas(str(OUT/'brief.pdf'),pagesize=(W,H))
c.setTitle('Minh An Office - ghi nhớ quyết định - DỮ LIỆU GIẢ LẬP')
c.setAuthor('Synthetic analytical handoff')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="595.276pt" height="841.890pt" viewBox="0 0 595.276 841.890">',
     '<title>Thử giao hàng trước, giữ bán B2B có điều kiện - dữ liệu giả lập</title>',
     '<desc>Toàn công ty tháng 6 đến tháng 7 năm 2026: đóng góp 35,00 triệu cộng tăng lãi gộp 2,80 triệu trừ tăng cước 6,85 triệu còn 30,95 triệu. B2B tăng 1,80 triệu sau cước kết nối, nhưng 3,00 triệu cước chưa gán nhóm có thể đổi kết luận. Thử STANDARD có giới hạn, chưa phê duyệt. Bảng chính xác và nguồn tính nằm trong analysis.xlsx và analysis.json.</desc>']
boxes=[]
def rect(x,y,w,h,color):
    c.setFillColor(HexColor(color));c.rect(x,H-y-h,w,h,fill=1,stroke=0)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
def line(x1,y1,x2,y2,color=RULE,width=.65,dash=None):
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,H-y1,x2,H-y2);c.setDash([])
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash[0]},{dash[1]}"' if dash else '')+'/>')
def text(x,y,s,size=10,color=INK,bold=False,align='left'):
    f='ArialBoldLocal' if bold else 'ArialLocal';c.setFont(f,size);c.setFillColor(HexColor(color))
    width=pdfmetrics.stringWidth(s,f,size);tx=x-width/2 if align=='center' else x-width if align=='right' else x
    c.drawString(tx,H-y,s)
    svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="'+{'left':'start','center':'middle','right':'end'}[align]+'">'+escape(s)+'</text>')
    boxes.append((tx,y-size,width,size,s))
    check('text_within_page_'+str(len(boxes)),tx>=20 and tx+width<=W-20 and y-size>=15 and y<=H-15,s)
def para(x,y,s,width,size=10,leading=14,color=INK,bold=False):
    font='ArialBoldLocal' if bold else 'ArialLocal';words=s.split();linebuf='';count=0
    for word in words:
        candidate=(linebuf+' '+word).strip()
        if pdfmetrics.stringWidth(candidate,font,size)>width and linebuf:
            text(x,y+count*leading,linebuf,size,color,bold);count+=1;linebuf=word
        else:linebuf=candidate
    if linebuf:text(x,y+count*leading,linebuf,size,color,bold);count+=1
    return y+count*leading
rect(0,0,W,H,WHITE)
text(36,37,'MINH AN OFFICE',9.5,INK,True)
text(W-36,37,'DỮ LIỆU GIẢ LẬP  /  07.08.2026',8.4,MUTED,False,'right')
line(36,49,W-36,49,INK,1)
text(36,88,'Thử đổi giao hàng trước,',24,INK,True)
text(36,119,'giữ bán B2B có điều kiện',24,INK,True)
para(36,145,'Doanh thu tăng 156,70 → 200,80 triệu VND, nhưng đóng góp sau giao hàng giảm. Chọn thử có giới hạn; chưa đủ căn cứ để cắt B2B hay quy mức giảm cho ưu đãi.',W-72,10.5,15)

text(36,203,'Cước tăng vượt phần lãi gộp tăng',14.5,INK,True)
text(36,222,'Toàn công ty · tháng 6 → tháng 7/2026 · triệu VND',9.2,MUTED)
baseline=395;scale=3.3;topval=lambda v:baseline-v*scale
for tick in [0,20,40]:
    yy=topval(tick);line(64,yy,W-36,yy,RULE,.45)
    text(52,yy+3,str(tick),8.5,MUTED,False,'right')
positions=[112,239,366,493];bw=60
bridge=[('Đóng góp T6',0,35,INK,'35,00'),('Lãi gộp tăng',35,37.8,GREEN,'+2,80'),('Cước tăng',30.95,37.8,ACCENT,'-6,85'),('Đóng góp T7',0,30.95,INK,'30,95')]
for idx,(label,lo,hi,color,value) in enumerate(bridge):
    x=positions[idx];rect(x-bw/2,topval(hi),bw,(hi-lo)*scale,color)
    text(x,topval(hi)-10,value,11.8,color,True,'center')
    text(x,414,label,9.3,INK,False,'center')
for i,v in [(0,35),(1,37.8),(2,30.95)]:line(positions[i]+bw/2,topval(v),positions[i+1]-bw/2,topval(v),MUTED,.7,[3,3])
text(36,438,'Đóng góp giảm 4,05 triệu (-11,6%); chưa trừ chi phí chung.',9.8,MUTED)

text(36,477,'B2B chưa đủ căn cứ để cắt giảm',14.5,INK,True)
text(36,495,'Đóng góp sau cước đã xác định nhóm, triệu VND',9.2,MUTED)
cols=[36,370,453,W-36]
text(cols[1],516,'T6',9,MUTED,True,'right');text(cols[2],516,'T7',9,MUTED,True,'right');text(cols[3],516,'Thay đổi',9,MUTED,True,'right')
line(36,523,W-36,523)
for yy,name,a,b,diff in [(540,'B2B','18,90','20,70','+1,80'),(560,'DIRECT','16,10','13,25','-2,85'),(580,'Trừ cước chưa gán nhóm','0,00','-3,00','-3,00'),(600,'Tổng công ty','35,00','30,95','-4,05')]:
    text(36,yy,name,10.3,INK,name in ['B2B','Tổng công ty']);text(cols[1],yy,a,10.3,INK,False,'right');text(cols[2],yy,b,10.3,INK,False,'right');text(cols[3],yy,diff,10.3,INK,True,'right')
para(36,619,'Cước tháng 7 còn 3,00 triệu chưa gán nhóm. Nếu đều thuộc B2B, mức thay đổi của B2B là -1,20 triệu. Đó chưa phải toàn bộ đóng góp nhóm.',W-72,9.8,14,ACCENT)

line(36,652,W-36,652,INK,.8)
text(36,676,'QUYẾT TẠI CUỘC HỌP',10,INK,True)
para(36,696,'Đề xuất thử 4 tuần với đơn B2B có hạn giao phù hợp giao tiêu chuẩn, cùng nhóm giữ hiện trạng. Chỉ mở sau đối soát 3 triệu cước và xác nhận hạn giao.',W-72,10.3,14)
text(36,740,'Ai chịu trách nhiệm',9.2,INK,True)
para(36,755,'Chủ DN duyệt/giữ/dừng; giao hàng thực hiện; kế toán chốt nguồn. Vai trò là đề xuất. Tối đa 60 yêu cầu đặt hàng đủ điều kiện; trần chi phí thêm 1 triệu.',238,9.1,12.4,MUTED)
text(310,740,'Giới hạn và cách đọc',9.2,INK,True)
para(310,755,'Dừng khi đổi dịch vụ làm trễ cam kết. Chỉ giữ thử nhỏ nếu đóng góp tăng ≥5.000 VND/yêu cầu đặt hàng, sau đủ giảm trừ, cước và chi phí thử; không hại nhu cầu.',W-346,9.1,12.4,MUTED)
text(36,812,'Đề xuất chưa phê duyệt. Đọc sau yêu cầu cuối ≥14 ngày và nguồn đủ; xem test-plan.md.',8.2,MUTED)
text(36,826,'Nguồn: tài chính khóa sổ; hóa đơn và giảm trừ theo ngày ghi sổ; cước theo tháng dịch vụ.',8.2,MUTED)
c.showPage();c.save();svg.append('</svg>')
(OUT/'brief.svg').write_text('\n'.join(svg),encoding='utf-8')

poppler=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
if not poppler.exists():
    detected=shutil.which('pdftoppm')
    if not detected:raise RuntimeError('Existing Poppler is unavailable; no dependency will be installed.')
    poppler=Path(detected)
subprocess.run([str(poppler),'-r','150','-singlefile','-png',str(OUT/'brief.pdf'),str(OUT/'brief')],check=True,capture_output=True)
pdf=PdfReader(OUT/'brief.pdf');check('pdf_one_page',len(pdf.pages)==1)
pdftext=pdf.pages[0].extract_text()
for needle in ['35,00','+2,80','-6,85','30,95','3,00','-1,20','DỮ LIỆU GIẢ LẬP','chưa phê duyệt']:
    check('pdf_text_'+needle,needle in pdftext)
check('raw_sources_unchanged',hashes=={f:hashlib.sha256((INPUT/f).read_bytes()).hexdigest() for f in files})
def luminance(color):
    vals=[int(color[i:i+2],16)/255 for i in [1,3,5]]
    v=[a/12.92 if a<=.04045 else ((a+.055)/1.055)**2.4 for a in vals]
    return .2126*v[0]+.7152*v[1]+.0722*v[2]
contrast={color:(luminance(WHITE)+.05)/(luminance(color)+.05) for color in [INK,MUTED,ACCENT,GREEN]}
check('essential_text_contrast_4.5',min(contrast.values())>=4.5,str(contrast))
check('essential_chart_mark_contrast_3',min(contrast.values())>=3)
analysis['checks']=checks;analysis['contrast_ratios_on_white']=contrast
(OUT/'analysis.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(OUT),'finance':finance,'change':d,'checks_passed':len(checks)},ensure_ascii=False,indent=2))
