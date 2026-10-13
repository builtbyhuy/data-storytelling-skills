import argparse,json,csv,zipfile,hashlib,re
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
import xml.etree.ElementTree as ET
import openpyxl
from pypdf import PdfReader
import pypdfium2 as pdfium

p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
f=json.loads((a.build_dir/'facts.json').read_text(encoding='utf-8'))
book=openpyxl.load_workbook(a.output_dir/'tong-hop-chuyen-can.xlsx',data_only=False)
cache=openpyxl.load_workbook(a.output_dir/'tong-hop-chuyen-can.xlsx',data_only=True)
assert book.sheetnames==['Tong hop','Dia ban','Nguon']
raw=list(csv.DictReader((a.source_dir/'raw/absence-geographic-autumn.csv').open(encoding='utf-8-sig')))
scope=[r for r in raw if r['time_identifier']=='Autumn term' and r['time_period'] in f['periods'] and r['geographic_level']=='Local authority' and r['education_phase'] in ['State-funded primary','State-funded secondary']]
totals=defaultdict(lambda:defaultdict(int))
for r in scope:
 for field in ['enrolments','enrolments_pa_10_exact','enrolments_pa_50_exact','sess_possible','sess_overall']:
  totals[(r['time_period'],r['education_phase'])][field]+=int(r[field])
checked=[]
for r in f['national']:
 t=totals[(r['period'],r['phase'])]
 for key,nu,de in [('pa','enrolments_pa_10_exact','enrolments'),('severe','enrolments_pa_50_exact','enrolments'),('overall','sess_overall','sess_possible')]:
  v=Decimal(t[nu])/Decimal(t[de]);assert abs(float(v)-r[key])<1e-14;checked.append((r['period'],r['phase'],key,float(v)))
for i,r in enumerate(f['local'],7):
 assert cache['Dia ban'].cell(i,1).value==r['code']
 for col,val in [(4,r['old']['pa']),(5,r['new']['pa']),(6,r['delta']['pa']*100),(7,r['old']['severe']),(8,r['new']['severe']),(9,r['delta']['severe']*100),(10,r['new']['pa_less_severe']),(11,r['new']['illness']),(12,r['new']['other_unauthorised'])]:
  cv=cache['Dia ban'].cell(i,col).value
  assert isinstance(cv,(int,float)),(i,col,cv)
  assert abs(cv-val)<1e-10,(i,col,cv,val)
for phase,rownum in [('State-funded primary',7),('State-funded secondary',8)]:
 old=next(x for x in f['national'] if x['phase']==phase and x['period']=='202425')
 new=next(x for x in f['national'] if x['phase']==phase and x['period']=='202526')
 for col,val in [(2,old['enrolments']),(3,new['enrolments']),(4,old['pa']),(5,new['pa']),(6,(new['pa']-old['pa'])*100),(7,old['severe']),(8,new['severe']),(9,(new['severe']-old['severe'])*100)]:assert abs(cache['Tong hop'].cell(rownum,col).value-val)<1e-10
ns=next(x for x in f['national'] if x['phase']=='State-funded secondary' and x['period']=='202526')
for col,val in [(6,ns['pa_less_severe']),(7,ns['illness']),(8,ns['other_unauthorised']),(9,ns['num_schools'])]:assert abs(cache['Tong hop'].cell(21,col).value-val)<1e-10
error_cells=[(s.title,c.coordinate,c.value) for s in cache for row in s for c in row if c.data_type=='e'];assert not error_cells,error_cells
formulas=sum(c.data_type=='f' for s in book for row in s for c in row)
pdf=a.output_dir/'thu-nghiem-chuyen-can.pdf';reader=PdfReader(pdf);assert len(reader.pages)==9
texts=[p.extract_text() or '' for p in reader.pages]
(a.build_dir/'pdf-text.txt').write_text('\n\n'.join(texts),encoding='utf-8')
for i,t in enumerate(texts):assert len(t)>150,(i,len(t))
document=pdfium.PdfDocument(pdf)
render=a.build_dir/'pdf-pages';render.mkdir(exist_ok=True)
for i in range(len(document)):
 document[i].render(scale=1.5).to_pil().save(render/f'page-{i+1:02d}.png')
for q in (a.build_dir/'native-sheets').glob('*.pdf'):
 d=pdfium.PdfDocument(q);d[0].render(scale=1.5).to_pil().save(q.with_suffix('.png'))
native=json.loads((a.build_dir/'native-receipt.json').read_text(encoding='utf-8-sig'))
assert native['powerpoint_opened'] and native['excel_opened'] and native['pdf_exported_from_actual_pptx']
assert [x['native_charts'] for x in native['slides']]==[0,1,1,1,0,0,0,0,0]
assert [x['native_tables'] for x in native['slides']]==[0,0,0,0,1,1,1,0,0]
if native.get('tests'):assert all(x['passed'] for x in native['tests'])
with zipfile.ZipFile(a.output_dir/'thu-nghiem-chuyen-can.pptx') as z:
 for name in ['ppt/slides/slide2.xml','ppt/slides/slide3.xml','ppt/slides/slide4.xml']:
  assert b'graphicFrame' in z.read(name)
 for i in range(1,10):assert b'<a:t>' in z.read(f'ppt/slides/slide{i}.xml')
 names=['Knowsley','North East Lincolnshire','Blackburn with Darwen']
 selected=[next(r for r in f['local'] if r['phase']=='State-funded secondary' and r['name']==n) for n in names]
 nat=lambda ph,t:next(r for r in f['national'] if r['phase']==ph and r['period']==t)
 expected=[(['Tiểu học','Trung học'],[[nat(ph,t)['pa'] for ph in ['State-funded primary','State-funded secondary']] for t in ['202425','202526']]),(['Tiểu học','Trung học'],[[nat(ph,t)['severe'] for ph in ['State-funded primary','State-funded secondary']] for t in ['202425','202526']]),(names,[[r[period]['pa'] for r in selected] for period in ['old','new']])]
 namespace={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
 charts=sorted([n for n in z.namelist() if re.match(r'ppt/(?:slides/)?charts/chart\d+\.xml$',n)],key=lambda n:int(re.search(r'chart(\d+)',n).group(1)))
 assert len(charts)==3
 for chart,(categories,values) in zip(charts,expected):
  dom=ET.fromstring(z.read(chart));series=dom.findall('.//c:barChart/c:ser',namespace);assert len(series)==2
  for i,ser in enumerate(series):
   cat=[n.text for n in ser.findall('.//c:cat//c:pt/c:v',namespace)]
   nums=[float(n.text) for n in ser.findall('.//c:val//c:pt/c:v',namespace)]
   assert cat==categories,(chart,cat,categories)
   assert len(nums)==len(values[i])
   assert all(abs(x-round(y,6))<1e-14 for x,y in zip(nums,values[i]))
 embeddings=[n for n in z.namelist() if n.endswith('.xlsx') and '/embeddings/' in n]
 assert len(embeddings)==3,embeddings
 for pageindex,categories,values in [(1,expected[0][0],expected[0][1]),(2,expected[1][0],expected[1][1]),(3,expected[2][0],expected[2][1])]:
  for v in sum(values,[]):assert f'{v*100:.2f}%' in texts[pageindex],(pageindex,v)
receipt={'raw_sha256':hashlib.sha256((a.source_dir/'raw/absence-geographic-autumn.csv').read_bytes()).hexdigest(),'source_rows':len(scope),'national_rates_checked_with_decimal':checked,'all_304_local_formula_rows_matched':True,'main_summary_and_england_reason_rates_matched':True,'all_three_native_chart_category_domains_and_values_matched':True,'chart_snapshot_precision':'Rate fractions rounded to 6 decimal places for Excel-compatible chart snapshots. Labels show 2 decimal percentage points. Workbook calculations retain full count-based precision.','embedded_chart_workbooks':len(embeddings),'pdf_chart_labels_matched':True,'formula_cells':formulas,'cached_formula_errors':error_cells,'pdf_pages':len(reader.pages),'pdf_export':'PowerPoint SaveCopyAs from delivered PPTX','native_powerpoint_and_excel_opened':True,'native_charts':3,'native_tables':3,'editability_limit':'Charts contain embedded snapshot workbooks. Rebuild required for source refresh. Native text and tables editable.','files':{q.name:{'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in a.output_dir.glob('*') if q.suffix in ('.pptx','.pdf','.xlsx')}}
(a.build_dir/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['national_rates_checked_with_decimal','files']},ensure_ascii=False,indent=2))
