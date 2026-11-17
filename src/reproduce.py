"""One complete paper-like B=100 pass, gated on completed calibration."""
from __future__ import annotations
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
import sys
import time
import traceback
import zipfile
import numpy as np
import scipy
import mpmath
from .models import Histogram,likelihood_ratio
from .bootstrap import bootstrap
from .calibrate import summarize

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=None


def init_worker():
    global ARCHIVE
    ARCHIVE=zipfile.ZipFile(ROOT/'data/raw/PG_English_wordfreqs.zip')


def run_book(task):
    row,seed=task
    pg=int(row['pg_id'])
    try:
        start=time.perf_counter()
        payload=ARCHIVE.read(f'PG_English_wordfreqs/PG{pg}.freqs')
        if hashlib.sha256(payload).hexdigest()!=row['sha256']:
            raise ValueError('Book hash differs from validated input')
        sample=list(map(int,payload.splitlines()))
        histogram=Histogram.from_sample(sample)
        if histogram.N!=int(row['N']) or sum(sample)!=int(row['L']):
            raise ValueError('Book metadata mismatch')
        results={}
        for model in (1,2):
            rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed,model,pg])))
            results[f'f{model}']=bootstrap(model,histogram,100,rng)
        results.update({'pg_id':pg,'pass_seed':seed,'N':histogram.N,'L':sum(sample),'source_sha256':row['sha256'],
                        'lr':likelihood_ratio(histogram,results['f1']['beta'],results['f2']['beta']),
                        'elapsed_seconds':time.perf_counter()-start})
        return results
    except Exception as exc:
        return {'pg_id':pg,'error_type':type(exc).__name__,'error_message':str(exc),'traceback':traceback.format_exc()}


def validate_calibration(directory):
    summary=json.loads((directory/'summary.json').read_bytes())
    manifest=json.loads((directory/'manifest.json').read_bytes())
    required={'mode':'full','random_engine':'PCG64','B':100,'main_outer':2000,'diagnostic_outer':200,
              'main_N':[300,3000,30000],'diagnostic_N':[27,84,210347],'betas':[1.5,2.,3.]}
    if any(manifest.get(k)!=v for k,v in required.items()):
        raise ValueError('Calibration manifest is not the frozen full configuration')
    if not summary['complete'] or not summary['calibration_pass'] or summary['completed_tasks']!=39600:
        raise ValueError('Full frozen calibration gate has not passed')
    error_path=directory/'errors.jsonl'
    if error_path.exists() and error_path.stat().st_size:
        raise ValueError('Calibration has recorded numerical failures')
    task_data=(directory/'tasks.jsonl').read_bytes()
    recomputed=summarize([json.loads(line) for line in task_data.splitlines()],'full')
    if recomputed!={k:v for k,v in summary.items() if k!='wall_seconds_this_invocation'}:
        raise ValueError('Calibration summary differs from its task records')
    for name in ('models.py','reference.py','bootstrap.py','calibrate.py'):
        if hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest()!=manifest['code_sha256'][name]:
            raise ValueError(f'Calibrated implementation changed: {name}')
    if manifest['contract_sha256']!=hashlib.sha256((ROOT/'planning/AMENDMENT-1.md').read_bytes()).hexdigest():
        raise ValueError('Calibrated contract changed')
    runtime={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__}
    if runtime!=manifest['environment']:
        raise ValueError('Calibrated runtime changed')
    hashes={name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in ('manifest.json','tasks.jsonl','summary.json')}
    return manifest,hashes


def validate_book_result(result,source,seed):
    for key,expected in (('pg_id',int(source['pg_id'])),('N',int(source['N'])),('L',int(source['L'])),('pass_seed',seed)):
        if type(result.get(key)) is not int or result[key]!=expected:
            raise ValueError(f'Book record has invalid {key}')
    if result.get('source_sha256')!=source['sha256']:
        raise ValueError('Book record source hash mismatch')
    for model in ('f1','f2'):
        r=result[model]
        for key in ('B','K_ge','K_gt','ties','raw_float_ties','ks_refinements','inverse_refinements','large_integers'):
            if type(r.get(key)) is not int or r[key]<0: raise ValueError('Invalid bootstrap counter')
        if r['B']!=100 or not 0<=r['K_gt']<=r['K_ge']<=100 or r['ties']!=r['K_ge']-r['K_gt'] or r['raw_float_ties']>100:
            raise ValueError('Invalid book bootstrap counts')
        if not max(r['ties'],r['raw_float_ties'])<=r['ks_refinements']<=100 or r['large_integers']>r['inverse_refinements']:
            raise ValueError('Inconsistent numerical refinement counts')
        if not math.isfinite(r['beta']) or not 1<r['beta']<=4 or not math.isfinite(r['D']) or not 0<=r['D']<=1:
            raise ValueError('Invalid fitted result')
    lr=result['lr']
    if not math.isfinite(lr['R']) or not math.isfinite(lr['variance']) or lr['variance']<0 or type(lr['degenerate']) is not bool:
        raise ValueError('Invalid likelihood-ratio result')
    for field in ('p_lr','p_lr_sample'):
        if lr[field] is None:
            if not lr['degenerate']: raise ValueError('Unexplained missing LR significance')
        elif not math.isfinite(lr[field]) or not 0<=lr[field]<=1:
            raise ValueError('Invalid LR p-value')
    if lr['variance']==0:
        expected_degenerate=lr['R']!=0
        if lr['degenerate']!=expected_degenerate or any(lr[f]!=(None if expected_degenerate else 1.) for f in ('p_lr','p_lr_sample')):
            raise ValueError('Inconsistent degenerate LR state')
    else:
        if lr['degenerate']: raise ValueError('Positive LR variance marked degenerate')
        N=result['N']
        for field,variance in (('p_lr',lr['variance']),('p_lr_sample',lr['variance']*N/(N-1))):
            expected=math.erfc(abs(lr['R'])/math.sqrt(2*N*variance))
            if not math.isclose(lr[field],expected,rel_tol=1e-12,abs_tol=2e-15):
                raise ValueError('Stored LR significance does not follow its statistics')


def require_manifest_for_checkpoint(checkpoint,manifest):
    if checkpoint.exists() and not manifest.exists():
        raise ValueError('Orphan checkpoint has no manifest')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pass-name',choices=('A','B'),required=True)
    parser.add_argument('--calibration',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=8)
    args=parser.parse_args()
    if not 1<=args.workers<=8: parser.error('workers must be1..8')
    calibration,calibration_hashes=validate_calibration(args.calibration)
    archive=ROOT/'data/raw/PG_English_wordfreqs.zip'
    if hashlib.sha256(archive.read_bytes()).hexdigest()!='6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61':
        raise ValueError('Archive changed')
    books_path=ROOT/'data/derived/books.csv'
    ingest=json.loads((ROOT/'data/derived/ingest.json').read_bytes())
    if ingest['archive_sha256']!='6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61':
        raise ValueError('Ingest names another archive')
    if hashlib.sha256(books_path.read_bytes()).hexdigest()!=ingest['books_csv_sha256']:
        raise ValueError('Validated book metadata changed')
    with books_path.open(encoding='utf-8',newline='') as source: books=list(csv.DictReader(source))
    expected={int(r['pg_id']) for r in books}
    by_id={int(r['pg_id']):r for r in books}
    if len(books)!=31075 or len(expected)!=31075: raise ValueError('Input book coverage mismatch')
    seed=2026111703 if args.pass_name=='A' else 2026111704
    manifest={'pass':args.pass_name,'seed':seed,'B':100,'expected_books':31075,
              'contract_sha256':calibration['contract_sha256'],'environment':calibration['environment'],
              'code_sha256':{name:hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest() for name in ('models.py','reference.py','bootstrap.py','reproduce.py')},
              'calibration_artifact_sha256':calibration_hashes,
              'ingest_json_sha256':hashlib.sha256((ROOT/'data/derived/ingest.json').read_bytes()).hexdigest(),
              'books_csv_sha256':ingest['books_csv_sha256'],'archive_sha256':ingest['archive_sha256']}
    args.out.mkdir(parents=True,exist_ok=True)
    manifest_bytes=(json.dumps(manifest,indent=2)+'\n').encode('utf-8')
    target=args.out/'manifest.json'
    checkpoint=args.out/'books.jsonl'
    require_manifest_for_checkpoint(checkpoint,target)
    if target.exists() and target.read_bytes()!=manifest_bytes: raise ValueError('Run identity changed')
    target.write_bytes(manifest_bytes)
    previous=[json.loads(line) for line in checkpoint.read_bytes().splitlines()] if checkpoint.exists() else []
    for record in previous:
        if record.get('pg_id') not in by_id: raise ValueError('Unknown checkpoint book')
        validate_book_result(record,by_id[record['pg_id']],seed)
    done=[r['pg_id'] for r in previous]
    if len(done)!=len(set(done)) or not set(done)<=expected: raise ValueError('Invalid checkpoint coverage')
    done_set=set(done)
    tasks=[(row,seed) for row in books if int(row['pg_id']) not in done_set]
    start=time.perf_counter()
    with checkpoint.open('ab') as output, ProcessPoolExecutor(max_workers=args.workers,initializer=init_worker) as pool:
        for result in pool.map(run_book,tasks,chunksize=5):
            if 'error_type' in result:
                with (args.out/'errors.jsonl').open('ab') as errors: errors.write((json.dumps(result)+'\n').encode('utf-8'))
                pool.shutdown(wait=True,cancel_futures=True)
                raise RuntimeError(f"Book {result['pg_id']} failed: {result['error_message']}")
            try:
                validate_book_result(result,by_id[result['pg_id']],seed)
            except Exception as exc:
                with (args.out/'errors.jsonl').open('ab') as errors:
                    errors.write((json.dumps({'pg_id':result.get('pg_id'),'error_type':type(exc).__name__,'error_message':str(exc),'stage':'record_validation'})+'\n').encode('utf-8'))
                pool.shutdown(wait=True,cancel_futures=True)
                raise
            output.write((json.dumps(result,separators=(',',':'))+'\n').encode('utf-8'))
            output.flush()
            done_set.add(result['pg_id'])
            if len(done_set)%500==0: print(f"Pass {args.pass_name}: {len(done_set)}/31075 books; {time.perf_counter()-start:.1f}s",flush=True)
    persisted=[json.loads(line) for line in checkpoint.read_bytes().splitlines()]
    persisted_ids=[r['pg_id'] for r in persisted]
    if len(persisted_ids)!=31075 or len(set(persisted_ids))!=31075 or set(persisted_ids)!=expected:
        raise ValueError('Incomplete or duplicate persisted output coverage')
    for result in persisted: validate_book_result(result,by_id[result['pg_id']],seed)
    completion={'pass':args.pass_name,'books':len(done_set),'complete':True,'wall_seconds_this_invocation':time.perf_counter()-start,
                'books_jsonl_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest()}
    (args.out/'completion.json').write_bytes((json.dumps(completion,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(completion,indent=2))


if __name__=='__main__': main()
