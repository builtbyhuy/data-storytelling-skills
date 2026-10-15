"""Offline Wine Quality reading report. Python 3.10+; standard library only.
Run from the package directory: python build.py
"""
from pathlib import Path
import csv, hashlib, json, math
from collections import Counter
from decimal import Decimal, InvalidOperation
from html import escape

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'input' / 'source'
EXPECTED = {
 'winequality-red.csv': '4a402cf041b025d4566d954c3b9ba8635a3a8a01e039005d97d6a710278cf05e',
 'winequality-white.csv': '76c3f809815c17c07212622f776311faeb31e87610d52c26d87d6e361b169836',
 'winequality.names': '15d215e73b39105952380fd487e4ce1bf5a6b83a425abb285c2ec55193d3ca92',
 'wine+quality.zip': '3ed56667f4b828242bd732d7d1dd7f2861e54432239d7fa63877014cbb0304d4',
 'LICENSE-CC-BY-4.0.txt': '9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411',
}
SCHEMA = ['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol','quality']
manifest = []
for name, expected in EXPECTED.items():
    raw = (SOURCE/name).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f'Source snapshot mismatch: {name}: {actual}')
    manifest.append({'file': name, 'bytes': len(raw), 'sha256': actual})
(ROOT/'source-manifest.json').write_text(json.dumps({'acquired_utc_date':'2026-10-15','files':manifest}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

data = {}
facts = []
def fact(metric, filename, group, value, denominator='', unit='rows', definition=''):
    facts.append(dict(metric=metric,source_file=filename,group=group,value=value,denominator=denominator,unit=unit,definition=definition))
for kind, group in [('red','Rượu đỏ'),('white','Rượu trắng')]:
    filename = f'winequality-{kind}.csv'
    with (SOURCE/filename).open(encoding='utf-8',newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        if reader.fieldnames != SCHEMA: raise ValueError('Unexpected schema')
        rows = list(reader)
    if any(set(r) != set(SCHEMA) or any(v is None for v in r.values()) for r in rows):
        raise ValueError('Malformed record; preserve source, investigate before reporting')
    scores=[]; missing=0; invalid=0
    for r in rows:
        q=r['quality'].strip()
        if not q:
            missing += 1; scores.append(None); continue
        try: d=Decimal(q)
        except InvalidOperation:
            invalid += 1; scores.append(None); continue
        if not d.is_finite() or d != d.to_integral_value() or not 0 <= d <= 10:
            invalid += 1; scores.append(None); continue
        scores.append(int(d))
    counts=Counter(s for s in scores if s is not None)
    n=len(rows); low=sum(counts[q] for q in range(6)); pct=100*low/n
    duplicates=Counter(tuple(r[c] for c in SCHEMA) for r in rows)
    extra=sum(v-1 for v in duplicates.values()); dup_groups=sum(v>1 for v in duplicates.values()); members=sum(v for v in duplicates.values() if v>1)
    d=dict(kind=kind,group=group,filename=filename,rows=rows,n=n,low=low,pct=pct,counts=counts,missing=missing,invalid=invalid,extra=extra,dup_groups=dup_groups,members=members,unique=len(duplicates))
    data[kind]=d
    for metric,value,denominator,unit,definition in [
      ('original_rows',n,'','rows','All data records; header excluded; duplicates retained'),
      ('quality_le_5',low,n,'rows','Valid integer quality in [0,5]'),
      ('quality_le_5_rate',low/n,n,'fraction','quality_le_5/original_rows; no silent denominator exclusion'),
      ('quality_missing',missing,n,'rows','Blank/whitespace quality'),
      ('quality_invalid',invalid,n,'rows','Non-numeric, non-integer, non-finite or outside [0,10]'),
      ('distinct_record_patterns',len(duplicates),n,'patterns','Equality of all 12 parsed field strings'),
      ('duplicate_extra_rows',extra,n,'rows','Sum(group size - 1) across identical 12-field patterns; not deleted'),
      ('duplicate_record_groups',dup_groups,'','groups','Identical 12-field patterns with count >1'),
      ('duplicate_group_members',members,n,'rows','All records in repeated patterns including first occurrence')]:
        fact(metric,filename,group,value,denominator,unit,definition)
    for score in range(11):
        fact(f'quality_{score}_count',filename,group,counts[score],n,'rows',f'quality = {score}; full ordinal domain 0-10')
        fact(f'quality_{score}_rate',filename,group,counts[score]/n,n,'fraction',f'quality = {score}/original_rows')
    assert sum(counts.values())+missing+invalid==n
    assert extra==n-len(duplicates)
red,white=data['red'],data['white']
delta=red['pct']-white['pct']
fact('red_minus_white_threshold_rate_pp','winequality-red.csv | winequality-white.csv','Đỏ trừ trắng',delta,'','percentage_points','100*(red_low/red_n - white_low/white_n)')
fact('review_records','','Đề xuất',40,'','records','20 first source data rows per file; convenience selection')
fact('review_person_minutes','','Giả định',120,'','person_minutes','40 records * 3 minutes/record')
fact('review_parallel_elapsed_minutes','','Giả định',60,'','minutes','120 person minutes / 2 only if both truly available in parallel')
with (ROOT/'facts.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['metric','source_file','group','value','denominator','unit','definition']);w.writeheader();w.writerows(facts)

with (ROOT/'review-40.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['source_file','source_data_row','reviewer','status']+SCHEMA
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for d in data.values():
        for i,r in enumerate(d['rows'][:20],1):
            w.writerow(dict(source_file=d['filename'],source_data_row=i,reviewer='',status='HOLD',**r))

record_fields=['source_file','source_data_row','source_field','original_value','original_state','snapshot_state','snapshot_evidence','provenance_state','provenance_evidence','scope_state','scope_evidence','availability_state','availability_evidence','permission_state','permission_evidence','assignee','status','reason','next_action','reviewer','review_when','start_decision']
blank={k:('unknown' if k.endswith('_state') and k!='original_state' else '') for k in record_fields}
blank['status']='HOLD'
with (ROOT/'work-record-template.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=record_fields);w.writeheader();w.writerow(blank)

def num(n): return f'{n:,}'.replace(',','.')
def pct(p, digits=2): return f'{p:.{digits}f}'.replace('.',',')+'%'
def hero_row(d):
    return f'''<div class="compare-row {d['kind']}"><div class="compare-label"><strong>{d['group']}</strong><span>{num(d['low'])} / {num(d['n'])} dòng</span></div><div class="compare-track"><span style="width:{d['pct']:.8f}%"></span></div><b>{pct(d['pct'])}</b></div>'''

# HTML/CSS bars and real editable text, never a raster chart.
distribution=[]
for q in range(11):
    r=red['counts'][q]; w=white['counts'][q]
    rp=100*r/red['n']; wp=100*w/white['n']
    divider='<div class="cut"><span>Ngưỡng giả định kết thúc tại điểm 5</span></div>' if q==6 else ''
    distribution.append(divider+f'''<div class="score-row"><span class="score">{q}</span><div class="score-pair"><div class="lane red"><div class="lane-track"><i style="width:{rp/50*100:.8f}%"></i></div><span>{num(r)} <small>({pct(rp,1)})</small></span></div><div class="lane white"><div class="lane-track"><i style="width:{wp/50*100:.8f}%"></i></div><span>{num(w)} <small>({pct(wp,1)})</small></span></div></div></div>''')

table_rows=[]
for q in range(11):
    table_rows.append(f'<tr><th scope="row">{q}</th><td>{num(red["counts"][q])}</td><td>{pct(100*red["counts"][q]/red["n"])}</td><td>{num(white["counts"][q])}</td><td>{pct(100*white["counts"][q]/white["n"])}</td></tr>')

source_rows=''.join(f'<li><a href="input/source/{escape(m["file"])}">{escape(m["file"])}</a><span>{num(m["bytes"])} byte</span><code>{m["sha256"]}</code></li>' for m in manifest)
summary_rows=''.join(f'<tr><th scope="row">{d["group"]}</th><td>{num(d["n"])}</td><td>{num(d["low"])}</td><td>{pct(d["pct"])}</td></tr>' for d in data.values())
duplicate_rows=''.join(f'<div class="dup-line"><strong>{d["group"]}</strong><p><b>{num(d["extra"])}</b> dòng lặp thêm trên {num(d["n"])} dòng gốc; {num(d["dup_groups"])} nhóm trùng chứa tổng cộng {num(d["members"])} dòng. Có {num(d["unique"])} mẫu bản ghi khác nhau.</p></div>' for d in data.values())
template=(ROOT/'report.template.html').read_text(encoding='utf-8')
replacements={'COMPARE_ROWS':hero_row(red)+hero_row(white),'DELTA':f'{delta:.2f}'.replace('.',','),'DISTRIBUTION':''.join(distribution),'TABLE_ROWS':''.join(table_rows),'SUMMARY_ROWS':summary_rows,'DUPLICATE_ROWS':duplicate_rows,'SOURCE_ROWS':source_rows,'RED_LOW':num(red['low']),'WHITE_LOW':num(white['low']),
'RED_RATE':pct(red['pct']),'WHITE_RATE':pct(white['pct']),'RED_N':num(red['n']),'WHITE_N':num(white['n']),
'RED_3_4':pct(100*(red['counts'][3]+red['counts'][4])/red['n']),'WHITE_3_4':pct(100*(white['counts'][3]+white['counts'][4])/white['n']),
'RED_3_4_N':num(red['counts'][3]+red['counts'][4]),'WHITE_3_4_N':num(white['counts'][3]+white['counts'][4])}
for key,value in replacements.items():template=template.replace('{{'+key+'}}',value)
if '{{' in template:raise ValueError('Unresolved template token')
(ROOT/'report.html').write_text(template,encoding='utf-8')
print(json.dumps({k:{x:v for x,v in d.items() if x not in ['rows','counts']} | {'distribution':dict(d['counts'])} for k,d in data.items()},ensure_ascii=False,indent=2))
print(f'Red minus white: {delta:.12f} percentage points')
print('Wrote report.html, facts.csv, review-40.csv, work-record-template.csv, source-manifest.json')
