import argparse,csv,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
import pdfplumber

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--receipt',type=Path,required=True)
a=p.parse_args()
out=a.out.resolve(); source=a.source.resolve()
(out/'checks').mkdir(exist_ok=True)
raw=source/'raw/ember-generation-five-countries-2015-2024.csv'
data=list(csv.DictReader(raw.open(encoding='utf-8',newline='')))
f=json.loads((out/'facts.json').read_text(encoding='utf-8'))
checks=[]
def check(name,result,detail=None):
    checks.append({'check':name,'passed':bool(result),**({'detail':detail} if detail is not None else {})})
by={(x['ISO 3 code'],int(x['Year']),x['Electricity source']):x for x in data}
check('frozen source hash',hashlib.sha256(raw.read_bytes()).hexdigest()==f['source_sha256'])
check('200 unique complete source records',len(data)==len(by)==200)
for c,values in f['countries'].items():
    # Independent binary arithmetic from source rows, separate from Decimal production path.
    arr=[float(by[c,y,'Wind and solar']['Share of generation (%)']) for y in range(2015,2025)]
    check(c+' annual values',arr==values['annual_shares_pct'])
    check(c+' endpoint pp difference',abs(arr[-1]-arr[0]-values['change_2015_2024_pp'])<1e-10)
    for y in range(2015,2025):
        ws=float(by[c,y,'Wind and solar']['Generation (TWh)']); total=float(by[c,y,'Total generation']['Generation (TWh)'])
        check(c+str(y)+' denominator',abs(ws/total*100-arr[y-2015])<=0.001)
v=f['vietnam']
for metric,source_name in [('ws_growth_pct','Wind and solar'),('total_growth_pct','Total generation')]:
    v23=float(by['VNM',2023,source_name]['Generation (TWh)']); v24=float(by['VNM',2024,source_name]['Generation (TWh)'])
    check(metric+' independently recomputed',abs((v24/v23-1)*100-v[metric])<1e-10)
check('Vietnam latest share falls despite both quantities rising',v['change_2023_2024_pp']<0 and v['total_growth_pct']>v['ws_growth_pct']>0)
pdf=PdfReader(out/'energy-editorial.vi.pdf')
check('PDF four pages',len(pdf.pages)==4)
page_info=[]
with pdfplumber.open(out/'energy-editorial.vi.pdf') as doc:
    for i,page in enumerate(doc.pages):
        text=page.extract_text() or ''
        (out/'checks'/f'pdf-page-{i+1}.txt').write_text(text,encoding='utf-8')
        info={'page':i+1,'text_characters':len(page.chars),'lines':len(page.lines),'rectangles':len(page.rects),'curves':len(page.curves),'images':len(page.images),'width_pt':page.width,'height_pt':page.height}
        page_info.append(info)
        check('PDF page '+str(i+1)+' vector text and no image',len(page.chars)>500 and len(page.images)==0 and len(pdf.pages[i].images)==0,info)
        check('PDF page '+str(i+1)+' visible footer',f'{i+1} / 4' in text)
check('PDF contains chart vector paths',sum(x['lines']+x['curves'] for x in page_info)>100)
for svg_path in sorted((out/'charts').glob('*.svg')):
    root=ET.fromstring(svg_path.read_text(encoding='utf-8'))
    ns='{http://www.w3.org/2000/svg}'
    check(svg_path.name+' editable text / no raster',len(list(root.iter(ns+'text')))>10 and not list(root.iter(ns+'image')))
    check(svg_path.name+' source date and license', '14/10/2026' in svg_path.read_text(encoding='utf-8') and 'CC BY 4.0' in svg_path.read_text(encoding='utf-8'))
ns='{http://www.w3.org/2000/svg}'
country_colors={'VNM':'#00695e','THA':'#9c5414','MYS':'#315f80','PHL':'#6b526f','IDN':'#4e5860'}
trend_root=ET.parse(out/'charts/trend.svg').getroot()
axis_text=list(trend_root.iter(ns+'text'))
x15=float(next(x.attrib['x'] for x in axis_text if x.text=='2015'))
x24=float(next(x.attrib['x'] for x in axis_text if x.text=='2024'))
y0=float(next(x.attrib['y'] for x in axis_text if x.text=='0'))-7
y16=float(next(x.attrib['y'] for x in axis_text if x.text=='16'))-7
for c,color in country_colors.items():
    poly=next(p for p in trend_root.iter(ns+'polyline') if p.attrib['stroke']==color)
    pts=[tuple(map(float,p.split(','))) for p in poly.attrib['points'].split()]
    expected=[(x15+(x24-x15)*(year-2015)/9,y0-(y0-y16)*float(by[c,year,'Wind and solar']['Share of generation (%)'])/16) for year in range(2015,2025)]
    check(c+' plotted full-year coordinates',len(pts)==10 and all(abs(x-e[0])<.011 and abs(y-e[1])<.011 for (x,y),e in zip(pts,expected)))
comparison_root=ET.parse(out/'charts/comparison.svg').getroot()
texts=list(comparison_root.iter(ns+'text'))
x0=float(next(t.attrib['x'] for t in texts if t.text=='0'))
x16=float(next(t.attrib['x'] for t in texts if t.text=='16'))
for c,color in country_colors.items():
    dots=[p for p in comparison_root.iter(ns+'circle') if p.attrib['stroke']==color]
    expected=[x0+(x16-x0)*float(by[c,y,'Wind and solar']['Share of generation (%)'])/16 for y in [2015,2024]]
    check(c+' comparison endpoint coordinates',len(dots)==2 and all(abs(float(p.attrib['cx'])-e)<1e-8 for p,e in zip(dots,expected)))
screen=json.loads(a.receipt.read_text(encoding='utf-8'))
check('browser 1280/390/360 checks',screen['passed'] and [x['width'] for x in screen['views']]==[1280,390,360])
def luminance(h):
    vals=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
    return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
bg=luminance('#faf8f1')
contrast={color:(bg+.05)/(luminance(color)+.05) for color in ['#1d2b31','#47575d','#00695e','#9c5414','#315f80','#6b526f','#4e5860']}
check('essential text and chart colors contrast >=4.5',all(x>=4.5 for x in contrast.values()),contrast)
report={'passed':all(c['passed'] for c in checks),'checks':checks,'pdf_page_objects':page_info,'helper_sha256':hashlib.sha256((Path(__file__).parent/'export_web.mjs').read_bytes()).hexdigest(),
        'limits':['Object, arithmetic and browser checks do not establish human taste, comprehension, approval or editorial outcomes.','Visual inspection of actual PDF and browser pages is recorded separately in README-rebuild.vi.md.']}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':[c for c in checks if not c['passed']]},ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
