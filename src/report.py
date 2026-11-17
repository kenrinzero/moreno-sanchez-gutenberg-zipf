"""Recompute all reported counts from complete A/B book records."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
from .reproduce import validate_book_result
import csv

ROOT=Path(__file__).resolve().parents[1]


def load_pass(directory,expected_pass):
    manifest=json.loads((directory/'manifest.json').read_bytes())
    expected_seed=2026111703 if expected_pass=='A' else 2026111704
    if manifest['pass']!=expected_pass or manifest['seed']!=expected_seed:
        raise ValueError('Wrong pass/seed supplied to report')
    completion=json.loads((directory/'completion.json').read_bytes())
    data=(directory/'books.jsonl').read_bytes()
    if not completion['complete'] or completion['pass']!=expected_pass or completion['books']!=31075 or hashlib.sha256(data).hexdigest()!=completion['books_jsonl_sha256']:
        raise ValueError('Incomplete or altered pass')
    rows=[json.loads(line) for line in data.splitlines()]
    if len(rows)!=31075 or len({r['pg_id'] for r in rows})!=31075:
        raise ValueError('Invalid book coverage')
    metadata_path=ROOT/'data/derived/books.csv'
    if hashlib.sha256(metadata_path.read_bytes()).hexdigest()!=manifest['books_csv_sha256']:
        raise ValueError('Report metadata differs from run input')
    with metadata_path.open(encoding='utf-8',newline='') as source:
        by_id={int(r['pg_id']):r for r in csv.DictReader(source)}
    if {r['pg_id'] for r in rows}!=set(by_id): raise ValueError('Report book set differs from validated input')
    for row in rows:
        validate_book_result(row,by_id[row['pg_id']],expected_seed)
    return {r['pg_id']:r for r in rows}


def category(row,threshold=5,strict=False,trial_key='K_ge'):
    a=row['f1'][trial_key]>threshold if strict else row['f1'][trial_key]>=threshold
    b=row['f2'][trial_key]>threshold if strict else row['f2'][trial_key]>=threshold
    return 'both' if a and b else 'f1_only' if a else 'f2_only' if b else 'neither'


def gate(observed,expected,tolerance):
    return {'observed':observed,'expected':expected,'difference':observed-expected,
            'tolerance':tolerance,'pass':abs(observed-expected)<=tolerance}


def sensitivity(rows,trial_key='K_ge',strict=False,p_field='p_lr'):
    groups={key:[r for r in rows if category(r,5,strict,trial_key)==key] for key in ('f1_only','f2_only','both','neither')}
    signed={key:[sum(r['lr'][p_field] is not None and r['lr'][p_field]<.05 and r['lr']['R']>0 for r in group),
                 sum(r['lr'][p_field] is not None and r['lr'][p_field]<.05 and r['lr']['R']<0 for r in group)] for key,group in groups.items()}
    return {'categories':{k:len(v) for k,v in groups.items()},'table2':signed,
            'total_first_three_rows':[sum(signed[k][i] for k in ('f1_only','f2_only','both')) for i in (0,1)]}


def strict_table_comparison(rows,targets):
    groups={name:[r for r in rows if category(r,strict=True)==name] for name in ('f1_only','f2_only','both','neither')}
    t1={name:[sum(r['lr']['R']>0 for r in group),sum(r['lr']['R']<0 for r in group),len(group)] for name,group in groups.items() if name!='neither'}
    t1['total_lr']=[sum(t1[name][i] for name in ('f1_only','f2_only','both')) for i in range(3)]
    sr=sensitivity(rows,strict=True)
    t2={**sr['table2'],'total_first_three_rows':sr['total_first_three_rows']}
    comparisons=[]
    for name,values in t1.items():
        for i,(x,y) in enumerate(zip(values,targets['table1']['rows'][name])):
            comparisons.append(gate(x,y,.03*y if i==2 or name=='total_lr' else max(.05*y,50)))
    for name,values in t2.items():
        for x,y in zip(values,targets['table2']['rows'][name]):comparisons.append(gate(x,y,5 if y==0 else max(.05*y,50)))
    counts={'f1':len(groups['f1_only'])+len(groups['both']),'f2':len(groups['f2_only'])+len(groups['both'])}
    for model,expected in (('f1',4524),('f2',12315)):comparisons.append(gate(counts[model],expected,.03*expected))
    ratio=counts['f2']/counts['f1'] if counts['f1'] else None
    comparisons.append(gate(ratio,12315/4524,.1) if ratio is not None else {'pass':False})
    return {'criterion':'K_ge>=6 (strict p>0.05); sensitivity only, does not replace primary inclusive rule',
            'table1':t1,'table2':t2,'acceptance':counts,'ratio':ratio,
            'all_comparison_bands_pass':all(g['pass'] for g in comparisons)}


def build_report(a,b):
    if set(a)!=set(b): raise ValueError('Pass book sets differ')
    for pg in a:
        for key in ('N','L','source_sha256','lr'):
            if a[pg][key]!=b[pg][key]: raise ValueError(f'Passes disagree on deterministic {key}')
        for model in ('f1','f2'):
            for key in ('beta','D'):
                if a[pg][model][key]!=b[pg][model][key]: raise ValueError('Deterministic fits differ')
    targets=json.loads((ROOT/'paper/targets.json').read_bytes())
    rows=list(a.values())
    by_category={name:[r for r in rows if category(r)==name] for name in ('f1_only','f2_only','both','neither')}
    table1={}
    for name in ('f1_only','f2_only','both'):
        group=by_category[name]
        observed=[sum(r['lr']['R']>0 for r in group),sum(r['lr']['R']<0 for r in group),len(group)]
        expected=targets['table1']['rows'][name]
        table1[name]=[gate(x,y,.03*y if i==2 else max(.05*y,50)) for i,(x,y) in enumerate(zip(observed,expected))]
    totals=[sum(table1[name][i]['observed'] for name in table1) for i in range(3)]
    table1['total_lr']=[gate(x,y,.03*y) for x,y in zip(totals,targets['table1']['rows']['total_lr'])]
    table2={}
    contradictions=[]
    for name in ('f1_only','f2_only','both','neither'):
        group=by_category[name]
        significant=[r for r in group if r['lr']['p_lr'] is not None and r['lr']['p_lr']<.05]
        observed=[sum(r['lr']['R']>0 for r in significant),sum(r['lr']['R']<0 for r in significant)]
        expected=targets['table2']['rows'][name]
        table2[name]=[gate(x,y,5 if y==0 else max(.05*y,50)) for x,y in zip(observed,expected)]
        for r in significant:
            if (name=='f1_only' and r['lr']['R']<0) or (name=='f2_only' and r['lr']['R']>0):
                contradictions.append({'pg_id':r['pg_id'],'category':name,'R':r['lr']['R'],'p_lr':r['lr']['p_lr'],
                                       'K_f1':r['f1']['K_ge'],'K_f2':r['f2']['K_ge']})
    totals=[sum(table2[name][i]['observed'] for name in ('f1_only','f2_only','both')) for i in range(2)]
    table2['total_first_three_rows']=[gate(x,y,max(.05*y,50)) for x,y in zip(totals,targets['table2']['rows']['total_first_three_rows'])]
    acceptance={}
    stability={}
    moments={}
    quartiles={}
    for model,expected in (('f1',4524),('f2',12315)):
        av=np.array([a[pg][model]['K_ge']>=5 for pg in sorted(a)])
        bv=np.array([b[pg][model]['K_ge']>=5 for pg in sorted(a)])
        acceptance[model]=gate(int(av.sum()),expected,.03*expected)
        observed_agreement=float((av==bv).mean())
        chance=float(av.mean()*bv.mean()+(1-av.mean())*(1-bv.mean()))
        stability[model]={'both_accept':int((av&bv).sum()),'A_only':int((av&~bv).sum()),'B_only':int((~av&bv).sum()),
                          'both_reject':int((~av&~bv).sum()),'switches':int((av!=bv).sum()),
                          'agreement':observed_agreement,'kappa':(observed_agreement-chance)/(1-chance) if chance<1 else None,
                          'A_accepted':int(av.sum()),'B_accepted':int(bv.sum()),
                          'relative_accepted_count_change':float(bv.sum()/av.sum()-1) if av.sum() else None}
        estimates=np.array([r[model]['beta'] for r in rows if r[model]['K_ge']>=5])
        moments[model]={'n_accepted':len(estimates),'mean':float(estimates.mean()) if len(estimates) else None,
                        'sd_population':float(estimates.std(ddof=0)) if len(estimates) else None,
                        'sd_sample':float(estimates.std(ddof=1)) if len(estimates)>1 else None, 'printed':targets['figure8'][model]}
        accepted=sorted([r for r in rows if r[model]['K_ge']>=5],key=lambda r:(r['L'],r['pg_id']))
        quartiles[model]=[]
        for indices in np.array_split(np.arange(len(accepted)),4):
            group=[accepted[int(i)] for i in indices]
            quartiles[model].append({'books':len(group),'min_L':group[0]['L'] if group else None,'max_L':group[-1]['L'] if group else None})
    ratio=acceptance['f2']['observed']/acceptance['f1']['observed'] if acceptance['f1']['observed'] else None
    ratio_gate=gate(ratio,12315/4524,.1) if ratio is not None else {'observed':None,'expected':12315/4524,'difference':None,'tolerance':.1,'pass':False,'reason':'No f1 accepts'}
    curve=[]
    for threshold in range(1,51):
        counts=Counter(category(r,threshold) for r in rows)
        curve.append({'p0':threshold/100,'f1':(counts['f1_only']+counts['both'])/len(rows),
                      'f2':(counts['f2_only']+counts['both'])/len(rows),'both':counts['both']/len(rows)})
    ordered=sorted(rows,key=lambda r:(r['L'],r['pg_id']))
    bins=[]
    for start in range(0,len(ordered),1000):
        group=ordered[start:start+1000]
        bins.append({'n_books':len(group),'min_L':group[0]['L'],'max_L':group[-1]['L'],
                     'geometric_mean_L':float(np.exp(np.log([r['L'] for r in group]).mean())),
                     'partial':len(group)<1000,
                     'counts':{str(k):{m:sum(r[m]['K_ge']>=k for r in group) for m in ('f1','f2')} for k in range(1,51)}})
    strict=Counter(category(r,5,True) for r in rows)
    pooled={m:sum(a[pg][m]['K_ge']+b[pg][m]['K_ge']>=10 for pg in a) for m in ('f1','f2')}
    gates=[g['pass'] for table in (table1,table2) for values in table.values() for g in values]
    gates += [g['pass'] for g in acceptance.values()]+[ratio_gate['pass']]
    return {'books':len(rows),'primary_pass':'A','table1':table1,'table2':table2,'acceptance':acceptance,
            'acceptance_ratio':ratio_gate,'all_declared_table_bands_pass':all(gates),
            'exposed_prediction_checks':{'status':'Historical pilot predictions, not calibration or reproduction gates',
                'f2_switches_500_to_2000':{'observed':stability['f2']['switches'],'within_prediction':500<=stability['f2']['switches']<=2000},
                'net_relative_change_within_4pct':{m:{'observed':s['relative_accepted_count_change'],
                    'within_prediction':abs(s['relative_accepted_count_change'])<=.04 if s['relative_accepted_count_change'] is not None else None}
                    for m,s in stability.items() if m=='f2'}},
            'contradictory_books':contradictions,'lr_degenerate_books':[r['pg_id'] for r in rows if r['lr']['degenerate']],
            'numerical_diagnostics':{label:{m:{key:sum(r[m].get(key,0) for r in books.values())
                for key in ('ties','raw_float_ties','ks_refinements','inverse_refinements','large_integers')}
                for m in ('f1','f2')} for label,books in (('A',a),('B',b))},
            'zero_lr_books':[r['pg_id'] for r in rows if r['lr']['R']==0],
            'strict_p_sensitivity':dict(strict),'beta_moments':moments,'stability':stability,
            'strict_cutoff_table_comparison':strict_table_comparison(rows,targets),
            'statistic_tie_sensitivity':sensitivity(rows,trial_key='K_gt'),
            'sample_variance_lr_sensitivity':sensitivity(rows,p_field='p_lr_sample'),
            'plus_one_p_sensitivity':{'centile_grid_classifications_identical':all(((r[m]['K_ge']+1)*100>=101*k)==(r[m]['K_ge']>=k) for r in rows for m in ('f1','f2') for k in range(1,51)),
                                      'note':'(K+1)/101 changes reported p levels but not decisions at p0=.01,...,.50; off-grid thresholds can differ.'},
            'figure9_reconstructed_quartiles':quartiles,
            'figure9_grouping':'Accepted books sorted by(L,PG_id); four near-equal count groups, extra books assigned first; descriptive reconstruction.',
            'pooled_B200_diagnostic':{'accepted_counts':pooled,'criterion':'K_A+K_B>=10 out of200; does not replace passA or its gates'},
            'survival_curve':curve,'length_bins':bins,
            'high_precision_status':'Separate precision audit required; all ordinary B=100/200 results retain Monte Carlo uncertainty',
            'scope':'f1/f2 on released frequency vectors under iid-type null; f3 and genre/holdout deferred'}


def source_path(path):
    resolved=path.resolve()
    return (resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else resolved).as_posix()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--A',type=Path,required=True)
    parser.add_argument('--B',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--precision',type=Path)
    args=parser.parse_args()
    am=json.loads((args.A/'manifest.json').read_bytes()); bm=json.loads((args.B/'manifest.json').read_bytes())
    for field in ('contract_sha256','environment','calibration_artifact_sha256','books_csv_sha256','archive_sha256','ingest_json_sha256'):
        if am[field]!=bm[field]: raise ValueError(f'Pass provenance differs: {field}')
    for name in ('models.py','reference.py','bootstrap.py','reproduce.py'):
        if am['code_sha256'][name]!=bm['code_sha256'][name]: raise ValueError('Pass implementations differ')
    report=build_report(load_pass(args.A,'A'),load_pass(args.B,'B'))
    report['report_code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['source_targets_sha256']=hashlib.sha256((ROOT/'paper/targets.json').read_bytes()).hexdigest()
    report['source_passes']={name:{'path':source_path(path),'manifest_sha256':hashlib.sha256((path/'manifest.json').read_bytes()).hexdigest(),
                                  'books_sha256':hashlib.sha256((path/'books.jsonl').read_bytes()).hexdigest()} for name,path in (('A',args.A),('B',args.B))}
    if args.precision:
        from .build_reader import load_precision,precision_comparisons
        summary,pairs=load_precision(args.precision,args.A,report)
        report['precision_summary']=summary
        report['precision_reclassifications']=precision_comparisons(pairs)
        report['precision_manifest_sha256']=hashlib.sha256((args.precision/'manifest.json').read_bytes()).hexdigest()
        report['high_precision_status']=f"Completed stratified audit of {len(pairs)} selected pairs; remaining {62150-len(pairs)} pairs not precision audited. Intervals are pointwise conditional Monte Carlo intervals."
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes((json.dumps(report,indent=2,allow_nan=False)+'\n').encode('utf-8'))
    print(json.dumps({k:report[k] for k in ('books','acceptance','acceptance_ratio','all_declared_table_bands_pass','stability')},indent=2))


if __name__=='__main__': main()
