"""Rebuild the bounded comparison report from the frozen instructional CSV.

Run with an available Python runtime:
python examples/02-fair-comparison/rebuild.py --output ./scratch/comparison-v3

No network, downloads, external publication, or input modification. The SVG
contains editable text; PDF and SVG are drawn from one layout definition.
This report's narrative is specific to these four rows: a changed input is
rejected rather than silently reusing a stale conclusion.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal
import csv
import hashlib
import json
import html
import argparse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader
import pypdfium2 as pdfium

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=HERE)
args = parser.parse_args()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = HERE / 'data.csv'
raw = SOURCE.read_bytes()
source_sha = hashlib.sha256(raw).hexdigest()
with SOURCE.open(encoding='utf-8-sig', newline='') as stream:
    reader = csv.DictReader(stream)
    assert reader.fieldnames == ['team', 'lead_tier', 'eligible_leads', 'wins']
    rows = [{**r, 'eligible_leads': int(r['eligible_leads']), 'wins': int(r['wins'])} for r in reader]
expected = [('A', 'High', 20, 12), ('A', 'Low', 60, 12), ('B', 'High', 60, 33), ('B', 'Low', 20, 3)]
assert [(r['team'], r['lead_tier'], r['eligible_leads'], r['wins']) for r in rows] == expected, 'Input differs from the frozen report scope; revise the narrative before rebuilding.'
assert len({(r['team'], r['lead_tier']) for r in rows}) == len(rows)
assert all(0 <= r['wins'] <= r['eligible_leads'] and r['eligible_leads'] > 0 for r in rows)

lookup = {(r['team'], r['lead_tier']): r for r in rows}
teams = {}
for team in ['A', 'B']:
    subset = [r for r in rows if r['team'] == team]
    leads = sum(r['eligible_leads'] for r in subset)
    wins = sum(r['wins'] for r in subset)
    rates = {tier: Fraction(lookup[team, tier]['wins'], lookup[team, tier]['eligible_leads']) for tier in ['High', 'Low']}
    weights = {tier: Fraction(lookup[team, tier]['eligible_leads'], leads) for tier in ['High', 'Low']}
    overall = Fraction(wins, leads)
    assert sum(weights.values()) == 1
    assert sum(weights[tier] * rates[tier] for tier in rates) == overall
    # Independent decimal arithmetic uses source counts directly.
    assert Decimal(wins) / Decimal(leads) == Decimal(overall.numerator) / Decimal(overall.denominator)
    teams[team] = dict(leads=leads, wins=wins, rates=rates, weights=weights, overall=overall)

pooled_counts = {tier: sum(r['eligible_leads'] for r in rows if r['lead_tier'] == tier) for tier in ['High', 'Low']}
total_leads = sum(r['eligible_leads'] for r in rows)
common = {tier: Fraction(pooled_counts[tier], total_leads) for tier in pooled_counts}
adjusted = {team: sum(common[tier] * teams[team]['rates'][tier] for tier in common) for team in teams}
raw_gap = teams['B']['overall'] - teams['A']['overall']
raw_relative = raw_gap / teams['A']['overall']
within_gap = {tier: teams['B']['rates'][tier] - teams['A']['rates'][tier] for tier in common}
adjusted_gap = adjusted['B'] - adjusted['A']
mix_component = sum((teams['B']['weights'][tier] - teams['A']['weights'][tier]) * teams['A']['rates'][tier] for tier in common)
rate_component = sum(teams['B']['weights'][tier] * within_gap[tier] for tier in common)
assert raw_gap == mix_component + rate_component
assert (teams['A']['overall'], teams['B']['overall'], raw_gap, raw_relative) == (Fraction(3, 10), Fraction(9, 20), Fraction(3, 20), Fraction(1, 2))
assert within_gap == {'High': Fraction(-1, 20), 'Low': Fraction(-1, 20)}
assert adjusted == {'A': Fraction(2, 5), 'B': Fraction(7, 20)}
assert adjusted_gap == Fraction(-1, 20)
sensitivities = {}
for reference in teams:
    ref_weights = teams[reference]['weights']
    result = {team: sum(ref_weights[tier] * teams[team]['rates'][tier] for tier in ref_weights) for team in teams}
    assert result['B'] - result['A'] == Fraction(-1, 20)
    sensitivities[reference] = {'weights': ref_weights, 'rates': result, 'B_minus_A': result['B'] - result['A']}
# For every shared High weight w in [0,1], the gap is w*(-.05)+(1-w)*(-.05)=-.05.
assert within_gap['High'] == within_gap['Low'] == adjusted_gap

def exact(f):
    if not isinstance(f, Fraction):
        return f
    value = Decimal(f.numerator) / Decimal(f.denominator)
    return {'numerator': f.numerator, 'denominator': f.denominator, 'fraction': str(f), 'decimal': str(value), 'percent': str(value * 100)}

def encode(o):
    if isinstance(o, Fraction): return exact(o)
    if isinstance(o, dict): return {k: encode(v) for k, v in o.items()}
    if isinstance(o, list): return [encode(v) for v in o]
    return o

calcs = {
    'source': {'path': 'data.csv', 'sha256': source_sha, 'synthetic_instructional_data': True, 'rows': rows},
    'metric': {'name': 'win_rate', 'definition': 'wins / eligible_leads', 'grain': 'team x lead_tier aggregate row', 'unit': 'proportion; displayed as percent', 'period': None, 'period_comparability': 'unknown', 'High_Low_definition': 'not supplied', 'coaching_exposure_and_assignment': 'not supplied'},
    'teams': teams,
    'observed_aggregate': {'B_minus_A': raw_gap, 'relative_B_vs_A': raw_relative, 'interpretation': 'Cross-team difference in the supplied rows, not temporal growth or a coaching effect.'},
    'within_tier_B_minus_A': within_gap,
    'common_mix_comparison': {'method': 'Direct standardization: sum(shared tier weight * team tier win rate)', 'pooled_tier_lead_counts': pooled_counts, 'weights': common, 'rates': adjusted, 'B_minus_A': adjusted_gap, 'relative_B_vs_A': adjusted_gap / adjusted['A'], 'interpretation': 'Computed common-mix comparison; not additional observed wins and not a causal estimate.'},
    'sensitivity_using_each_team_mix': sensitivities,
    'any_shared_mix_result': {'formula': 'w*(-1/20) + (1-w)*(-1/20) = -1/20 for every w in [0,1]', 'B_minus_A': adjusted_gap},
    'exact_aggregate_gap_decomposition': {'reference_rates': 'A', 'reference_weights_for_rate_component': 'B', 'mix_component': mix_component, 'within_tier_rate_component': rate_component, 'sum': raw_gap, 'interpretation': 'Arithmetic reconciliation, not causal attribution.'},
    'limitations': ['No observation dates or comparable maturity window.', 'No coaching allocation, exposure, pre/post baseline, randomization, or individual records.', 'Tier definitions and residual differences within tiers are unknown.', 'No inference that A coaching is causally superior or B coaching is harmful.', 'No confidence intervals, significance claims, client outcomes, or impact forecasts are asserted.']
}
(OUT / 'calculations.json').write_text(json.dumps(encode(calcs), ensure_ascii=False, indent=2), encoding='utf-8')

memo = '''# Báo cáo sales: sửa kết luận về coaching

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
'''
(OUT / 'memo.md').write_text(memo, encoding='utf-8')

pdfmetrics.registerFont(TTFont('ReportArial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ReportArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
W, H = 794, 1123
scale = A4[0] / W
pdf = canvas.Canvas(str(OUT / 'brief.pdf'), pagesize=(A4[0], H * scale), pageCompression=1)
pdf.setTitle('Rà soát kết luận sales: chưa đủ bằng chứng để nhân rộng coaching của B')
pdf.setAuthor('Báo cáo từ dữ liệu giả lập phục vụ học tập')
pdf.setSubject('So sánh tỷ lệ chốt theo tier và cơ cấu lead; giới hạn bằng chứng và quyết định đề xuất')
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">', '<title id="title">Chưa đủ bằng chứng để nhân rộng coaching của B</title>', '<desc id="desc">Dữ liệu giả lập. Gộp toàn bộ lead: A 30%, B 45%. B có 75% lead High, A có 25%. Trong High: A 60%, B 55%; trong Low: A 20%, B 15%. Cùng cơ cấu 50% High và 50% Low: A 40%, B 35%. Thiếu thời gian quan sát và việc phân coaching nên chưa xác định được tác động. Đề xuất thử nghiệm có đối chứng trước khi nhân rộng. Số chính xác trong memo.md và calculations.json.</desc>']
INK, MUTED, A_COLOR, B_COLOR = '#172A2B', '#4D6061', '#314A4D', '#136D69'
BG, RULE, PALE = '#FCFBF8', '#D2DCDC', '#EAF2F0'
placed_text = []

def rgb(color):
    return tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))

def rectangle(x, y, w, h, fill):
    pdf.setFillColorRGB(*rgb(fill))
    pdf.rect(x * scale, (H - y - h) * scale, w * scale, h * scale, fill=1, stroke=0)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')

def line(x1, y1, x2, y2, color=RULE, width=1):
    pdf.setStrokeColorRGB(*rgb(color)); pdf.setLineWidth(width * scale)
    pdf.line(x1 * scale, (H - y1) * scale, x2 * scale, (H - y2) * scale)
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')

def text(x, y, s, size=16, bold=False, color=INK, align='left'):
    font = 'ReportArialBold' if bold else 'ReportArial'
    tw = pdfmetrics.stringWidth(s, font, size)
    tx = x - (tw if align == 'right' else tw / 2 if align == 'center' else 0)
    assert tx >= 45 and tx + tw <= 750, (s, tx, tw)
    assert 20 <= y <= H - 20
    pdf.setFillColorRGB(*rgb(color)); pdf.setFont(font, size * scale)
    pdf.drawString(tx * scale, (H - y) * scale, s)
    anchor = {'left': 'start', 'right': 'end', 'center': 'middle'}[align]
    svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{html.escape(s)}</text>')
    placed_text.append({'text': s, 'x': tx, 'baseline': y, 'width': tw, 'font_px': size})

rectangle(0, 0, W, H, BG)
text(48, 49, 'RÀ SOÁT KẾT LUẬN SALES  |  DỮ LIỆU GIẢ LẬP', 13.3, True, B_COLOR)
text(48, 99, 'Chưa đủ bằng chứng', 35, True)
text(48, 142, 'để nhân rộng coaching của B', 35, True)
text(48, 181, 'B cao hơn khi gộp lead, nhưng thấp hơn A trong từng nhóm.', 17.5)
text(48, 216, 'CSV không có thời gian quan sát hoặc cách phân coaching;', 15, color=MUTED)
text(48, 238, '+50% là chênh lệch tỷ lệ gộp, chưa phải hiệu quả coaching.', 15, color=MUTED)
line(48, 260, 746, 260)

text(48, 293, 'Cùng cơ cấu lead, thứ hạng đảo chiều', 22, True)
text(48, 327, 'Gộp theo cơ cấu thực tế', 17, True)
text(416, 327, 'Chuẩn hóa cùng cơ cấu lead', 17, True)
text(48, 351, 'B cao hơn 15 điểm % (+50% so với A)', 14.5, color=MUTED)
text(416, 351, 'B thấp hơn 5 điểm %', 14.5, True, B_COLOR)

plot_origins = [76, 444]
plot_width = 228
for origin in plot_origins:
    for tick in [0, 20, 40, 60]:
        xx = origin + plot_width * tick / 60
        line(xx, 372, xx, 453, RULE, 0.7)
        text(xx, 477, f'{tick}%', 13, color=MUTED, align='center')
    line(origin, 453, origin + plot_width, 453, MUTED, 0.8)

for origin, rates, counts in [(76, {t: teams[t]['overall'] for t in teams}, True), (444, adjusted, False)]:
    for team, y in [('A', 383), ('B', 427)]:
        color = A_COLOR if team == 'A' else B_COLOR
        text(origin - 15, y + 7, team, 16, True, color, 'right')
        bw = float(rates[team]) / 0.60 * plot_width
        rectangle(origin, y - 12, bw, 22, color)
        rate_label = f'{float(rates[team]) * 100:.0f}%'
        label = rate_label + (f" · {teams[team]['wins']}/{teams[team]['leads']}" if counts else '')
        text(origin + bw + 8, y + 6, label, 14.5, True, color)

text(48, 505, 'A và B: mỗi bên 80 lead', 14.5, color=MUTED)
text(48, 527, 'Lead High: A 25% | B 75%', 14.5, True)
text(416, 505, '50% High + 50% Low cho cả hai', 14.5, True)
text(416, 527, 'Từ 160 lead: 80 High, 80 Low', 14.5, color=MUTED)
text(48, 553, 'Tỷ lệ chuẩn hóa dùng để so sánh; không phải số chốt mới quan sát.', 14.3, color=MUTED)
line(48, 573, 746, 573)

text(48, 607, 'Kiểm lại từng nhóm lead', 21, True)
text(48, 640, 'Nhóm lead', 14, True, MUTED)
text(290, 640, 'A: chốt / lead', 14, True, A_COLOR)
text(482, 640, 'B: chốt / lead', 14, True, B_COLOR)
text(746, 640, 'B - A', 14, True, MUTED, 'right')
line(48, 651, 746, 651)
for tier, y in [('High', 677), ('Low', 716)]:
    text(48, y, tier, 16, True)
    for team, x in [('A', 290), ('B', 482)]:
        r = lookup[team, tier]
        text(x, y, f"{r['wins']}/{r['eligible_leads']} = {float(teams[team]['rates'][tier]) * 100:.0f}%", 16, color=A_COLOR if team == 'A' else B_COLOR)
    text(746, y, '-5 điểm %', 15.5, True, align='right')
line(48, 732, 746, 732)
text(48, 758, 'Với mọi cơ cấu High/Low chung, B đều thấp hơn A 5 điểm %.', 15.2, True)

rectangle(48, 790, 698, 204, PALE)
text(68, 823, 'Quyết định đề xuất: kiểm thử trước khi nhân rộng', 19, True)
decision_lines = [
    '• Trưởng nhóm đề xuất chia ngẫu nhiên nhân sự A: coaching B /',
    '  đối chứng; cân bằng High/Low giữa hai nhóm. Chưa triển khai đại trà.',
    '• Chốt số mẫu, thời gian đủ để lead chốt, chi phí, ngưỡng cải thiện',
    '  và quy tắc dừng trước khi bắt đầu.',
    '• Chỉ nhân rộng khi lợi ích đạt ngưỡng đã thống nhất, với độ bất định',
    '  chấp nhận được.'
]
for n, s in enumerate(decision_lines): text(68, 853 + n * 23, s, 14.8)

text(48, 1030, 'Nguồn: data.csv · 4 dòng · 160 lead · tỷ lệ chốt = wins / eligible_leads.', 14, color=MUTED)
text(48, 1052, 'Dữ liệu giả lập. CSV chưa định nghĩa High/Low; giữ nguyên nhãn nguồn.', 14, color=MUTED)
line(48, 1070, 746, 1070)
text(48, 1095, 'TÀI LIỆU HỌP  |  BẢN SỬA KẾT LUẬN', 11.8, True, MUTED)
text(746, 1095, '1 / 1', 12, color=MUTED, align='right')

pdf.showPage(); pdf.save()
svg.append('</svg>')
(OUT / 'brief.svg').write_text('\n'.join(svg), encoding='utf-8')

reader = PdfReader(str(OUT / 'brief.pdf'))
assert len(reader.pages) == 1
extracted = reader.pages[0].extract_text()
for required in [t['text'] for t in placed_text]:
    assert required in extracted, f'Missing PDF text: {required}'
assert '\ufffd' not in extracted
pagebox = reader.pages[0].mediabox
assert abs(float(pagebox.width) - A4[0]) < 0.01
assert abs(float(pagebox.height) - A4[1]) < 0.5
assert SOURCE.read_bytes() == raw, 'Input was modified.'

doc = pdfium.PdfDocument(str(OUT / 'brief.pdf'))
page = doc[0]
bitmap = page.render(scale=2.4)
preview = bitmap.to_pil()
preview.save(OUT / 'brief.png')
png_size = preview.size
page.close(); doc.close()

def luminance(color):
    def f(v): return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [f(v) for v in rgb(color)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(fg, bg):
    x, y = sorted([luminance(fg), luminance(bg)])
    return (y + 0.05) / (x + 0.05)

contrasts = {f'{fg} on {bg}': contrast(fg, bg) for fg, bg in [(INK, BG), (MUTED, BG), (A_COLOR, BG), (B_COLOR, BG), (INK, PALE)]}
assert all(v >= 4.5 for v in contrasts.values())
assert all(t['font_px'] >= 13 for t in placed_text if t['baseline'] < 1070)

print(json.dumps({'output': str(OUT), 'pages': 1, 'preview_pixels': png_size, 'source_sha256': source_sha, 'files': ['brief.pdf', 'brief.svg', 'brief.png', 'memo.md', 'calculations.json', 'rebuild.py']}, ensure_ascii=False))
