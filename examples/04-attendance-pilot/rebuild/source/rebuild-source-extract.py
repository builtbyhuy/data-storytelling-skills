"""Neutral reproducible source extraction; no analysis, ranking or recommendation."""
import argparse,csv,hashlib,io,json
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent

def run(config_path,source_path,output_dir):
    config=json.loads(config_path.read_text(encoding='utf-8'))
    source=source_path or config_path.parent/config['source']
    payload=source.read_bytes()
    reader=csv.DictReader(io.StringIO(payload.decode('utf-8-sig')))
    fields=reader.fieldnames
    source_rows=list(enumerate(reader,2))
    selected=[(index,row) for index,row in source_rows if row['time_period'] in config['periods'] and row['time_identifier']==config['time_identifier'] and row['country_name']==config['country_name'] and row['education_phase'] in config['education_phases']]
    candidates=[(index,row) for index,row in selected if row['geographic_level']==config['candidate_geographic_level']]
    contexts=[row for index,row in selected if row['geographic_level'] in config['context_geographic_levels']]
    lookup={}
    for index,row in candidates:
        key=(row['time_period'],*(row[field] for field in config['key_fields']))
        if key in lookup:raise ValueError(f'Duplicate source key: {key}')
        lookup[key]=(index,row)
    union=sorted({tuple(row[field] for field in config['key_fields']) for index,row in candidates})
    authority_names={row['new_la_code']:row['la_name'] for index,row in candidates}
    absent_phase_pairs=[{'new_la_code':code,'la_name':authority_names[code],'education_phase':phase,'periods_without_source_row':list(config['periods'])} for code in sorted(authority_names) for phase in config['education_phases'] if all((period,code,phase) not in lookup for period in config['periods'])]
    records=[];references=[];missing=[];unmatched=[];identity_changes=[]
    numeric_fields=[field for field in fields if field.startswith(('sess_','enrolments')) or field=='num_schools']
    for key in union:
        record=dict(zip(config['key_fields'],key))
        reference={**record,'source_csv_rows':{}}
        year_rows=[]
        for period in config['periods']:
            observation=lookup.get((period,*key))
            record['source_row_present__'+period]='1' if observation else '0'
            if observation:
                index,row=observation
                reference['source_csv_rows'][period]=index;year_rows.append(row)
            else:
                row={};unmatched.append({'period':period,**dict(zip(config['key_fields'],key))})
            for field in fields:
                if field in config['key_fields']:continue
                record[field+'__'+period]=row.get(field,'')
                if observation and field in numeric_fields and row[field] in ('x','z','',':','..'):
                    missing.append({'period':period,**dict(zip(config['key_fields'],key)),'field':field,'source_marker':row[field],'source_csv_row':index})
        if len(year_rows)==len(config['periods']):
            for field in ('new_la_code','old_la_code','la_name','region_code','region_name','education_phase'):
                values=[row[field] for row in year_rows]
                if len(set(values))>1:identity_changes.append({**dict(zip(config['key_fields'],key)),'field':field,'values_by_period':dict(zip(config['periods'],values))})
        records.append(record);references.append(reference)
    output_dir.mkdir(parents=True,exist_ok=True)
    with (output_dir/config['output']).open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    with (output_dir/'published-context.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(contexts)
    manifest={'source_file':source.name,'source_sha256':hashlib.sha256(payload).hexdigest(),'source_record_count':len(source_rows),'source_fields':fields,'numeric_fields':numeric_fields,'periods':config['periods'],'education_phases':config['education_phases'],'distinct_local_authority_codes':len(authority_names),'candidate_source_rows':len(candidates),'wide_cohort_rows':len(records),'context_rows':len(contexts),'candidate_counts_by_period_phase':{period:{phase:sum(row['time_period']==period and row['education_phase']==phase for index,row in candidates) for phase in config['education_phases']} for period in config['periods']},'authority_phase_pairs_absent_in_all_selected_periods':absent_phase_pairs,'missing_markers':missing,'missing_marker_counts':dict(Counter(item['source_marker'] for item in missing)),'unmatched_period_keys':unmatched,'identity_changes':identity_changes,'source_row_references':references,'extraction':'Source field strings copied unchanged to a union-of-observed-keys two-period pivot. Structurally absent phase pairs are documented, not added as zero rows. Key and column labels reorganized; raw CSV bytes unchanged. source_row_present is a provenance flag, not an absence measure.'}
    (output_dir/'source-extract-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_records':len(source_rows),'candidate_source_rows':len(candidates),'input_wide_rows':len(records),'context_rows':len(contexts),'missing_marker_counts':manifest['missing_marker_counts'],'unmatched_period_keys':len(unmatched),'identity_changes':len(identity_changes),'source_sha256':manifest['source_sha256']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',type=Path,default=BASE/'cohort-config.json');parser.add_argument('--source',type=Path);parser.add_argument('--output-dir',type=Path,default=BASE)
    args=parser.parse_args();run(args.config.resolve(),args.source.resolve() if args.source else None,args.output_dir.resolve())
