"""Prespecified stratified follow-up; fresh fixed B=10000 per selected pair."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[_name]='1'
import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import hashlib
import json
import math
from pathlib import Path
import time
import traceback
import numpy as np
from . import reproduce
from .report import load_pass
from .models import Histogram
from .bootstrap import bootstrap
from .calibrate import cp_interval

ROOT=Path(__file__).resolve().parents[1]
STRATA=((1,3),(4,5),(6,10),(11,20))


def select_pairs(books):
    selected=[]
    for model in (1,2):
        for low,high in STRATA:
            candidates=[r for r in books.values() if low<=r[f'f{model}']['K_ge']<=high]
            candidates.sort(key=lambda r:(hashlib.sha256(f"2026111705:{model}:{r['pg_id']}".encode()).hexdigest(),r['pg_id']))
            for row in candidates[:50]:
                selected.append({'model':model,'pg_id':row['pg_id'],'stratum':[low,high],
                                 'candidate_count':len(candidates),'selecting_K':row[f'f{model}']['K_ge'],
                                 'beta_expected':row[f'f{model}']['beta'],'D_expected':row[f'f{model}']['D']})
    return selected


def precision_task(task):
    selected,metadata=task
    model,pg=selected['model'],selected['pg_id']
    try:
        start=time.perf_counter()
        data=reproduce.ARCHIVE.read(f'PG_English_wordfreqs/PG{pg}.freqs')
        if hashlib.sha256(data).hexdigest()!=metadata['sha256']: raise ValueError('Book hash changed')
        values=list(map(int,data.splitlines()))
        h=Histogram.from_sample(values)
        if h.N!=int(metadata['N']) or sum(values)!=int(metadata['L']): raise ValueError('Metadata mismatch')
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([2026111705,model,pg])))
        result=bootstrap(model,h,10000,rng)
        if result['beta']!=selected['beta_expected'] or result['D']!=selected['D_expected']:
            raise ValueError('Fitted statistic changed since selecting pass')
        lo,hi=cp_interval(result['K_ge'],10000,.05)
        result.update(selected)
        result.update({'seed':2026111705,'N':h.N,'L':sum(values),'source_sha256':metadata['sha256'],
                       'cp95':[lo,hi],'precision_status':'rejected' if hi<.05 else 'non_rejected' if lo>=.05 else 'unresolved',
                       'worst_case_mc_se':.005,'elapsed_seconds':time.perf_counter()-start})
        return result
    except Exception as exc:
        return {'model':model,'pg_id':pg,'error_type':type(exc).__name__,'error_message':str(exc),'traceback':traceback.format_exc()}


def validate_pair(result,selection,metadata):
    for key in ('model','pg_id'):
        if type(result.get(key)) is not int or result[key]!=selection[key]:
            raise ValueError('Precision identity must be exact integers')
    for key,value in selection.items():
        if result.get(key)!=value: raise ValueError('Precision record selection mismatch')
    for key,value in (('N',int(metadata['N'])),('L',int(metadata['L'])),('seed',2026111705),('B',10000)):
        if type(result.get(key)) is not int or result[key]!=value: raise ValueError('Precision record identity mismatch')
    if result['source_sha256']!=metadata['sha256'] or result['beta']!=selection['beta_expected'] or result['D']!=selection['D_expected']:
        raise ValueError('Precision record source or statistic changed')
    for key in ('K_ge','K_gt','ties','raw_float_ties','ks_refinements','inverse_refinements','large_integers'):
        if type(result.get(key)) is not int or result[key]<0: raise ValueError('Invalid precision count')
    if not 0<=result['K_gt']<=result['K_ge']<=10000 or result['ties']!=result['K_ge']-result['K_gt']:
        raise ValueError('Invalid precision trial counts')
    if not max(result['ties'],result['raw_float_ties'])<=result['ks_refinements']<=10000 or result['large_integers']>result['inverse_refinements']:
        raise ValueError('Invalid precision refinement counts')
    lo,hi=cp_interval(result['K_ge'],10000,.05)
    if any(not math.isclose(x,y,rel_tol=0,abs_tol=1e-15) for x,y in zip(result['cp95'],(lo,hi))) or len(result['cp95'])!=2:
        raise ValueError('Precision interval does not follow its trials')
    expected='rejected' if hi<.05 else 'non_rejected' if lo>=.05 else 'unresolved'
    if result['precision_status']!=expected or result['worst_case_mc_se']!=.005:
        raise ValueError('Invalid precision interpretation')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--A',type=Path,required=True)
    parser.add_argument('--calibration',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=8)
    args=parser.parse_args()
    if not 1<=args.workers<=8: parser.error('workers must be1..8')
    calibrated,calibration_hashes=reproduce.validate_calibration(args.calibration)
    books=load_pass(args.A,'A')
    source_manifest=json.loads((args.A/'manifest.json').read_bytes())
    for key in ('contract_sha256','environment'):
        if source_manifest[key]!=calibrated[key]: raise ValueError('Selecting pass differs from calibration')
    if source_manifest['calibration_artifact_sha256']!=calibration_hashes:
        raise ValueError('Selecting pass used another calibration')
    for name in ('models.py','reference.py','bootstrap.py'):
        if source_manifest['code_sha256'][name]!=hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest():
            raise ValueError('Selecting-pass numerical code changed')
    selected=select_pairs(books)
    selection_by_key={(r['model'],r['pg_id']):r for r in selected}
    archive_hash=hashlib.sha256((ROOT/'data/raw/PG_English_wordfreqs.zip').read_bytes()).hexdigest()
    ingest_path=ROOT/'data/derived/ingest.json';csv_path=ROOT/'data/derived/books.csv'
    ingest_hash=hashlib.sha256(ingest_path.read_bytes()).hexdigest()
    csv_hash=hashlib.sha256(csv_path.read_bytes()).hexdigest()
    ingest=json.loads(ingest_path.read_bytes())
    if archive_hash!=source_manifest['archive_sha256'] or archive_hash!=ingest['archive_sha256']:
        raise ValueError('Follow-up archive changed')
    if csv_hash!=source_manifest['books_csv_sha256'] or csv_hash!=ingest['books_csv_sha256'] or ingest_hash!=source_manifest['ingest_json_sha256']:
        raise ValueError('Follow-up metadata changed')
    with (ROOT/'data/derived/books.csv').open(encoding='utf-8',newline='') as source:
        metadata={int(r['pg_id']):r for r in csv.DictReader(source)}
    identity={'seed':2026111705,'B':10000,'contract_sha256':calibrated['contract_sha256'],
              'calibration_artifact_sha256':calibration_hashes,
              'environment':calibrated['environment'],
              'archive_sha256':archive_hash,'books_csv_sha256':csv_hash,'ingest_json_sha256':ingest_hash,
              'selecting_manifest_sha256':hashlib.sha256((args.A/'manifest.json').read_bytes()).hexdigest(),
              'selecting_completion_sha256':hashlib.sha256((args.A/'completion.json').read_bytes()).hexdigest(),
              'selecting_pass_sha256':hashlib.sha256((args.A/'books.jsonl').read_bytes()).hexdigest(),
              'code_sha256':{name:hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest() for name in ('models.py','reference.py','bootstrap.py','precision.py')},
              'selection':selected,'ci_confidence':.95,'interval_scope':'pointwise; selection trials excluded'}
    args.out.mkdir(parents=True,exist_ok=True)
    manifest=args.out/'manifest.json';checkpoint=args.out/'pairs.jsonl'
    reproduce.require_manifest_for_checkpoint(checkpoint,manifest)
    encoded=(json.dumps(identity,indent=2)+'\n').encode('utf-8')
    if manifest.exists() and manifest.read_bytes()!=encoded: raise ValueError('Follow-up identity changed')
    manifest.write_bytes(encoded)
    rows=[json.loads(line) for line in checkpoint.read_bytes().splitlines()] if checkpoint.exists() else []
    expected={(r['model'],r['pg_id']) for r in selected}
    done={(r['model'],r['pg_id']) for r in rows}
    if len(done)!=len(rows) or not done<=expected: raise ValueError('Invalid follow-up coverage')
    for r in rows:
        validate_pair(r,selection_by_key[(r['model'],r['pg_id'])],metadata[r['pg_id']])
    tasks=[(r,metadata[r['pg_id']]) for r in selected if (r['model'],r['pg_id']) not in done]
    start=time.perf_counter()
    with checkpoint.open('ab') as output, ProcessPoolExecutor(max_workers=args.workers,initializer=reproduce.init_worker) as pool:
        for result in pool.map(precision_task,tasks,chunksize=1):
            if 'error_type' in result:
                with (args.out/'errors.jsonl').open('ab') as errors: errors.write((json.dumps(result)+'\n').encode('utf-8'))
                pool.shutdown(wait=True,cancel_futures=True)
                raise RuntimeError(f"Precision task failed: {result['model']}/{result['pg_id']}: {result['error_message']}")
            try:
                validate_pair(result,selection_by_key[(result['model'],result['pg_id'])],metadata[result['pg_id']])
            except Exception as exc:
                with (args.out/'errors.jsonl').open('ab') as errors:
                    errors.write((json.dumps({'model':result.get('model'),'pg_id':result.get('pg_id'),'error_type':type(exc).__name__,'error_message':str(exc)})+'\n').encode('utf-8'))
                pool.shutdown(wait=True,cancel_futures=True)
                raise
            output.write((json.dumps(result,separators=(',',':'))+'\n').encode('utf-8'));output.flush()
            rows.append(result)
            if len(rows)%10==0: print(f'Precision: {len(rows)}/{len(expected)} pairs; {time.perf_counter()-start:.1f}s',flush=True)
    persisted=[json.loads(line) for line in checkpoint.read_bytes().splitlines()]
    if len(persisted)!=len(expected) or {(r['model'],r['pg_id']) for r in persisted}!=expected:
        raise ValueError('Incomplete persisted precision results')
    for r in persisted: validate_pair(r,selection_by_key[(r['model'],r['pg_id'])],metadata[r['pg_id']])
    summary={'complete':True,'selected_pairs':len(persisted),'pairs_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
             'models':{f'f{m}':{status:sum(r['model']==m and r['precision_status']==status for r in persisted) for status in ('rejected','non_rejected','unresolved')} for m in (1,2)},
             'strata':[{'model':m,'stratum':[lo,hi],
                        'candidates':sum(lo<=r[f'f{m}']['K_ge']<=hi for r in books.values()),
                        'selected':sum(r['model']==m and r['stratum']==[lo,hi] for r in persisted)}
                       for m in (1,2) for lo,hi in STRATA],
             'not_precision_audited_pairs':2*31075-len(persisted),
             'interpretation':'Stratified selected subset; pointwise conditional Monte Carlo intervals, no whole-corpus extrapolation',
             'wall_seconds_this_invocation':time.perf_counter()-start}
    (args.out/'summary.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
