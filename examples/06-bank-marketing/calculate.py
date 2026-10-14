"""Reproducible descriptive calculations. Read-only source; no row recoding."""
from pathlib import Path
import argparse, csv, hashlib, json, collections
import pandas as pd

def calculate(source, out):
    source, out = Path(source), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    contract = json.loads((source.parent/'source-contract.json').read_text(encoding='utf-8'))
    assert sha == contract['selected_file']['sha256']
    df = pd.read_csv(source, sep=';')
    assert len(df)==45211 and list(df.columns)==contract['selected_file']['header_order']
    assert not df.isna().any().any()
    yes = df.y.eq('yes')
    def group(mask, key, label):
        n, y = int(mask.sum()), int((mask & yes).sum())
        return dict(key=key, label=label, records=n, yes=y, no=n-y, rate_pct=100*y/n if n else None)
    history = [group(df.poutcome.eq(k), k, l) for k,l in [('success','Thành công trước'),('failure','Thất bại trước'),('other','Kết quả khác'),('unknown','Không rõ kết quả')]]
    bins=[('1','1 lần',df.campaign.eq(1)),('2-3','2–3 lần',df.campaign.between(2,3)),('4-6','4–6 lần',df.campaign.between(4,6)),('7+','Từ 7 lần',df.campaign.ge(7))]
    attempts=[group(m,k,l) for k,l,m in bins]
    strata=[]
    for k,l,m in bins:
        for h in ['success','not_success']:
            hm=df.poutcome.eq('success') if h=='success' else ~df.poutcome.eq('success')
            r=group(m & hm, f'{k}:{h}', l);r['campaign_group']=k;r['history_group']=h;strata.append(r)
    contact=[]
    for k in ['cellular','telephone','unknown']:
        for h in ['success','not_success']:
            hm=df.poutcome.eq('success') if h=='success' else ~df.poutcome.eq('success')
            r=group(df.contact.eq(k)&hm, f'{k}:{h}',k);r['contact']=k;r['history_group']=h;contact.append(r)
    # Independent pass through Python's csv reader, with integer counts only.
    hist=collections.defaultdict(lambda:[0,0]); camps=collections.defaultdict(lambda:[0,0]); total=[0,0]; blank=0
    with source.open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f,delimiter=';'):
            y=int(r['y']=='yes');total[0]+=1;total[1]+=y
            hist[r['poutcome']][0]+=1;hist[r['poutcome']][1]+=y
            c=int(r['campaign']); k='1' if c==1 else '2-3' if c<=3 else '4-6' if c<=6 else '7+'
            camps[k][0]+=1;camps[k][1]+=y
            blank+=sum(v=='' for v in r.values())
    assert total==[len(df),int(yes.sum())] and blank==0
    for r in history: assert hist[r['key']]==[r['records'],r['yes']]
    for r in attempts: assert camps[r['key']]==[r['records'],r['yes']]
    assert sum(r['records'] for r in history)==len(df)==sum(r['records'] for r in attempts)
    assert sum(r['yes'] for r in history)==int(yes.sum())==sum(r['yes'] for r in attempts)
    success=history[0]
    pdays_stats={'not_previously_contacted':int(df.pdays.eq(-1).sum()),'previous_zero':int(df.previous.eq(0).sum()),'pdays_sentinel_previous_positive':int((df.pdays.eq(-1)&df.previous.gt(0)).sum()),'pdays_non_sentinel_previous_zero':int((df.pdays.ne(-1)&df.previous.eq(0)).sum())}
    result=dict(source_sha256=sha,rows=len(df),columns=len(df.columns),yes=int(yes.sum()),no=int((~yes).sum()),rate_pct=float(100*yes.mean()),history=history,attempts=attempts,strata=strata,contact_strata=contact,success_share_records_pct=100*success['records']/len(df),success_share_yes_pct=100*success['yes']/int(yes.sum()),rest_yes=int(yes.sum())-success['yes'],rest_records=len(df)-success['records'],rest_rate_pct=100*(int(yes.sum())-success['yes'])/(len(df)-success['records']),unknown_counts={c:int(df[c].eq('unknown').sum()) for c in ['job','education','contact','poutcome']},pdays=pdays_stats,duplicates_exact=int(df.duplicated().sum()),campaign_min=int(df.campaign.min()),campaign_max=int(df.campaign.max()),zero_duration=int(df.duration.eq(0).sum()),checks={'raw_hash_contract':True,'header_and_shape':True,'blank_cells':blank,'all_y_domain':set(df.y)=={'yes','no'},'independent_csv_counts':True,'history_and_attempt_reconciliation':True})
    (out/'calculations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for name, rows in [('history',history),('attempts',attempts),('history-by-attempts',strata),('history-by-contact',contact)]:
        pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False,encoding='utf-8-sig')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(calculate(a.source,a.out),ensure_ascii=False,indent=2))

