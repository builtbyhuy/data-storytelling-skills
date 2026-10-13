"""Rebuild the supplied synthetic invoice/payment reconciliation and one-page brief.

Run with an available Python runtime:
  python examples/03-join-audit/rebuild.py --output ./scratch/join-v3
Optional: --inputs PATH --output PATH --audit-helper PATH --poppler PATH
Dependencies: bundled reportlab, pypdf, Pillow; Windows Arial; bundled Poppler.
No source mutation, network, account changes, installation, or publication.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, shutil, subprocess, sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
from PIL import Image

HERE = Path(__file__).resolve().parent
DEFAULT_SKILLS = HERE.parents[1] / 'skills'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--inputs', type=Path, default=HERE / 'inputs')
parser.add_argument('--output', type=Path, default=HERE)
parser.add_argument('--audit-helper', type=Path, default=DEFAULT_SKILLS / 'business-insight-diagnosis/scripts/join_audit.py')
parser.add_argument('--poppler', type=Path, default=Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
args = parser.parse_args()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
INPUT = args.inputs.resolve()
checks = []
def check(name, ok, evidence=None):
    checks.append({'check': name, 'pass': bool(ok), 'evidence': evidence})
    if not ok: raise AssertionError(name)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def fmt(value): return f'{Decimal(value):.2f}'
def vn(value): return f'{int(Decimal(value)):,}'.replace(',', '.')
def read_csv(path, required):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        check(path.name + ': exact columns', reader.fieldnames == required, reader.fieldnames)
        rows = list(reader)
    check(path.name + ': complete records', all(None not in r and all(v is not None and v.strip() for v in r.values()) for r in rows))
    return rows
def sum_field(rows, name): return sum((Decimal(r[name]) for r in rows), Decimal(0))

source_paths = [INPUT / n for n in ['invoice-lines.csv', 'payment-allocations.csv', 'source-notes.md']]
source_hashes = {p.name: digest(p) for p in source_paths}
lines = read_csv(source_paths[0], ['invoice_id','line_id','item','net_amount_usd'])
payments = read_csv(source_paths[1], ['invoice_id','allocation_id','received_amount_usd'])
check('line_id unique', len({r['line_id'] for r in lines}) == len(lines))
check('allocation_id unique', len({r['allocation_id'] for r in payments}) == len(payments))
lc, pc = Counter(r['invoice_id'] for r in lines), Counter(r['invoice_id'] for r in payments)
check('no orphan allocations', set(pc) <= set(lc), sorted(set(pc)-set(lc)))
rev, cash = defaultdict(Decimal), defaultdict(Decimal)
for r in lines: rev[r['invoice_id']] += Decimal(r['net_amount_usd'])
for r in payments: cash[r['invoice_id']] += Decimal(r['received_amount_usd'])

# Actually construct the small naive equality joins to verify the prediction.
inner = [(l,p) for l in lines for p in payments if l['invoice_id'] == p['invoice_id']]
left = []
for l in lines:
    matches = [p for p in payments if p['invoice_id'] == l['invoice_id']]
    left.extend((l,p) for p in matches) if matches else left.append((l,None))
naive_inner_revenue = sum((Decimal(l['net_amount_usd']) for l,p in inner), Decimal(0))
naive_left_revenue = sum((Decimal(l['net_amount_usd']) for l,p in left), Decimal(0))
naive_inner_cash = sum((Decimal(p['received_amount_usd']) for l,p in inner), Decimal(0))
naive_left_cash = sum((Decimal(p['received_amount_usd']) if p else Decimal(0) for l,p in left), Decimal(0))
source_revenue, source_cash = sum_field(lines,'net_amount_usd'), sum_field(payments,'received_amount_usd')
unpaid_revenue = sum((rev[k] for k in lc if k not in pc), Decimal(0))
fanout_excess = sum((rev[k] * max(pc[k]-1,0) for k in lc), Decimal(0))

# Use the canonical helper; numeric audit fields remain unmodified.
helper = args.audit_helper.resolve()
if not helper.exists():
    raise FileNotFoundError('Pass --audit-helper pointing to the bundled join audit.')
spec = importlib.util.spec_from_file_location('frozen_join_audit', helper)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)
lt = audit_module.read_table(source_paths[0], ['invoice_id'], 'net_amount_usd')
rt = audit_module.read_table(source_paths[1], ['invoice_id'])
audit, evidence = audit_module.audit(lt,rt,'many-to-many','net_amount_usd')
for side, name in [('left','invoice-lines.csv'),('right','payment-allocations.csv')]:
    audit['sources'][side]['path'] = 'inputs/' + name
(OUT / 'audit').mkdir(exist_ok=True)
(OUT / 'audit/report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'audit/key-audit.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(evidence[0]));w.writeheader();w.writerows(evidence)
check('helper predicts actual INNER row count', audit['predicted_rows']['inner']==len(inner), len(inner))
check('helper predicts actual LEFT row count', audit['predicted_rows']['left']==len(left), len(left))
check('helper predicts actual INNER revenue', Decimal(audit['left_measure']['inner_join_total'])==naive_inner_revenue,fmt(naive_inner_revenue))
check('helper predicts actual LEFT revenue', Decimal(audit['left_measure']['left_join_total'])==naive_left_revenue,fmt(naive_left_revenue))
check('helper fanout excess agrees with reconstruction', Decimal(audit['left_measure']['duplication_excess'])==fanout_excess,fmt(fanout_excess))
check('declared many-to-many holds but does not make naive sums valid', audit['status']=='cardinality_holds' and naive_left_revenue!=source_revenue)
check('INNER bridge reconciles', source_revenue+fanout_excess-unpaid_revenue==naive_inner_revenue)
check('cash duplication verified independently by source line counts', naive_inner_cash-source_cash==sum((cash[k]*(lc[k]-1) for k in pc),Decimal(0)))

reconciliation=[]
for k in sorted(lc):
    amount=rev[k]; received=cash.get(k,Decimal(0)); due=amount-received
    reconciliation.append({'invoice_id':k,'invoice_line_count':lc[k],'payment_allocation_count':pc[k],
        'invoiced_revenue_usd':fmt(amount),'cash_received_usd':fmt(received),'remaining_receivable_usd':fmt(due),
        'payment_status':'unpaid' if not pc[k] else ('paid_in_full' if due==0 else 'part_paid'),
        'naive_inner_join_rows':lc[k]*pc[k],'naive_inner_revenue_usd':fmt(amount*pc[k]),
        'naive_left_join_rows':lc[k]*max(pc[k],1),'naive_left_revenue_usd':fmt(amount*max(pc[k],1)),
        'duplicate_revenue_usd':fmt(amount*max(pc[k]-1,0))})
with (OUT/'invoice-reconciliation.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(reconciliation[0])[:7],extrasaction='ignore');w.writeheader();w.writerows(reconciliation)
# Reopen the actual delivered table, not just its in-memory precursor.
with (OUT/'invoice-reconciliation.csv').open(encoding='utf-8',newline='') as f: delivered=list(csv.DictReader(f))
check('delivered CSV has exactly all four unique invoice keys', len(delivered)==4 and {r['invoice_id'] for r in delivered}==set(lc))
check('delivered revenue equals raw source', sum_field(delivered,'invoiced_revenue_usd')==source_revenue)
check('delivered cash equals raw source', sum_field(delivered,'cash_received_usd')==source_cash)
check('delivered balance reconciles invoice by invoice', all(Decimal(r['invoiced_revenue_usd'])-Decimal(r['cash_received_usd'])==Decimal(r['remaining_receivable_usd']) for r in delivered))
check('unpaid invoice retained with zero received', any(r['invoice_id']=='INV-1004' and r['cash_received_usd']=='0.00' and r['remaining_receivable_usd']=='150.00' and r['payment_status']=='unpaid' for r in delivered))
check('no invoice overpayment under supplied source contract', all(Decimal(r['remaining_receivable_usd'])>=0 for r in delivered))
check('expected closed-example totals', source_revenue==Decimal('1200') and source_cash==Decimal('1050') and unpaid_revenue==Decimal('150'))
check('expected demonstrated join behavior', (len(inner),len(left),naive_inner_revenue,naive_left_revenue,naive_inner_cash)==(11,13,Decimal('2350'),Decimal('2500'),Decimal('1850')))

facts={
 'schema_version':1,'synthetic_instructional_data':True,
 'source_contract':'inputs/source-notes.md','sources':{n:{'path':'inputs/'+n,'sha256':h} for n,h in source_hashes.items()},
 'definitions':{'currency':'USD','population':'All four supplied invoices; common cut-off from source contract, no calendar date supplied',
 'invoice_grain':'one line per line_id','payment_grain':'one received allocation per allocation_id','join_key':'exact invoice_id',
 'revenue':'Sum net_amount_usd once at invoice-line grain, after discounts and excluding tax, for the closed instructional period',
 'cash':'Sum received_amount_usd once at allocation grain through common cut-off',
 'balance':'Invoiced revenue minus allocated cash; no opening balances/refunds/voids/unlisted invoices under this source contract'},
 'totals':{'invoice_count':len(lc),'invoice_line_rows':len(lines),'allocation_rows':len(payments),
 'invoiced_revenue_usd':fmt(source_revenue),'cash_received_usd':fmt(source_cash),'remaining_receivable_usd':fmt(source_revenue-source_cash),
 'raw_inner_rows':len(inner),'raw_left_rows':len(left),'raw_inner_revenue_usd':fmt(naive_inner_revenue),'raw_left_revenue_usd':fmt(naive_left_revenue),
 'duplicate_revenue_usd':fmt(fanout_excess),'unpaid_revenue_dropped_by_inner_usd':fmt(unpaid_revenue),
 'inner_net_revenue_overstatement_usd':fmt(naive_inner_revenue-source_revenue),
 'raw_inner_cash_usd':fmt(naive_inner_cash),'raw_left_cash_usd':fmt(naive_left_cash),'cash_overstatement_usd':fmt(naive_inner_cash-source_cash)},
 'invoice_reconciliation':reconciliation,
 'raw_inner_pairs':[{'invoice_id':l['invoice_id'],'line_id':l['line_id'],'allocation_id':p['allocation_id'],
     'repeated_line_amount_usd':l['net_amount_usd'],'repeated_allocation_amount_usd':p['received_amount_usd']} for l,p in inner],
 'bridge':{'start_usd':fmt(source_revenue),'repeat_INV-1001_usd':'300.00','repeat_INV-1002_usd':'1000.00',
 'unpaid_invoice_excluded_usd':'-150.00','end_inner_usd':fmt(naive_inner_revenue)},
 'audit_helper':{'path':'../../skills/business-insight-diagnosis/scripts/join_audit.py','sha256':digest(helper),'expected_relationship':'many-to-many',
 'status':audit['status'],'interpretation':'Correct declared cardinality; unsafe additive sums on raw join. Actual constructed joins match predictions. Published report only normalizes source paths.'},
 'authority':{'delivery':'Prepared locally; not sent; operational report not changed',
 'recommendation':'Proposed report builder aggregates each source to invoice_id, then LEFT joins invoice summaries; accounting reviews before replacing report',
 'acceptance':'Before replacing report for this snapshot: four unique invoices including unpaid INV-1004; totals 1200/1050/150 USD; no orphan allocation; no duplicate invoice summaries',
 'limits':'Synthetic closed example; actual user join type, query and production output not supplied. Reproduced INNER/LEFT behavior does not prove a production repair or general accounting recognition policy.'}}

memo = f'''# Bản soạn nội bộ: sửa đối chiếu hóa đơn và tiền thu

**Dữ liệu giả lập để minh họa; chưa gửi, chưa thay báo cáo vận hành.**

Doanh thu hóa đơn đúng là **1.200 USD**, tiền đã thu **1.050 USD**, còn phải thu **150 USD**. Khoản tăng sau phép nối là lỗi đếm lặp. Cộng riêng từng nguồn theo `invoice_id`, rồi ghép với danh sách hóa đơn làm gốc sẽ giữ đủ bốn hóa đơn, gồm INV-1004 chưa trả.

| Hóa đơn | Dòng hóa đơn × khoản thu | Doanh thu đúng | Doanh thu sau nối trong | Phần cộng lặp | Tiền đã thu đúng | Còn phải thu |
|---|---:|---:|---:|---:|---:|---:|
| INV-1001 | 2 × 2 | 300 | 600 | 300 | 300 | 0 |
| INV-1002 | 2 × 3 | 500 | 1.500 | 1.000 | 500 | 0 |
| INV-1003 | 1 × 1 | 250 | 250 | 0 | 250 | 0 |
| INV-1004 | 2 × 0 | 150 | 0 (bị bỏ) | 0 | 0 | 150 |

Đơn vị: USD. Hai dòng 450 và 50 USD của INV-1002 ghép với ba khoản thu 250, 150 và 100 USD thành sáu tổ hợp. Mỗi dòng hóa đơn được tính ba lần: 500 thành 1.500 USD. INV-1001 tạo thêm 300 USD; tổng phần lặp là **1.300 USD**. Đây là nhiều dòng hàng và nhiều lần thu hợp lệ, không phải bản ghi nguồn trùng cần xóa.

Nếu dùng nối trong (INNER), INV-1004 bị loại vì chưa có khoản thu: **1.200 + 1.300 - 150 = 2.350 USD**, cao hơn nguồn 1.150 USD. Nếu dùng nối trái (LEFT) trực tiếp trên hai CSV, hóa đơn chưa trả được giữ nhưng doanh thu vẫn bị lặp: **2.500 USD**, cao hơn 1.300 USD. Cả hai cách cũng làm tiền thu thành **1.850 USD** thay vì 1.050 USD, thừa 800 USD vì khoản thu lặp theo số dòng hóa đơn. Chưa có truy vấn hoặc loại phép nối thực tế của người dùng; đây là hai hành vi đã tái tạo từ nguồn.

**Đề xuất để kế toán duyệt:** người phụ trách báo cáo cộng 7 dòng hóa đơn thành 4 tổng doanh thu, cộng 6 phân bổ thanh toán thành 3 tổng tiền thu, kiểm mỗi bảng có một dòng cho mỗi hóa đơn, rồi LEFT JOIN hai bảng tổng hợp. Chỉ đặt tiền thu bằng 0 khi hóa đơn thực sự không có khoản thu theo nguồn đầy đủ; không thay tiền lỗi hoặc thiếu bằng 0. Không dùng DISTINCT hoặc bỏ các dòng hợp lệ để chữa phép nối.

**Điều kiện trước khi thay báo cáo cho lần chốt này:** kế toán xác nhận đủ 4 mã hóa đơn, tổng doanh thu/tiền thu/còn phải thu lần lượt 1.200/1.050/150 USD, INV-1004 còn 150 USD, không có phân bổ vào hóa đơn ngoài nguồn và không có mã trùng trong bảng tổng. Nếu bất kỳ điều kiện nào lệch, giữ báo cáo chưa thay và đối chiếu nguồn trước. Đây là vai trò đề xuất, chưa phải phân công hoặc triển khai đã được phê duyệt.

Nguồn có thẩm quyền trong ví dụ: `inputs/source-notes.md`, `inputs/invoice-lines.csv`, `inputs/payment-allocations.csv`. Doanh thu trong bài là tổng giá trị hóa đơn sau giảm giá, chưa thuế; không suy rộng thành chính sách ghi nhận doanh thu thực tế. Nguồn quy định cùng mốc chốt nhưng không cho ngày lịch, không có hoàn tiền/hủy/số dư đầu kỳ/hóa đơn ngoài danh sách. Chi tiết số và dấu vân tay SHA-256 nằm trong `calculations.json`; kết quả audit và kiểm tái tạo nằm trong `audit/` và `audit-result.json`.
'''
(OUT/'memo.md').write_text(memo,encoding='utf-8')

# One source of layout commands draws both an editable text SVG and embedded-font PDF.
WIDTH,HEIGHT=595.276,841.89
font_root=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('AR',str(font_root/'arial.ttf')))
pdfmetrics.registerFont(TTFont('AB',str(font_root/'arialbd.ttf')))
INK='#173342'; MUTED='#4C626D'; TEAL='#005B52'; AMBER='#7C4614'; PALE='#FFF3E3'; LIGHT='#EDF5F3'; LINE='#CED9DB'; WHITE='#FFFFFF'
pdf=canvas.Canvas(str(OUT/'brief.pdf'),pagesize=(WIDTH,HEIGHT))
pdf.setTitle('Đối chiếu hóa đơn và tiền thu | Dữ liệu giả lập')
pdf.setAuthor('Bản soạn nội bộ')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
'<title id="title">Giá trị hóa đơn là 1.200 USD; phép nối thô đếm lặp</title>',
'<desc id="desc">INV-1002 có hai dòng hóa đơn 450 và 50 USD, ba khoản thu 250, 150, 100 USD. Sáu tổ hợp nối làm doanh thu 500 thành 1.500 USD. Tổng cộng lặp 1.300 USD; nối trong còn bỏ 150 USD chưa trả và báo 2.350. Bảng đúng giữ bốn hóa đơn: doanh thu 1.200, thu 1.050, còn 150 USD. Chi tiết có trong invoice-reconciliation.csv và memo.md.</desc>',
f'<rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>']
layout_checks=[]
def rect(x,y,w,h,fill,stroke=None):
    pdf.setFillColor(fill)
    if stroke: pdf.setStrokeColor(stroke)
    pdf.rect(x,HEIGHT-y-h,w,h,fill=1,stroke=bool(stroke))
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def line(x1,y1,x2,y2,color=LINE,width=.7):
    pdf.setStrokeColor(color);pdf.setLineWidth(width);pdf.line(x1,HEIGHT-y1,x2,HEIGHT-y2)
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
def text(s,x,y,size=10,color=INK,bold=False,anchor='start',max_width=None):
    font='AB' if bold else 'AR';w=pdfmetrics.stringWidth(s,font,size)
    start=x if anchor=='start' else x-w if anchor=='end' else x-w/2
    fits=max_width is None or w<=max_width+.01
    on_page=start>=32 and start+w<=WIDTH-32 and 30<y<HEIGHT-20
    layout_checks.append({'text':s,'width':w,'assigned_width':max_width,'fits':fits,'on_page':on_page})
    if not fits or not on_page:raise AssertionError(f'Layout: {s}; width={w}, assigned={max_width}, x={start}, y={y}')
    pdf.setFont(font,size);pdf.setFillColor(color)
    pdf.drawString(start,HEIGHT-y,s)
    svg.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(s)}</text>')
def lines_text(values,x,y,size=10,leading=14,**kw):
    for i,s in enumerate(values):text(s,x,y+i*leading,size,**kw)

text('BẢN SOẠN NỘI BỘ  /  DỮ LIỆU GIẢ LẬP',40,43,9,MUTED,True)
lines_text(['Giá trị hóa đơn: 1.200 USD.','Phép nối thô đã đếm lặp tiền.'],40,78,22,27,bold=True,max_width=515)
text('4 hóa đơn · cùng mốc chốt theo nguồn · USD · giá trị hóa đơn sau giảm giá, chưa thuế',40,130,9.2,MUTED,max_width=515)

text('01   INV-1002: hai dòng hóa đơn, ba khoản thu, sáu tổ hợp',40,166,12,INK,True,max_width=515)
rect(40,184,515,144,'#F6F8F7')
text('MỖI CỘT LÀ MỘT KHOẢN THU',56,207,8.4,MUTED,True)
text('250 USD',185,228,9,INK,True,anchor='middle')
text('150 USD',249,228,9,INK,True,anchor='middle')
text('100 USD',313,228,9,INK,True,anchor='middle')
text('Dòng 450 USD',56,258,9,INK)
text('Dòng 50 USD',56,287,9,INK)
for y,amount in [(244,'450'),(273,'50')]:
    for x in [157,221,285]:
        rect(x,y,56,25,PALE)
        text(amount,x+28,y+17,11,AMBER,True,anchor='middle')
text('Các ô là tiền hóa đơn được cộng sau nối, không phải tiền thu.',56,314,8.3,MUTED,max_width=485)
line(360,199,360,302)
lines_text(['450 + 50 = 500 USD','Mỗi dòng xuất hiện 3 lần.','500 × 3 = 1.500 USD'],378,226,10,19,max_width=162)
text('Dư 1.000 USD',378,292,14,AMBER,True,max_width=162)
text('INV-1001 cũng lặp: 300 thành 600 USD, dư 300. Tổng phần lặp: 1.300 USD.',40,347,10,INK,max_width=515)

text('02   Chỉ giữ hóa đơn có khoản thu sẽ bỏ INV-1004',40,382,12,INK,True,max_width=515)
bridge=[(40,'1.200','Nguồn đúng',INK),(179,'+1.300','Phần cộng lặp',AMBER),(318,'-150','INV-1004 bị bỏ',MUTED),(457,'2.350','Sau nối trong',AMBER)]
for x,value,label,color in bridge:
    text(value,x,411,20,color,True,max_width=98)
    text(label,x,432,9,MUTED,max_width=100)
text('=',424,411,16,MUTED,anchor='middle')
text('Ghép thô và giữ mọi hóa đơn: 2.500 USD. Tiền thu cả hai cách: 1.850 thay vì 1.050 USD.',40,453,9.1,MUTED,max_width=515)

text('03   Bảng đúng để kế toán đối chiếu',40,491,12,INK,True,max_width=515)
text('USD',555,491,9,MUTED,anchor='end')
rect(40,504,515,27,INK)
col=[52,310,430,543]
text('Hóa đơn',col[0],522,9.4,WHITE,True)
text('Doanh thu',col[1],522,9.4,WHITE,True,anchor='end')
text('Đã thu',col[2],522,9.4,WHITE,True,anchor='end')
text('Còn phải thu',col[3],522,9.4,WHITE,True,anchor='end')
for i,r in enumerate(reconciliation):
    y=531+i*29
    if i==3:rect(40,y,515,29,PALE)
    text(r['invoice_id']+(' · Chưa trả' if i==3 else ''),col[0],y+19,10,INK,bold=i==3,max_width=200)
    for x,key in zip(col[1:],['invoiced_revenue_usd','cash_received_usd','remaining_receivable_usd']):
        text(vn(r[key]),x,y+19,10,INK,bold=i==3,anchor='end')
    line(40,y+29,555,y+29)
rect(40,647,515,31,LIGHT)
text('TỔNG · 4 hóa đơn',52,668,10,TEAL,True)
for x,value in zip(col[1:],[source_revenue,source_cash,source_revenue-source_cash]):
    text(vn(value),x,668,11,TEAL,True,anchor='end')

text('Sửa báo cáo trước khi dùng số để ra quyết định',40,710,12,INK,True,max_width=515)
lines_text(['Cộng theo từng hóa đơn: 7 dòng hóa đơn thành 4 tổng; 6 khoản thu thành 3 tổng.',
            'Ghép các tổng với danh sách hóa đơn làm gốc và giữ INV-1004 chưa trả.',
            'Trước khi thay, kế toán soát truy vấn thực tế và tổng 1.200 / 1.050 / 150 USD.'],40,733,10,15,max_width=515)
line(40,784,555,784)
lines_text(['Nguồn: invoice-lines.csv, payment-allocations.csv; định nghĩa: source-notes.md.',
            'Đã tái tạo hai kiểu nối; chưa có truy vấn thực tế. Dữ liệu giả lập theo nguồn.',
            'Chỉ soạn, chưa gửi; chưa sửa báo cáo vận hành hoặc xác nhận chính sách kế toán.'],40,791,8.3,12,color=MUTED,max_width=515)
pdf.showPage();pdf.save();svg.append('</svg>')
(OUT/'brief.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
check('all page text fits assigned widths and stays in margins',all(r['fits'] and r['on_page'] for r in layout_checks),{'text_elements':len(layout_checks)})

# Read the final PDF and render at 150 DPI (readable full-page preview).
reader=PdfReader(str(OUT/'brief.pdf'))
check('PDF exactly one A4 page',len(reader.pages)==1 and abs(float(reader.pages[0].mediabox.width)-WIDTH)<.05 and abs(float(reader.pages[0].mediabox.height)-HEIGHT)<.05)
pdf_text=reader.pages[0].extract_text()
for required in ['Giá trị hóa đơn: 1.200 USD.','Dư 1.000 USD','INV-1004','1.850','1.050','Chưa trả','chưa gửi']:
    check('PDF includes verified content: '+required,required in pdf_text)
check('PDF has no replacement glyph', '\ufffd' not in pdf_text and '\u25a0' not in pdf_text)
subprocess.run([str(args.poppler),'-png','-singlefile','-r','150',str(OUT/'brief.pdf'),str(OUT/'brief')],check=True,capture_output=True)
with Image.open(OUT/'brief.png') as image:
    check('preview full page at readable scale', image.width>=1200 and image.height>=1700, {'width':image.width,'height':image.height})
import xml.etree.ElementTree as ET
svg_root=ET.parse(OUT/'brief.svg').getroot()
check('SVG is editable text with semantic alternative', len(svg_root.findall('{http://www.w3.org/2000/svg}text'))>=50 and svg_root.find('{http://www.w3.org/2000/svg}desc') is not None)

def luminance(c):
    rgb=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v,w in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
    hi,lo=sorted([luminance(a),luminance(b)],reverse=True);return (hi+.05)/(lo+.05)
contrasts={f'{fg} on {bg}':round(contrast(fg,bg),3) for fg,bg in [(INK,WHITE),(MUTED,WHITE),(INK,'#F6F8F7'),(AMBER,PALE),(WHITE,INK),(TEAL,LIGHT),(INK,PALE)]}
check('essential text contrasts at least 4.5:1',all(v>=4.5 for v in contrasts.values()),contrasts)
check('raw source bytes unchanged', all(digest(p)==source_hashes[p.name] for p in source_paths),source_hashes)
facts['render_checks']={'page_count':len(reader.pages),'page_size_points':[WIDTH,HEIGHT],'preview_dpi':150,
 'essential_text_contrast_ratios':contrasts,'text_svg_elements':len(svg_root.findall('{http://www.w3.org/2000/svg}text')),
 'authority':'Automated geometry/text checks plus model visual inspection; no human comprehension or business-impact evidence'}
(OUT/'calculations.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result={'status':'all_programmatic_checks_passed','checks':checks,
 'visual_review':'Pending direct review of the actual generated PNG; record completion in receipt.md',
 'authority':'Source-based synthetic analysis; not production validation, implementation, or approval',
 'deliverable_sha256':{n:digest(OUT/n) for n in ['invoice-reconciliation.csv','memo.md','brief.pdf','brief.svg','brief.png','calculations.json']}}
(OUT/'audit-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
skill_reads=[
 'business-insight-diagnosis/SKILL.md','business-insight-diagnosis/references/evidence-contract.md','business-insight-diagnosis/references/join-audit.md','business-insight-diagnosis/scripts/join_audit.py',
 'data-storytelling/SKILL.md','data-storytelling/references/decision-workflow.md',
 'business-chart-communication/SKILL.md','business-chart-communication/references/chart-method.md','evidence-to-narrative/SKILL.md']
print(json.dumps({'output':str(OUT),'checks_passed':len(checks),'revenue_usd':fmt(source_revenue),'cash_usd':fmt(source_cash),'receivable_usd':fmt(source_revenue-source_cash),'render':'brief.png'},ensure_ascii=False))
