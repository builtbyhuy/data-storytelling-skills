import argparse, csv, json, hashlib
from pathlib import Path
from collections import Counter
from decimal import Decimal

p=argparse.ArgumentParser()
p.add_argument('--source-dir',type=Path,default=Path(__file__).parent/'source')
p.add_argument('--build-dir',type=Path,default=Path(__file__).parent/'scratch/build')
a=p.parse_args(); a.build_dir.mkdir(parents=True,exist_ok=True)
config=json.loads((a.source_dir/'cohort-config.json').read_text(encoding='utf-8'))
periods=config['periods']; phases=config['education_phases']
raw=list(csv.DictReader((a.source_dir/'raw/absence-geographic-autumn.csv').open(encoding='utf-8-sig')))
rows=[r for r in raw if r['time_period'] in periods and r['time_identifier']=='Autumn term' and r['country_name']=='England' and r['education_phase'] in phases and r['geographic_level']=='Local authority']
fields=['enrolments','sess_possible','sess_overall','sess_authorised','sess_unauthorised','enrolments_pa_10_exact','enrolments_pa_50_exact','sess_auth_illness','sess_unauth_other','sess_unauth_holiday','num_schools']
keys=[(r['time_period'],r['new_la_code'],r['education_phase']) for r in rows]
assert len(keys)==len(set(keys))
lookup={(r['time_period'],r['new_la_code'],r['education_phase']):r for r in rows}
checks={'raw_sha256':hashlib.sha256((a.source_dir/'raw/absence-geographic-autumn.csv').read_bytes()).hexdigest(),'source_rows':len(raw),'selected_rows':len(rows),'distinct_authorities':len(set(r['new_la_code'] for r in rows)),'phase_period_counts':dict(Counter(f"{r['time_period']} {r['education_phase']}" for r in rows)),'numeric_missing':{},'national_reconciliation':[]}
for f in fields:
    bad=[r for r in rows if r[f] in ('','x','z',':','..')]
    checks['numeric_missing'][f]=len(bad)
    assert not bad,(f,len(bad))
for r in rows:
    assert int(r['sess_overall'])==int(r['sess_authorised'])+int(r['sess_unauthorised'])
    assert int(r['enrolments_pa_50_exact'])<=int(r['enrolments_pa_10_exact'])<=int(r['enrolments'])

def obs(r):
    d={f:int(r[f]) for f in fields}
    for target,num,den in [('overall','sess_overall','sess_possible'),('pa','enrolments_pa_10_exact','enrolments'),('severe','enrolments_pa_50_exact','enrolments'),('unauthorised','sess_unauthorised','sess_possible'),('illness','sess_auth_illness','sess_possible'),('other_unauthorised','sess_unauth_other','sess_possible'),('holiday_unauthorised','sess_unauth_holiday','sess_possible')]:
        d[target]=d[num]/d[den]
    d['pa_less_severe']=d['enrolments_pa_10_exact']-d['enrolments_pa_50_exact']
    return d

local=[]
for code,phase in sorted({(r['new_la_code'],r['education_phase']) for r in rows}):
    rr=[lookup[(t,code,phase)] for t in periods]
    d={'code':code,'phase':phase,'name':rr[1]['la_name'],'region':rr[1]['region_name'],'old':obs(rr[0]),'new':obs(rr[1])}
    d['delta']={f:d['new'][f]-d['old'][f] for f in ['overall','pa','severe','unauthorised','illness']}
    local.append(d)

national=[]
for phase in phases:
    for period in periods:
        chosen=[r for r in rows if r['education_phase']==phase and r['time_period']==period]
        n={f:sum(int(r[f]) for r in chosen) for f in fields}
        official=next(r for r in raw if r['geographic_level']=='National' and r['time_period']==period and r['time_identifier']=='Autumn term' and r['education_phase']==phase and r['country_name']=='England')
        for f in fields:
            assert n[f]==int(official[f]),(period,phase,f,n[f],official[f])
        checks['national_reconciliation'].append({'period':period,'phase':phase,'fields_exactly_matched':fields})
        national.append({'period':period,'phase':phase,**obs({f:str(n[f]) for f in fields})})

summary={}
for phase in phases:
    pool=[r for r in local if r['phase']==phase]
    n=next(r for r in national if r['phase']==phase and r['period']==periods[1])
    summary[phase]={'n':len(pool),'pa_rise':sum(r['delta']['pa']>0 for r in pool),'severe_rise':sum(r['delta']['severe']>0 for r in pool),'pa_min':min(r['new']['pa'] for r in pool),'pa_max':max(r['new']['pa'] for r in pool),'above_national_pa_and_rising':sum(r['new']['pa']>n['pa'] and r['delta']['pa']>0 for r in pool)}

result={'periods':periods,'national':national,'local':local,'summary':summary,'checks':checks}
(a.build_dir/'facts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'national':national,'summary':summary},ensure_ascii=False,indent=2))
sec=[r for r in local if r['phase']==phases[1]]
for label,fn in [('PA rate',lambda r:r['new']['pa']),('PA increase',lambda r:r['delta']['pa']),('severe rate',lambda r:r['new']['severe']),('severe decrease',lambda r:-r['delta']['severe'])]:
    print(label)
    for r in sorted(sec,key=fn,reverse=True)[:10]:
        print(r['name'], 'PA',round(r['new']['pa']*100,2),'dPA',round(r['delta']['pa']*100,2),'SV',round(r['new']['severe']*100,2),'dSV',round(r['delta']['severe']*100,2),'PAcount',r['new']['enrolments_pa_10_exact'],'moderate',r['new']['pa_less_severe'],'enrol',r['new']['enrolments'])
