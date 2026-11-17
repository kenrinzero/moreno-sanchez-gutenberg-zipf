"""Build the standalone reader from complete, hash-checked run artifacts."""
import argparse
import hashlib
import html
import json
from pathlib import Path
from . import precision,reproduce
from .report import load_pass,build_report
import csv

ROOT=Path(__file__).resolve().parents[1]
LABELS={'f1_only':'f1 only','f2_only':'f2 only','both':'Both','neither':'Neither',
        'total_lr':'Total: at least one accepted','total_first_three_rows':'Total of first three rows'}


def table(headers,rows):
    return '<div class="tablewrap"><table><thead><tr>'+''.join('<th scope="col">'+html.escape(str(c))+'</th>' for c in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value,spec=','):
    return 'unavailable' if value is None else format(value,spec)


def precision_comparisons(rows):
    return {f'f{m}':{'A_accepted_now_rejected':sum(r['model']==m and r['selecting_K']>=5 and r['precision_status']=='rejected' for r in rows),
                     'A_rejected_now_non_rejected':sum(r['model']==m and r['selecting_K']<5 and r['precision_status']=='non_rejected' for r in rows)} for m in (1,2)}


def load_precision(directory,a_path,report):
    summary=json.loads((directory/'summary.json').read_bytes())
    manifest=json.loads((directory/'manifest.json').read_bytes())
    payload=(directory/'pairs.jsonl').read_bytes()
    if summary['complete'] is not True or sha(directory/'pairs.jsonl')!=summary['pairs_sha256']:
        raise ValueError('Precision output incomplete or changed')
    books=load_pass(a_path,'A')
    am=json.loads((a_path/'manifest.json').read_bytes())
    if manifest['seed']!=2026111705 or manifest['B']!=10000 or manifest['ci_confidence']!=.95 or manifest['interval_scope']!='pointwise; selection trials excluded':
        raise ValueError('Precision design changed')
    for name in ('models.py','reference.py','bootstrap.py'):
        if manifest['code_sha256'][name]!=am['code_sha256'][name] or manifest['code_sha256'][name]!=sha(ROOT/'src'/name):
            raise ValueError('Precision numerical implementation changed')
    if manifest['code_sha256']['precision.py']!=sha(ROOT/'src/precision.py'):
        raise ValueError('Precision runner changed')
    for key in ('environment','contract_sha256','calibration_artifact_sha256','archive_sha256','books_csv_sha256','ingest_json_sha256'):
        if manifest[key]!=am[key]: raise ValueError('Precision provenance differs from pass A')
    if manifest['selecting_pass_sha256']!=report['source_passes']['A']['books_sha256'] or manifest['selecting_pass_sha256']!=sha(a_path/'books.jsonl'):
        raise ValueError('Precision selected another pass')
    if manifest['selecting_manifest_sha256']!=sha(a_path/'manifest.json') or manifest['selecting_completion_sha256']!=sha(a_path/'completion.json'):
        raise ValueError('Selecting pass metadata changed')
    selected=precision.select_pairs(books)
    if selected!=manifest['selection']: raise ValueError('Precision selection changed')
    expected={(r['model'],r['pg_id']):r for r in selected}
    rows=[json.loads(line) for line in payload.splitlines()]
    if len(rows)!=len(expected) or {(r['model'],r['pg_id']) for r in rows}!=set(expected):
        raise ValueError('Precision selection coverage incomplete')
    with (ROOT/'data/derived/books.csv').open(encoding='utf-8',newline='') as source:
        metadata={int(r['pg_id']):r for r in csv.DictReader(source)}
    for row in rows: precision.validate_pair(row,expected[(row['model'],row['pg_id'])],metadata[row['pg_id']])
    counts={f'f{m}':{s:sum(r['model']==m and r['precision_status']==s for r in rows) for s in ('rejected','non_rejected','unresolved')} for m in (1,2)}
    if counts!=summary['models'] or summary['selected_pairs']!=len(rows) or summary['not_precision_audited_pairs']!=62150-len(rows):
        raise ValueError('Precision summary differs from records')
    expected_strata=[{'model':m,'stratum':[lo,hi],'candidates':sum(lo<=r[f'f{m}']['K_ge']<=hi for r in books.values()),
                     'selected':sum(r['model']==m and r['stratum']==[lo,hi] for r in rows)} for m in (1,2) for lo,hi in precision.STRATA]
    if expected_strata!=summary['strata']: raise ValueError('Stratum summary differs from records')
    if 'precision_summary' in report and report['precision_summary']!=summary:
        raise ValueError('Report includes another precision summary')
    if 'precision_manifest_sha256' in report and report['precision_manifest_sha256']!=sha(directory/'manifest.json'):
        raise ValueError('Report includes another precision manifest')
    if 'precision_reclassifications' in report and report['precision_reclassifications']!=precision_comparisons(rows):
        raise ValueError('Report precision reclassifications differ from records')
    return summary,rows


def render(report,ps,pairs,calibration,report_hash):
    a=report['acceptance'];ratio=report['acceptance_ratio']['observed']
    replacements={}
    replacements['HEADLINE']=f"The power-law survival model is accepted for {ratio:.2f} times as many books as the power-law mass model at the paper's 0.05 cutoff." if ratio is not None else "The acceptance ratio is unavailable because no book accepts f1 at the paper's 0.05 cutoff."
    replacements['VERDICT']='All predeclared table-comparison bands pass; individual counts are not exact matches.' if report['all_declared_table_bands_pass'] else '<strong>Partial numerical reproduction.</strong> Some predeclared table-comparison bands fail; the exact mismatches are retained below.'
    replacements['CARDS']=''.join(f'<div class="card"><span>{label}</span><strong>{value}</strong><span>{desc}</span></div>' for label,value,desc in (
        ('f1 accepted',f"{a['f1']['observed']:,}",f"{100*a['f1']['observed']/report['books']:.1f}% of books"),
        ('f2 accepted',f"{a['f2']['observed']:,}",f"{100*a['f2']['observed']/report['books']:.1f}% of books"),
        ('f2 / f1 accepted',number(ratio,'.2f')+('×' if ratio is not None else ''),'published table: 2.72×')))
    gate_rows=[]
    for key,headers in (('table1',['KS group','R &gt; 0','R &lt; 0','Total']),('table2',['KS group','Significant f1','Significant f2'])):
        # table() escapes headings, so plain text keeps comparison signs accessible.
        headers=[h.replace('&gt;','>').replace('&lt;','<') for h in headers]
        order=('f1_only','f2_only','both','total_lr') if key=='table1' else ('f1_only','f2_only','both','total_first_three_rows','neither')
        rows=[]
        for name in order:
            cells=report[key][name]
            rows.append([LABELS[name]]+[f'<span class="{"pass" if g["pass"] else "fail"}">{g["observed"]:,} / {g["expected"]:,}{"" if g["pass"] else " · outside band"}</span>' for g in cells])
            for i,g in enumerate(cells):
                gate_rows.append([f'{key.title()} · {LABELS[name]} · {headers[i+1]}',f'{g["difference"]:+,}',f'±{g["tolerance"]:g}', 'Pass' if g['pass'] else '<strong class="fail">Fail</strong>'])
        replacements[key.upper()]=table(headers,rows)
    for model,g in a.items(): gate_rows.append([f'{model} accepted total',f'{g["difference"]:+,}',f'±{g["tolerance"]:g}','Pass' if g['pass'] else '<strong class="fail">Fail</strong>'])
    g=report['acceptance_ratio'];gate_rows.append(['f2/f1 ratio',number(g['difference'],'+.6f'),f'±{g["tolerance"]:g}','Pass' if g['pass'] else '<strong class="fail">Fail</strong>'])
    replacements['GATES']=table(['Comparison','Run minus paper','Allowed difference','Outcome'],gate_rows)
    contradictions=report['contradictory_books']
    replacements['MISMATCH_NOTE']=f"The separate pass B accepts {report['stability']['f1']['B_accepted']:,} books under f1 and {report['stability']['f2']['B_accepted']:,} under f2. The authors' per-book seeds and full implementation are unavailable here, so the residual table differences cannot be assigned a unique cause. Changing the cutoff is a sensitivity check, not evidence that the authors used another rule; the primary inclusive rule remains fixed."
    strict_check=report['strict_cutoff_table_comparison']
    replacements['MISMATCH_NOTE']+=f" In the predeclared strict-cutoff sensitivity, f1 accepts {strict_check['acceptance']['f1']:,} books and f2 {strict_check['acceptance']['f2']:,}; {'all' if strict_check['all_comparison_bands_pass'] else 'not all'} comparison bands pass. This convention sensitivity does not change the primary verdict."
    replacements['CONTRADICTIONS']=f'{len(contradictions)} books contradict the paper’s zero-significant-disagreement statement in these simulations.' if contradictions else 'No book has a significant likelihood-ratio preference opposite to its sole accepted model in pass A.'
    if contradictions: replacements['CONTRADICTIONS']+=table(['PG identifier','KS group','R','pLR','K f1','K f2'],[[r['pg_id'],LABELS[r['category']],f"{r['R']:.6g}",f"{r['p_lr']:.6g}",r['K_f1'],r['K_f2']] for r in contradictions])
    replacements['MOMENTS']=table(['Model','Accepted books','Mean β','SD (population)','SD (sample)','Paper mean / SD'],[[m,f'{v["n_accepted"]:,}',number(v['mean'],'.4f'),number(v['sd_population'],'.4f'),number(v['sd_sample'],'.4f'),f'{v["printed"]["mean"]:.2f} / {v["printed"]["sd"]:.2f}'] for m,v in report['beta_moments'].items()])
    replacements['QUARTILES']=table(['Model / quartile','Books','Minimum L','Maximum L'],[[f'{m} / Q{i+1}',r['books'],number(r['min_L']),number(r['max_L'])] for m,groups in report['figure9_reconstructed_quartiles'].items() for i,r in enumerate(groups)])
    replacements['STABILITY']=table(['Model','Accepted A','Accepted B','A only','B only','Switches','Relative net change','κ'],[[m,f'{s["A_accepted"]:,}',f'{s["B_accepted"]:,}',s['A_only'],s['B_only'],f'{s["switches"]:,} ({100*s["switches"]/report["books"]:.2f}%)',number(None if s['relative_accepted_count_change'] is None else 100*s['relative_accepted_count_change'],'+.2f')+('%' if s['relative_accepted_count_change'] is not None else ''),number(s['kappa'],'.3f')] for m,s in report['stability'].items()])
    replacements['STABILITY_TABLES']=''.join(f'<h3>{m}</h3>'+table(['Pass A status','B accepted','B rejected'],[['A accepted',s['both_accept'],s['A_only']],['A rejected',s['B_only'],s['both_reject']]]) for m,s in report['stability'].items())
    predictions=report['exposed_prediction_checks']
    p=predictions['f2_switches_500_to_2000']
    replacements['EXPOSED_PREDICTIONS']=f"The exposed September pilot predicted 500–2,000 f2 switches: this run has {p['observed']:,} ({'within' if p['within_prediction'] else 'outside'} that range). It also predicted net accepted-count changes within ±4% relative: "+'; '.join(f"{m} is {'within' if v['within_prediction'] else 'outside' if v['within_prediction'] is False else 'unavailable for'} that range" for m,v in predictions['net_relative_change_within_4pct'].items())+'. These are exposed predictions, not acceptance gates.'
    replacements['PRECISION']=f"A predeclared hash ordering selected up to 50 book/model pairs from each pass-A K stratum 1–3, 4–5, 6–10 and 11–20, separately for each model. The audit covers {ps['selected_pairs']} pairs; the remaining {ps['not_precision_audited_pairs']:,} pairs have not received this precision audit. The subset does not estimate whole-corpus error rates."
    replacements['PRECISION_TABLE']=table(['Model','Rejected','Non-rejected','Unresolved'],[[m]+[v[s] for s in ('rejected','non_rejected','unresolved')] for m,v in ps['models'].items()])
    changed=precision_comparisons(pairs)
    replacements['PRECISION_TABLE']+=table(['Model','Accepted in A → rejected','Rejected in A → non-rejected'],[[m,*v.values()] for m,v in changed.items()])
    replacements['PRECISION_TABLE']+='<p class="note">These interval-resolved disagreements concern the selected subset only. Neither they nor the unresolved pairs establish whole-corpus error rates.</p>'
    replacements['STRATA']=table(['Model','Selecting K range','Candidate pairs','Audited'],[[f'f{s["model"]}',f'{s["stratum"][0]}–{s["stratum"][1]}',s['candidates'],s['selected']] for s in ps['strata']])
    strict=report['strict_p_sensitivity'];pool=report['pooled_B200_diagnostic']['accepted_counts']
    replacements['SENSITIVITY']=table(['Convention','f1 accepted / favored','f2 accepted / favored'],[
        ['Strict p > 0.05: accepted',strict.get('f1_only',0)+strict.get('both',0),strict.get('f2_only',0)+strict.get('both',0)],
        ['Pooled 200 draws: accepted',pool['f1'],pool['f2']],
        ['Sample-variance LR: significant preference, first three rows',*report['sample_variance_lr_sensitivity']['total_first_three_rows']]])
    replacements['SENSITIVITY']+=table(['KS group','Strict statistic-exceedance count (Dsim > Dobs)'],[[LABELS[k],v] for k,v in report['statistic_tie_sensitivity']['categories'].items()])
    replacements['SENSITIVITY']+=f"<p>There are {len(report['lr_degenerate_books'])} degenerate LR calculations and {len(report['zero_lr_books'])} exact zero LR values.</p>"
    primary=[c for c in calibration['cells'] if c['outer_tests']==2000]
    rates=[c['rejections_at_005']/2000 for c in primary]
    replacements['CALIBRATION']=f"All 39,600 outer simulated cases completed. The 18 primary cells each used 2,000 outer samples and 100 refitted inner draws; their 0.05 rejection rates ranged from {100*min(rates):.1f}% to {100*max(rates):.1f}%. All predeclared primary calibration and six large-sample estimator-recovery screens passed, with no recorded numerical exception. An independent reviewer recomputed the gates from the raw records."
    replacements['CALIBRATION_CELLS']=table(['Model','N types','True β','Outer tests','Rejected at .05','Adjusted interval','Mean β error'],[
        [f'f{c["model"]}',f'{c["N"]:,}',c['true_beta'],c['outer_tests'],f'{100*c["rejections_at_005"]/c["outer_tests"]:.2f}%',
         '–'.join(f'{100*x:.2f}%' for x in c['cp_interval_99pct_family']),f'{c["bias"]:+.5f}'] for c in calibration['cells']])
    replacements['REPORT_HASH']=report_hash
    portable_report=json.loads(json.dumps(report))
    for source in portable_report.get('source_passes',{}).values(): source.pop('path',None)
    replacements['DATA']=json.dumps({'report':portable_report,'precision_pairs':pairs,'calibration':calibration},ensure_ascii=True,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    template=(ROOT/'src/reader.html').read_text(encoding='utf-8')
    for key,value in replacements.items(): template=template.replace('@@'+key+'@@',value)
    if '@@' in template: raise ValueError('Unsubstituted reader placeholder')
    return template


def source_directory(source,override=None):
    if override is not None:
        return override
    # Read both historical Windows separators and portable serialized paths.
    path=Path(source['path'].replace('\\','/'))
    return path if path.is_absolute() else ROOT/path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,default=ROOT/'results/report.json')
    parser.add_argument('--A',type=Path,help='Override the hash-checked pass A directory')
    parser.add_argument('--B',type=Path,help='Override the hash-checked pass B directory')
    parser.add_argument('--precision',type=Path,default=ROOT/'results/precision-001')
    parser.add_argument('--calibration',type=Path,default=ROOT/'results/calibration-001')
    parser.add_argument('--out',type=Path,default=ROOT/'index.html')
    args=parser.parse_args()
    calibrated,calibration_hashes=reproduce.validate_calibration(args.calibration)
    report=json.loads(args.report.read_bytes())
    args.A=source_directory(report['source_passes']['A'],args.A)
    args.B=source_directory(report['source_passes']['B'],args.B)
    if report['source_passes']['A']['books_sha256']!=sha(args.A/'books.jsonl'):
        raise ValueError('Report pass A changed')
    passes={}
    for key in ('A','B'):
        source=report['source_passes'][key];directory=getattr(args,key)
        passes[key]=load_pass(directory,key)
        manifest=json.loads((directory/'manifest.json').read_bytes())
        for field in ('contract_sha256','environment'):
            if manifest[field]!=calibrated[field]: raise ValueError('Reader pass differs from calibration')
        if manifest['calibration_artifact_sha256']!=calibration_hashes:
            raise ValueError('Reader pass used another calibration')
        for name in ('models.py','reference.py','bootstrap.py'):
            if manifest['code_sha256'][name]!=calibrated['code_sha256'][name]:
                raise ValueError('Reader pass numerical implementation differs from calibration')
        if source['manifest_sha256']!=sha(directory/'manifest.json') or source['books_sha256']!=sha(directory/'books.jsonl'):
            raise ValueError('Report source pass changed')
    recomputed=build_report(passes['A'],passes['B'])
    for key,value in recomputed.items():
        if key!='high_precision_status' and report[key]!=value:
            raise ValueError(f'Report arithmetic changed: {key}')
    ingest_path=ROOT/'data/derived/ingest.json'
    am=json.loads((args.A/'manifest.json').read_bytes())
    if sha(ingest_path)!=am['ingest_json_sha256']: raise ValueError('Ingest changed')
    ingest=json.loads(ingest_path.read_bytes())
    if ingest['vectors']!=31075 or ingest['total_tokens']!=1961738645 or sum(r['L'] for r in passes['A'].values())!=1961738645:
        raise ValueError('Reader corpus totals differ')
    if len(ingest['length_anchor_checks'])!=5 or not all(c['pass'] and c['observed_L']==c['expected_L'] for c in ingest['length_anchor_checks'].values()):
        raise ValueError('Reader length anchors differ')
    anchors=json.loads((ROOT/'results/figure4-anchors.json').read_bytes())
    if len(anchors)!=2 or {(r['pg_id'],r['model']) for r in anchors}!={(27027,1),(9365,2)}:
        raise ValueError('Reader exponent-anchor coverage differs')
    for anchor in anchors:
        result=passes['A'][anchor['pg_id']][f'f{anchor["model"]}']
        if result['beta']!=anchor['beta'] or result['D']!=anchor['D'] or round(anchor['beta'],2)!=anchor['printed_beta']:
            raise ValueError('Reader exponent anchors differ')
    ps,pairs=load_precision(args.precision,args.A,report)
    calibration=json.loads((args.calibration/'summary.json').read_bytes())
    result=render(report,ps,pairs,calibration,sha(args.report))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(result.encode('utf-8'))
    print(json.dumps({'output':str(args.out),'bytes':args.out.stat().st_size,'sha256':sha(args.out)}))


if __name__=='__main__': main()
