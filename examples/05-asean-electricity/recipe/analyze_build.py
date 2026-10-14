from __future__ import annotations
import argparse, csv, hashlib, html, json, re, shutil
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

P = argparse.ArgumentParser()
P.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1] / 'input')
P.add_argument('--out', type=Path, default=Path(__file__).resolve().parent / 'output')
args = P.parse_args()
src, out = args.source.resolve(), args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
raw = src / 'raw/ember-generation-five-countries-2015-2024.csv'
provenance = json.loads((src / 'provenance.json').read_text(encoding='utf-8'))
assert hashlib.sha256(raw.read_bytes()).hexdigest() == provenance['retained_csv']['sha256']
rows = list(csv.DictReader(raw.open(encoding='utf-8', newline='')))
codes = ['VNM', 'THA', 'MYS', 'PHL', 'IDN']
names = dict(zip(codes, ['Việt Nam', 'Thái Lan', 'Malaysia', 'Philippines', 'Indonesia']))
colors = dict(zip(codes, ['#00695e', '#9c5414', '#315f80', '#6b526f', '#4e5860']))
years = list(range(2015, 2025))
sources = ['Wind', 'Solar', 'Wind and solar', 'Total generation']
key = lambda r: (r['ISO 3 code'], int(r['Year']), r['Electricity source'])
assert len(rows) == 200 and len({key(r) for r in rows}) == 200
assert {key(r) for r in rows} == {(c,y,s) for c in codes for y in years for s in sources}
lookup = {key(r): r for r in rows}
def v(c,y,s,field):
    val = lookup[c,y,s][field]
    assert val != ''
    return Decimal(val)
def share(c,y): return v(c,y,'Wind and solar','Share of generation (%)')
def gen(c,y,s='Wind and solar'): return v(c,y,s,'Generation (TWh)')
reconciliation = []
for c in codes:
    for y in years:
        a, w, s, total = gen(c,y), gen(c,y,'Wind'), gen(c,y,'Solar'), gen(c,y,'Total generation')
        assert a >= 0 and total > 0 and abs(a-w-s) <= Decimal('0.001')
        component_diff = abs(share(c,y) - v(c,y,'Wind','Share of generation (%)') - v(c,y,'Solar','Share of generation (%)'))
        recalculated = a / total * 100
        assert abs(recalculated - share(c,y)) <= Decimal('0.001')
        assert component_diff <= Decimal('0.001')
        reconciliation.append({'iso':c,'year':y,'reported_share_pct':float(share(c,y)),
          'generation_share_pct':float(recalculated),'share_diff_pp':float(recalculated-share(c,y)),
          'component_share_diff_pp':float(component_diff),'component_generation_diff_twh':float(a-w-s)})
def n(x,places=2):
    return f"{Decimal(str(x)).quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP):.{places}f}".replace('.', ',')
facts = {
 'metric':'Published wind and solar share of domestic annual electricity generation; net imports excluded',
 'scope':{'iso':codes,'years':years,'source_rows':len(rows),'annual_combined_observations':50},
 'countries':{c:{'name':names[c],'share_2015_pct':float(share(c,2015)),'share_2024_pct':float(share(c,2024)),
                  'change_2015_2024_pp':float(share(c,2024)-share(c,2015)),
                  'annual_shares_pct':[float(share(c,y)) for y in years]} for c in codes},
 'vietnam':{
   'share_2018_pct':float(share('VNM',2018)), 'share_2021_pct':float(share('VNM',2021)),
   'change_2018_2021_pp':float(share('VNM',2021)-share('VNM',2018)),
   'share_2023_pct':float(share('VNM',2023)), 'share_2024_pct':float(share('VNM',2024)),
   'change_2023_2024_pp':float(share('VNM',2024)-share('VNM',2023)),
   'ws_2023_twh':float(gen('VNM',2023)), 'ws_2024_twh':float(gen('VNM',2024)),
   'total_2023_twh':float(gen('VNM',2023,'Total generation')), 'total_2024_twh':float(gen('VNM',2024,'Total generation')),
   'ws_growth_pct':float((gen('VNM',2024)/gen('VNM',2023)-1)*100),
   'total_growth_pct':float((gen('VNM',2024,'Total generation')/gen('VNM',2023,'Total generation')-1)*100),
   'gap_thailand_2024_pp':float(share('VNM',2024)-share('THA',2024))},
 'source_sha256':provenance['retained_csv']['sha256'],
 'reconciliation':reconciliation,
}
(out/'facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (out/'annual-calculations.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ISO','Country','Year','Wind_TWh','Solar_TWh','Wind_and_solar_TWh','Total_generation_TWh','Reported_share_pct','Computed_share_pct','Change_vs_previous_year_pp'])
    for c in codes:
        for y in years:
            writer.writerow([c,names[c],y,gen(c,y,'Wind'),gen(c,y,'Solar'),gen(c,y),gen(c,y,'Total generation'),share(c,y),gen(c,y)/gen(c,y,'Total generation')*100, '' if y==2015 else share(c,y)-share(c,y-1)])

ink='#1d2b31'; muted='#47575d'; paper='#faf8f1'; grid='#d7dcd8'
def txt(x,y,text,size=22,fill=ink,anchor='start',weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(str(text))}</text>'
def line(x1,y1,x2,y2,color=grid,width=1,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" {extra}/>'
def circle(x,y,r,color,filled=True):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color if filled else paper}" stroke="{color}" stroke-width="2.5"/>'
def svg(parts,w,h,title,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><g font-family="Arial, sans-serif">'+''.join(parts)+'</g></svg>'
def foot(parts,y,rounding=False):
    parts += [txt(0,y,'Tỷ trọng trong phát điện nội địa; không tính nhập khẩu ròng.',18,muted),
      txt(0,y+25,'Chỉ năm nước trong dữ liệu. Nguồn: Ember, tải 14/10/2026; CC BY 4.0.',18,muted)]
    if rounding: parts.append(txt(0,y+50,'Nhãn làm tròn; mức tăng tính từ số gốc.',18,muted))
def comparison(mobile=False):
    parts=[]
    if not mobile:
        w,h=940,520; x0=175; span=580
        parts += [txt(0,25,'Điện gió + mặt trời trong tổng phát điện (%)',22,ink,weight='bold'),
                  circle(17,57,6,muted,False),txt(32,64,'2015',20,muted),circle(112,57,6,ink),txt(126,64,'2024',20,muted),
                  txt(940,64,'Tăng từ 2015 (điểm %)',20,ink,'end')]
        for t in [0,4,8,12,16]:
            x=x0+span*t/16
            parts += [line(x,87,x,384),txt(x,414,str(t),20,muted,'middle')]
        for i,c in enumerate(codes):
            y=115+i*61; a=float(share(c,2015)); b=float(share(c,2024)); xa=x0+span*a/16; xb=x0+span*b/16
            parts += [txt(0,y+8,names[c],23,ink,weight='bold' if c=='VNM' else 'normal'),line(xa,y,xb,y,colors[c],4),circle(xa,y,6,colors[c],False),circle(xb,y,7,colors[c]),
                      txt(xa,y+27,n(a),20,muted,'middle'),txt(xb+12,y-8,n(b),22,colors[c],weight='bold'),txt(940,y+8,'+'+n(b-a),22,ink,'end')]
        foot(parts,459,True)
    else:
        w,h=350,580; x0=14; span=300
        parts += [txt(0,23,'Tỷ trọng điện gió + mặt trời (%)',19,ink,weight='bold'),
          circle(10,48,5,muted,False),txt(24,54,'2015',18,muted),circle(98,48,5,ink),txt(111,54,'2024',18,muted),txt(183,54,'Thang 0–16%',18,muted)]
        for i,c in enumerate(codes):
            y=105+i*79; a=float(share(c,2015)); b=float(share(c,2024)); xa=x0+span*a/16; xb=x0+span*b/16
            parts += [txt(0,y-22,names[c],20,ink,weight='bold'),txt(345,y-22,'+'+n(b-a)+' điểm %',18,ink,'end'),
              line(x0,y,x0+span,y,grid,2),line(xa,y,xb,y,colors[c],4),circle(xa,y,5,colors[c],False),circle(xb,y,6,colors[c]),
              txt(0,y+24,'2015: '+n(a),18,muted),txt(345,y+24,'2024: '+n(b),18,colors[c],'end',weight='bold')]
        parts += [txt(0,516,'Phát điện nội địa; loại nhập khẩu ròng.',18,muted),txt(0,540,'Ember · 14/10/2026 · CC BY 4.0 · 5 nước',18,muted),txt(0,565,'Nhãn làm tròn; mức tăng dùng số gốc.',18,muted)]
    return svg(parts,w,h,'Tỷ trọng điện gió và mặt trời: 2015 và 2024','Việt Nam tăng từ 0,079% lên 14,697%, mức tăng lớn nhất trong năm nước. Thái Lan 5,802%, Malaysia 3,016%, Philippines 2,883%, Indonesia 0,372% năm 2024. Chênh lệch tính bằng điểm phần trăm.')
def trends(mobile=False):
    parts=[]
    if not mobile:
        w,h=940,520; x0=52; xend=680; ytop=75; ybottom=421
        parts += [txt(0,25,'Điện gió + mặt trời trong tổng phát điện (%)',22,ink,weight='bold')]
        for t in [0,4,8,12,16]:
            y=ybottom-(ybottom-ytop)*t/16
            parts += [line(x0,y,xend,y),txt(x0-14,y+7,str(t),20,muted,'end')]
        for y in years:
            x=x0+(xend-x0)*(y-2015)/9
            if y in [2015,2018,2021,2024]: parts += [txt(x,452,str(y),20,muted,'middle')]
        label_y={'VNM':106,'THA':291,'MYS':348,'PHL':390,'IDN':425}
        for c in reversed(codes):
            coords=[(x0+(xend-x0)*(y-2015)/9,ybottom-(ybottom-ytop)*float(share(c,y))/16) for y in years]
            points=' '.join(f'{x:.2f},{y:.2f}' for x,y in coords)
            parts.append(f'<polyline points="{points}" fill="none" stroke="{colors[c]}" stroke-width="{4.5 if c=="VNM" else 3}" stroke-linejoin="round"/>')
            for x,y in coords: parts.append(circle(x,y,4,colors[c]))
            x,y=coords[-1]; ly=label_y[c]
            parts += [line(x+7,y,722,ly-7,colors[c],1.5),txt(735,ly,names[c]+' '+n(share(c,2024))+'%',22,colors[c],weight='bold' if c=='VNM' else 'normal')]
        x=x0+(xend-x0)*6/9; y=ybottom-(ybottom-ytop)*float(share('VNM',2021))/16
        parts += [txt(x-22,y-20,'2021: '+n(share('VNM',2021))+'%',21,colors['VNM'],'end',weight='bold')]
        foot(parts,491)
    else:
        w,h=350,820
        parts += [txt(0,22,'Điện gió + mặt trời (%)',20,ink,weight='bold'),txt(0,48,'Cùng thang 0–16% · 2015–2024',18,muted)]
        for i,c in enumerate(codes):
            top=82+i*136; bottom=top+92; left=30; right=330
            parts += [txt(0,top,names[c],20,ink,weight='bold'),txt(345,top,n(share(c,2024))+'% (2024)',18,colors[c],'end')]
            for t in [0,8,16]:
                yy=bottom-68*t/16; parts += [line(left,yy,right,yy),txt(23,yy+5,str(t),18,muted,'end')]
            pts=[(left+(right-left)*(y-2015)/9,bottom-68*float(share(c,y))/16) for y in years]
            parts.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="none" stroke="{colors[c]}" stroke-width="3"/>')
            for x,y in pts:parts.append(circle(x,y,2.5,colors[c]))
            parts += [txt(left,bottom+23,'2015',18,muted),txt(right,bottom+23,'2024',18,muted,'end')]
        parts += [txt(0,792,'Phát điện nội địa; loại nhập khẩu ròng.',18,muted),txt(0,817,'Ember · 14/10/2026 · CC BY 4.0 · 5 nước',18,muted)]
    return svg(parts,w,h,'Diễn biến tỷ trọng điện gió và mặt trời 2015–2024','Mười quan sát thường niên cho mỗi nước, không làm trơn. Việt Nam tăng mạnh từ 2019 đến 2021, đạt 15,136% năm 2023 rồi giảm còn 14,697% năm 2024. Mọi đường dùng chung thang tỷ trọng.')
def growth(mobile=False):
    V=facts['vietnam']; parts=[]
    if not mobile:
        w,h=940,330; x0=390; span=430; yrows=[100,207]
        parts += [txt(0,25,'Việt Nam: tăng sản lượng từ 2023 đến 2024 (%)',22,ink,weight='bold')]
        for t in [0,4,8,12]:
            x=x0+span*t/12; parts += [line(x,57,x,257),txt(x,280,str(t)+'%',20,muted,'middle')]
        for y,label,a,b,g,color in [(yrows[0],'Điện gió + mặt trời',V['ws_2023_twh'],V['ws_2024_twh'],V['ws_growth_pct'],colors['VNM']),(yrows[1],'Tổng phát điện',V['total_2023_twh'],V['total_2024_twh'],V['total_growth_pct'],ink)]:
            parts += [txt(0,y-3,label,23,ink,weight='bold'),txt(0,y+27,n(a)+' → '+n(b)+' TWh',22,muted),f'<rect x="{x0}" y="{y-18}" width="{span*g/12}" height="31" fill="{color}"/>',txt(x0+span*g/12+12,y+6,'+'+n(g)+'%',23,color,weight='bold')]
        parts += [txt(0,321,'Sản lượng phát điện nội địa. Nguồn: Ember, tải 14/10/2026; CC BY 4.0.',18,muted)]
    else:
        w,h=350,390; x0=0; span=285
        parts += [txt(0,22,'Việt Nam · tăng sản lượng 2023–2024',18,ink,weight='bold')]
        for i,(label,a,b,g,color) in enumerate([('Điện gió + mặt trời',V['ws_2023_twh'],V['ws_2024_twh'],V['ws_growth_pct'],colors['VNM']),('Tổng phát điện',V['total_2023_twh'],V['total_2024_twh'],V['total_growth_pct'],ink)]):
            y=76+i*120
            parts += [txt(0,y,label,21,ink,weight='bold'),txt(0,y+29,n(a)+' → '+n(b)+' TWh',19,muted),f'<rect x="0" y="{y+45}" width="{span*g/12}" height="28" fill="{color}"/>',txt(span*g/12+10,y+66,'+'+n(g)+'%',19,color,weight='bold')]
        for t in [0,4,8,12]:parts.append(txt(span*t/12,318,str(t)+'%',18,muted,'middle' if t else 'start'))
        parts += [txt(0,349,'Phát điện nội địa; loại nhập khẩu ròng.',18,muted),txt(0,376,'Ember · 14/10/2026 · CC BY 4.0',18,muted)]
    return svg(parts,w,h,'Sản lượng gió và mặt trời vẫn tăng khi tỷ trọng giảm','Việt Nam năm 2024: điện gió và mặt trời tăng 6,96% từ 42,683 lên 45,655 TWh; tổng phát điện tăng 10,15% từ 282,000 lên 310,633 TWh. Tổng tăng nhanh hơn nên tỷ trọng gió và mặt trời giảm. Đây là quan hệ số học, không xác định nguyên nhân chính sách hoặc lưới điện.')
charts = {'comparison':comparison(),'comparison-mobile':comparison(True),'trend':trends(),'trend-mobile':trends(True),'growth':growth(),'growth-mobile':growth(True)}
chartdir=out/'charts'; chartdir.mkdir(exist_ok=True)
for name,s in charts.items(): (chartdir/(name+'.svg')).write_text(s,encoding='utf-8')
def inline(name):
    return charts[name].replace('aria-labelledby="title desc"',f'aria-labelledby="{name}-title {name}-desc"').replace('id="title"',f'id="{name}-title"').replace('id="desc"',f'id="{name}-desc"')
def chart(name): return f'<div class="chart desktop" data-essential>{inline(name)}</div><div class="chart mobile" data-essential>{inline(name+"-mobile")}</div>'
def footer(page):return f'<footer><span>Ember · dữ liệu 2015–2024 · tải 14/10/2026</span><span>{page} / 4</span></footer>'
V=facts['vietnam']
data_rows=''.join('<tr><th scope="row">'+str(y)+'</th>'+''.join('<td>'+n(share(c,y))+'</td>' for c in codes)+'</tr>' for y in years)
css='''
:root{--paper:#faf8f1;--ink:#1d2b31;--teal:#00695e;--muted:#47575d;--rule:#d7dcd8}
*{box-sizing:border-box}body{margin:0;background:#e9ede8;color:var(--ink);font:19px/1.55 Arial,sans-serif}
a{color:var(--teal);text-underline-offset:3px}nav{max-width:1120px;margin:22px auto;display:flex;gap:20px;align-items:center;padding:0 22px;font-size:16px}nav a{font-weight:bold}nav .print{margin-left:auto}
.page{max-width:1120px;margin:0 auto 30px;padding:46px 58px 35px;background:var(--paper);min-height:1090px;display:flex;flex-direction:column;box-shadow:0 2px 12px #1d2b310b}
.eyebrow{font-size:16px;letter-spacing:.09em;text-transform:uppercase;margin:0 0 27px;color:var(--muted)}h1,h2{font-family:Georgia,'Times New Roman',serif;font-weight:normal;letter-spacing:-.026em;line-height:1.12;margin:0 0 22px}h1{font-size:45px}h2{font-size:42px}h3{font-size:21px;line-height:1.35;margin:0 0 10px}p{margin:0 0 17px}.lead{font-size:21px;line-height:1.5;max-width:970px}.kicker{font-size:17px;color:var(--teal);font-weight:bold;margin:10px 0 12px}.chart{margin:20px 0 12px}.chart svg{width:100%;height:auto;display:block;overflow:visible}.mobile{display:none}.note{font-size:18px;color:var(--muted)}.decision{border-left:4px solid var(--teal);padding-left:20px;margin:18px 0 22px}.decision p:last-child{margin-bottom:0}.two{display:grid;grid-template-columns:1fr 1fr;gap:42px;margin:25px 0}.limit{border-top:1px solid var(--rule);padding-top:19px;margin-top:22px}.metric{font-size:30px;line-height:1.2;margin-bottom:14px;font-family:Georgia,'Times New Roman',serif}.metric strong{color:var(--teal);font-weight:normal}.action-step{display:grid;grid-template-columns:90px 1fr;gap:20px;padding:18px 0;border-top:1px solid var(--rule)}.action-step .day{color:var(--teal);font-weight:bold}.source{font-size:16px;line-height:1.5;color:var(--muted);border-top:1px solid var(--rule);padding-top:17px;margin-top:23px}.source p{margin-bottom:10px}footer{display:flex;justify-content:space-between;gap:15px;border-top:1px solid var(--rule);padding-top:17px;margin-top:auto;font-size:16px;color:var(--muted)}details{margin:10px 0 22px;font-size:17px}summary{cursor:pointer;font-weight:bold;color:var(--teal);padding:10px 0}table{width:100%;border-collapse:collapse;font-size:17px}th,td{padding:9px 10px;border-bottom:1px solid var(--rule);text-align:right;font-variant-numeric:tabular-nums}th:first-child,td:first-child{text-align:left}.table-scroll{overflow:auto}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:700px){body{font-size:18px}nav{gap:15px;flex-wrap:wrap;margin:12px auto;padding:0 20px}nav .print{margin-left:0}.page{margin:0 0 16px;padding:28px 20px 28px;min-height:0;box-shadow:none}.eyebrow{font-size:16px;letter-spacing:.04em;margin-bottom:22px}h1{font-size:35px}h2{font-size:32px}.lead{font-size:19px}.desktop{display:none}.mobile{display:block}.chart{margin:22px 0}.two{grid-template-columns:1fr;gap:14px}.note{font-size:18px}.decision{padding-left:16px}.metric{font-size:27px}.action-step{grid-template-columns:58px 1fr;gap:12px}.source{font-size:16px}footer{margin-top:26px;font-size:16px}footer span:first-child{max-width:245px}table{font-size:16px;min-width:590px}}
@page{size:A4 portrait;margin:0}
@media print{html,body{background:white}body{font-size:12pt;line-height:1.46}nav,details{display:none!important}.page{width:210mm;height:297mm;min-height:297mm;max-width:none;margin:0;padding:15mm 16mm 12mm;box-shadow:none;break-after:page;page-break-after:always;overflow:hidden}.page:last-child{break-after:auto}.eyebrow{font-size:9.5pt;margin-bottom:7mm}h1{font-size:28pt;margin-bottom:5mm}h2{font-size:27pt;margin-bottom:5mm}h3{font-size:13pt}.lead{font-size:13pt;line-height:1.45}.kicker{font-size:10.5pt;margin:3mm 0 1mm}p{margin-bottom:4mm}.chart{margin:4mm 0 2mm}.desktop{display:block}.mobile{display:none}.note{font-size:11.5pt}.decision{margin:4mm 0 5mm;padding-left:4mm}.two{gap:9mm;margin:6mm 0}.metric{font-size:20pt}.limit{padding-top:4mm;margin-top:5mm}.action-step{grid-template-columns:19mm 1fr;gap:4mm;padding:4mm 0}.source{font-size:10pt;line-height:1.42;margin-top:5mm;padding-top:4mm}.source p{margin-bottom:3mm}footer{font-size:9pt;padding-top:4mm}a{color:inherit;text-decoration:none}}
'''
doc=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Điện gió và mặt trời: khoảng cách mở rộng, tỷ trọng không tăng đều</title><style>{css}</style></head><body>
<nav aria-label="Mục lục"><a href="#angle">Góc bài</a><a href="#trajectory">Diễn biến</a><a href="#denominator">Ngoại lệ 2024</a><a href="#assignment">Giao việc</a><a class="print" href="javascript:window.print()">In / lưu PDF</a></nav>
<main>
<section class="page" id="angle" data-essential>
<p class="eyebrow">Bản họp biên tập · Đề xuất góc bài · Chưa xuất bản</p>
<h1>Việt Nam mở rộng khoảng cách.<br>Tỷ trọng năm 2024 lại giảm nhẹ.</h1>
<p class="lead">Trong năm nước được so sánh, Việt Nam tăng tỷ trọng điện gió và mặt trời nhiều nhất giai đoạn 2015–2024. Nhưng vị trí dẫn đầu không đồng nghĩa tỷ trọng sẽ tăng mỗi năm.</p>
<p class="kicker">So sánh đầu kỳ và cuối kỳ</p>
{chart('comparison')}
<div class="decision"><p><strong>Góc chính đề xuất:</strong> lấy Việt Nam làm trục bài, đặt trong so sánh năm nước: bước chuyển lớn của điện gió và mặt trời, cùng câu hỏi vì sao sản lượng vẫn tăng mà tỷ trọng năm 2024 giảm.</p></div>
<p class="note">Năm 2024, Việt Nam cao hơn Thái Lan <strong>{n(V['gap_thailand_2024_pp'])} điểm phần trăm</strong>. Đây là so sánh cơ cấu phát điện trong nhóm đã chọn, không phải bảng xếp hạng toàn ASEAN hay mức độ thành công của chính sách.</p>
{footer(1)}</section>

<section class="page" id="trajectory" data-essential>
<p class="eyebrow">02 · Đọc cả chặng đường</p>
<h2>Khoảng cách hình thành chủ yếu<br>trong bước tăng 2019–2021.</h2>
<p class="lead">Tại Việt Nam, tỷ trọng đi từ <strong>{n(V['share_2018_pct'])}% năm 2018</strong> lên <strong>{n(V['share_2021_pct'])}% năm 2021</strong>. Bốn nước còn lại đều dưới 6% vào năm 2024, nhưng có nhịp thay đổi riêng.</p>
{chart('trend')}
<p>Thái Lan tăng sớm hơn và đạt <strong>{n(share('THA',2024))}%</strong> năm 2024. Malaysia tiếp tục tăng về cuối kỳ; Philippines thay đổi ít hơn; Indonesia vẫn dưới 1%. Đường thời gian cho thấy sự khác biệt này rõ hơn một con số tăng trưởng chung.</p>
<p class="note limit">Bước nhảy trong dữ liệu xác định <strong>thời điểm cần tìm hiểu</strong>, chưa xác định nguyên nhân. Không thể từ các đường này quy mức tăng cho một chính sách cụ thể.</p>
<details><summary>Xem tỷ trọng từng năm của cả năm nước</summary><div class="table-scroll"><table><caption>Tỷ trọng điện gió + mặt trời trong phát điện nội địa (%), làm tròn hai chữ số</caption><thead><tr><th>Năm</th>{''.join('<th>'+names[c]+'</th>' for c in codes)}</tr></thead><tbody>{data_rows}</tbody></table></div></details>
{footer(2)}</section>

<section class="page" id="denominator" data-essential>
<p class="eyebrow">03 · Ngoại lệ làm rõ ý nghĩa của tỷ trọng</p>
<h2>Sản lượng tăng,<br>nhưng tổng phát điện tăng nhanh hơn.</h2>
<p class="lead">Ở Việt Nam, điện gió và mặt trời vẫn sản xuất thêm điện trong năm 2024. Tỷ trọng giảm vì mức tăng của hai nguồn này thấp hơn mức tăng của tổng phát điện.</p>
{chart('growth')}
<div class="two">
<div><h3>Tỷ trọng trong tổng phát điện</h3><p class="metric">{n(V['share_2023_pct'])}% <span aria-hidden="true">→</span> <strong>{n(V['share_2024_pct'])}%</strong></p><p>2023 → 2024: giảm <strong>{n(-V['change_2023_2024_pp'])} điểm phần trăm</strong>. Đó là thay đổi của một tỷ lệ, dù lượng điện gió và mặt trời tăng.</p></div>
<div><h3>Mẫu số quyết định cách đọc</h3><p>Tỷ trọng = lượng điện gió + mặt trời ÷ tổng lượng điện phát trong nước. Nhập khẩu ròng không nằm trong mẫu số; tỷ trọng này không phải tỷ trọng tiêu thụ điện.</p></div>
</div>
<p class="note limit">Đây là quan hệ số học trong bộ dữ liệu. Nó chưa cho biết vì sao từng nguồn điện thay đổi, và không chứng minh thiếu điện, giá điện, chất lượng lưới hoặc tác động của một can thiệp.</p>
{footer(3)}</section>

<section class="page" id="assignment" data-essential>
<p class="eyebrow">04 · Một việc có thể giao ngay · Đề xuất</p>
<h2>Hai ngày để kiểm tra<br>cách đọc ngoại lệ của Việt Nam.</h2>
<div class="decision"><p><strong>Giao một phóng viên đối chiếu số phát điện 2023–2024.</strong> Câu hỏi: chênh lệch tăng trưởng điện gió + mặt trời và tổng phát điện có được xác nhận trên cùng phạm vi thống kê, đặc biệt với điện mặt trời phân tán?</p></div>
<div class="action-step"><div class="day">Ngày 1</div><div><h3>Lấy số và định nghĩa đi cùng nhau</h3><p>Kiểm tra báo cáo năm 2023, 2024 của EVN; bảng và phương pháp nguồn EI được Ember dẫn. Tách phát điện trong nước khỏi điện mua/nhập khẩu; ghi rõ phạm vi điện mặt trời mái nhà và điện tự sản xuất.</p></div></div>
<div class="action-step"><div class="day">Ngày 2</div><div><h3>Giao một trang đối chiếu có nguồn</h3><p>Ghi số gió + mặt trời, tổng phát điện và phạm vi của từng năm; đính kèm trang/bảng gốc. Nếu còn lệch định nghĩa, lập câu hỏi gửi Ember hoặc đơn vị báo cáo để xác minh, không tự ghép hai phạm vi.</p></div></div>
<div class="limit"><h3>Biên tập viên quyết định cuối ngày 2</h3><p>Đưa phần giải thích về chênh lệch tăng trưởng vào bài khi số liệu hai năm đối chiếu được và cùng định nghĩa, cùng phạm vi. Nếu chưa đạt, giữ mô tả theo Ember, ghi điểm chưa xác minh; chưa viết kết luận về nguyên nhân chính sách hoặc lưới điện.</p></div>
<div class="source"><p><strong>Nguồn và cách đọc.</strong> Ember, <em>Yearly Electricity Data</em>, bản tải 14/10/2026, nguồn cập nhật 06/10/2026; lọc Việt Nam, Thái Lan, Malaysia, Philippines, Indonesia trong 2015–2024. Dùng tỷ trọng gộp do Ember công bố; mức tăng dài hạn tính bằng điểm phần trăm. Số hiển thị được làm tròn; phép tính giữ độ chính xác nguồn.</p><p><strong>Giới hạn bao phủ.</strong> Phương pháp Ember (bản 22/09/2026) lưu ý điện phân tán và điện tự sản xuất có thể được ước tính hoặc thiếu trong thống kê; Indonesia có ước tính điện tự sản xuất. Dữ liệu này không đại diện toàn ASEAN.</p><p><a href="https://ember-energy.org/data/yearly-electricity-data/">Ember: dữ liệu</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Phân tích và trình bày riêng, không hàm ý Ember xác nhận. Đây là đề xuất công việc biên tập; chưa có bài được duyệt hoặc xuất bản.</p></div>
{footer(4)}</section>
</main></body></html>'''
doc = doc.replace('class="page" id="angle" data-essential','class="page" id="angle"').replace('class="page" id="trajectory" data-essential','class="page" id="trajectory"').replace('class="page" id="denominator" data-essential','class="page" id="denominator"').replace('class="page" id="assignment" data-essential','class="page" id="assignment"')
doc = re.sub(r'<(p|h[123])(?=[ >])', r'<\1 data-essential', doc)
doc = doc.replace('<footer>', '<footer data-essential>').replace('class="action-step"', 'class="action-step" data-essential')
(out/'energy-editorial.vi.html').write_text(doc,encoding='utf-8')
calculation_note=f'''# Phép tính và căn cứ cho bản biên tập

## Nguồn đóng băng
Ember Yearly Electricity Data. CSV tải 14/10/2026, nguồn được sửa lần cuối 06/10/2026. SHA-256: `{facts['source_sha256']}`. Giấy phép CC BY 4.0. Phân tích, lọc và trình bày riêng, không hàm ý Ember xác nhận.

Grain: ISO + năm + nguồn điện. 200 hàng = 5 nước × 10 năm × 4 nguồn. Dòng `Wind and solar` là tổng gộp, chồng lặp `Wind` và `Solar`; tuyệt đối không cộng cả ba dòng. Tỷ trọng công bố của tổng gộp là chỉ tiêu chuẩn cho biểu đồ; mẫu số là phát điện nội địa, loại nhập khẩu ròng.

## Công thức
- Chênh lệch dài hạn (điểm phần trăm) = tỷ trọng công bố 2024 − tỷ trọng công bố 2015.
- Đối chiếu tỷ trọng = TWh gió + mặt trời ÷ TWh tổng phát điện × 100.
- Tăng sản lượng 2023–2024 (%) = (TWh 2024 ÷ TWh 2023 − 1) × 100.
- Chênh lệch giữa nước = hai tỷ trọng cùng năm trừ nhau; không lấy tỷ lệ tăng tương đối từ các nền thấp làm góc chính.
- Hiển thị tiếng Việt dùng dấu phẩy thập phân, làm tròn nửa lên đến 2 chữ số. Phép tính dùng Decimal và độ chính xác CSV.

## Số quyết định
| Nước | 2015 (%) | 2024 (%) | Tăng (điểm phần trăm) |
|---|---:|---:|---:|
'''+''.join(f'| {names[c]} | {share(c,2015)} | {share(c,2024)} | {share(c,2024)-share(c,2015)} |\n' for c in codes)+f'''
Việt Nam 2023–2024: gió + mặt trời {gen('VNM',2023)} → {gen('VNM',2024)} TWh (+{V['ws_growth_pct']:.12f}%); tổng phát điện {gen('VNM',2023,'Total generation')} → {gen('VNM',2024,'Total generation')} TWh (+{V['total_growth_pct']:.12f}%). Tỷ trọng {share('VNM',2023)} → {share('VNM',2024)}%, chênh lệch {V['change_2023_2024_pp']} điểm phần trăm. Khoảng cách với Thái Lan năm 2024: {V['gap_thailand_2024_pp']} điểm phần trăm.

## Kiểm tra đã thực thi khi dựng
Không trùng khóa; đủ mọi tổ hợp ISO/năm/nguồn; không thiếu hai cột quyết định; tổng phát điện dương. Cả 50 quan sát gộp đối chiếu với tổng hai thành phần và mẫu số. Dung sai 0,001 TWh hoặc 0,001 điểm phần trăm cho sai khác làm tròn. Kết quả chi tiết trong facts.json/reconciliation và annual-calculations.csv. Tỷ trọng gộp có thể lệch tổng hai tỷ trọng thành phần 0,001 điểm do làm tròn (ví dụ Việt Nam 2024).

## Căn cứ diễn giải và giới hạn
Góc chọn: khoảng cách tỷ trọng của Việt Nam mở rộng trong nhóm năm nước, nhưng tỷ trọng 2024 giảm dù sản lượng tăng. Quan hệ mẫu số đủ giải thích hiện tượng số học; dữ liệu không phân biệt nguyên nhân chính sách, điều kiện tự nhiên, huy động, báo cáo hay lưới điện. Một năm giảm không chứng minh xu hướng suy giảm dài hạn. Không đại diện toàn ASEAN; không đo tiêu thụ/công suất, độ đầy đủ điện, giá hay tác động can thiệp.

Phương pháp Ember trang vật lý 9–10 định nghĩa phát điện và loại nhập khẩu; trang 13 nêu giới hạn captive/distributed generation; trang 50 mô tả ước tính điện tự sản xuất Indonesia; trang 60/72/86–87/93 mô tả các nguồn năm. Cảnh báo điện gió Việt Nam trước 2022 ở trang 93 là cho chuỗi tháng EVN; không chuyển nó thành kết luận về mọi quan sát năm dùng ở đây.

## Vai trò và trạng thái
Bản này là đề xuất họp biên tập. Phóng viên đề xuất: đối chiếu số và phạm vi trong 2 ngày làm việc. Biên tập viên: quyết định cuối ngày 2 theo điều kiện trên trang 4. Chưa giao người cụ thể, chưa gửi câu hỏi, chưa duyệt hoặc xuất bản. Nguồn ngoài được nêu ở trang 4 là việc cần kiểm tra tiếp, không phải dữ liệu mới dùng cho bản này.
'''
(out/'calculations.vi.md').write_text(calculation_note,encoding='utf-8')
print(json.dumps({'html':str(out/'energy-editorial.vi.html'),'csv_rows':len(rows),'observations':len(reconciliation),'checks':'source hash, key domain, component and denominator reconciliations passed'},ensure_ascii=False))
