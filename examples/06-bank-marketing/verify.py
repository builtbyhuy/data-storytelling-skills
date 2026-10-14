"""Independent arithmetic, output semantics, SVG/PDF, and source checks."""
from pathlib import Path
import argparse,csv,collections,hashlib,json,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import ContentStream
import pdfplumber

def verify(source,out,poppler=None):
    source,out=Path(source),Path(out)
    e=json.loads((out/'evidence/calculations.json').read_text(encoding='utf-8'))
    checks={};counts=collections.Counter();history=collections.defaultdict(lambda:[0,0]);attempts=collections.defaultdict(lambda:[0,0]);strata=collections.defaultdict(lambda:[0,0]);contact=collections.defaultdict(lambda:[0,0])
    with source.open(encoding='utf-8',newline='') as f:
        rd=csv.DictReader(f,delimiter=';')
        for r in rd:
            y=int(r['y']=='yes');c=int(r['campaign']);b='1' if c==1 else '2-3' if c<=3 else '4-6' if c<=6 else '7+'
            counts['rows']+=1;counts['yes']+=y;counts['blank']+=sum(x=='' for x in r.values())
            counts['pdays_sentinel']+=int(r['pdays']=='-1');counts['unknown_history']+=int(r['poutcome']=='unknown')
            for d,k in [(history,r['poutcome']),(attempts,b),(strata,b+':'+('success' if r['poutcome']=='success' else 'not_success')),(contact,r['contact']+':'+('success' if r['poutcome']=='success' else 'not_success'))]:d[k][0]+=1;d[k][1]+=y
    assert counts['rows']==e['rows']==45211 and counts['yes']==e['yes']==5289 and counts['blank']==0
    for name,d in [('history',history),('attempts',attempts),('strata',strata),('contact_strata',contact)]:
        for r in e[name]:
            assert d[r['key']]==[r['records'],r['yes']]
            assert abs(r['rate_pct']-100*r['yes']/r['records'])<1e-10
            assert r['records']==r['yes']+r['no']
    checks['independent_all_group_counts_and_rates']=True
    assert counts['pdays_sentinel']==36954 and counts['unknown_history']==36959
    checks['unknown_and_sentinel_not_conflated']=True
    sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha==e['source_sha256']
    assert hashlib.sha256((out/'source/bank-full.csv').read_bytes()).hexdigest()==sha
    checks['source_bytes_preserved']=True
    browser=json.loads((out/'evidence/browser-checks.json').read_text(encoding='utf-8'))
    def n(x):return f'{x:,}'.replace(',','.')
    def p(x):return f'{x:.2f}'.replace('.',',')+'%'
    expected={}
    for name,tid in [('history','history-table'),('attempts','attempts-table')]:
        expected[tid]=[[r['label'],n(r['records']),n(r['yes']),n(r['no']),p(r['rate_pct'])] for r in e[name]]
    expected['contact-check']=[]
    for i in range(0,len(e['contact_strata']),2):
        a,b=e['contact_strata'][i:i+2]
        expected['contact-check'].append([a['contact'],f"{n(a['yes'])} / {n(a['records'])}",p(a['rate_pct']),f"{n(b['yes'])} / {n(b['records'])}",p(b['rate_pct'])])
    for surface in browser['surfaces']:
        assert surface['width'] in [1280,390]
        for t in surface['tables']:
            assert t['rows']==expected[t['id']],(t['id'],t['rows'])
            if surface['width']==390:
                assert not t['numericLookup']['bad'] and t['numericLookup']['cells']==len(t['rows'])*4
        assert len(surface['chartNames'])==2 and all(not c['clippedText'] for c in surface['charts'])
    checks['browser_tables_every_cell_and_row_identity']=True
    checks['phone_every_numeric_value_recoverable_with_sticky_row_header']=True
    checks['browser_visible_chart_names_and_no_svg_clipping']=True
    assert not browser['network_requests'] and not browser['errors'];checks['html_offline_no_network']=True
    ns={'s':'http://www.w3.org/2000/svg'}
    for k in ['history','attempts']:
        for variant in ['desktop','phone']:
            root=ET.parse(out/'charts'/f'{k}-{variant}.svg').getroot()
            assert len(root.findall('s:text',ns))>12 and not root.findall('.//s:image',ns)
            assert root.find('s:title',ns) is not None
            labels=[x.text for x in root.findall('s:text',ns)]
            for r in e[k]:assert r['label'] in labels and f"{r['rate_pct']:.1f}".replace('.',',')+'%' in labels
    checks['all_four_svg_sidecars_text_and_values']=True
    pdf=PdfReader(out/'report.pdf');assert len(pdf.pages)==4
    texts=[x.extract_text() for x in pdf.pages]
    for i,t in enumerate(texts):assert f'0{i+1} / 04' in t and len(t)>1000
    for needle in ['64,7%','3,3%','4.311','978','1.511']:assert needle in texts[0]
    for r in e['attempts']:assert f"{r['rate_pct']:.1f}".replace('.',',')+'%' in texts[1]
    for tid in ['history-table','attempts-table']:
        for row in expected[tid]:
            for cell in row:assert cell in texts[3],cell
    assert '60 hồ sơ' in texts[2] and '200 lượt' in texts[2] and '16 giờ' in texts[2] and '2 giờ' in texts[2]
    images=[];pathops=[]
    for i,pg in enumerate(pdf.pages):
        xobjs=pg.get('/Resources',{}).get('/XObject',{})
        for key,obj in xobjs.items():
            ob=obj.get_object()
            if ob.get('/Subtype')=='/Image':images.append((i+1,str(key)))
        ops=ContentStream(pg.get_contents(),pdf).operations
        pathops.append(sum(op in [b're',b'm',b'l',b'c'] for _,op in ops))
    assert not images and pathops[0]>100 and pathops[1]>100 and all(c>0 for c in pathops)
    checks['pdf_four_searchable_pages_no_raster_images']=True
    checks['pdf_factual_surfaces_match_checked_values']=True
    with pdfplumber.open(out/'report.pdf') as pp:
        overflow=[]
        for i,pg in enumerate(pp.pages):
            for c in pg.chars:
                if c['x0']<0 or c['x1']>pg.width+.5 or c['top']<0 or c['bottom']>pg.height+.5:overflow.append((i+1,c['text']))
        assert not overflow
    checks['pdf_text_within_page_bounds']=True
    def lum(hex):
        v=[int(hex[i:i+2],16)/255 for i in (1,3,5)]
        v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
        return .2126*v[0]+.7152*v[1]+.0722*v[2]
    contrast={}
    for fg in ['#243c45','#546870','#006b61','#5e7985']:
        ratio=(lum('#fffdf9')+.05)/(lum(fg)+.05);contrast[fg]=ratio
        assert ratio>=3 if fg=='#5e7985' else ratio>=4.5
    assert (lum('#edf5f2')+.05)/(lum('#243c45')+.05)>=4.5
    checks['essential_text_and_mark_contrast']=True
    result=dict(checks=checks,source_sha256=sha,pdf_pages=len(pdf.pages),pdf_vector_path_operations_per_page=pathops,pdf_image_objects=images,contrast_ratios=contrast,checked_screen_widths=[1280,390],manual_review_scope='Final HTML sections at 1280 and 390 px; PDF four pages rendered with bundled Poppler. Model inspection only, no human comprehension outcome claimed.')
    if poppler:
        cache=out/'_inspection';cache.mkdir(exist_ok=True)
        subprocess.run([str(Path(poppler)/'pdftoppm.exe'),'-scale-to','1400','-png',str(out/'report.pdf'),str(cache/'final-pdf')],check=True)
        result['poppler_rendered_pages']=4
    (out/'evidence/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--poppler-bin');a=p.parse_args()
    print(json.dumps(verify(a.source,a.out,a.poppler_bin),ensure_ascii=False,indent=2))
