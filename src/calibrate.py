"""Checkpointed synthetic calibration. No real corpus vectors are read."""
from __future__ import annotations
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[_name]='1'

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

import mpmath
import numpy as np
import scipy
from scipy.stats import beta as beta_distribution, norm
from .models import HeadTailSampler
from .bootstrap import bootstrap

ROOT=Path(__file__).resolve().parents[1]
BETAS=(1.5,2.,3.)
MAIN_N=(300,3000,30000)
DIAGNOSTIC_N=(27,84,210347)


def task_key(task):
    return ':'.join(map(str,task[:4]))


def _run_task(task):
    model,N,index,outer,mode,cell_index=task
    start=time.perf_counter()
    def rng(role):
        entropy=([2026111701,model,N,index,outer,role] if mode=='full'
                 else [2026111702,10000+cell_index*100+outer*2+role,model])
        return np.random.Generator(np.random.PCG64(np.random.SeedSequence(entropy)))
    generator=HeadTailSampler(model,BETAS[index])
    sample=generator.sample(N,rng(0))
    result=bootstrap(model,sample,100,rng(1))
    result.update({'key':task_key(task),'model':model,'N':N,'true_beta':BETAS[index],
                   'outer_index':outer,'diagnostic':N in DIAGNOSTIC_N,
                   'outer_inverse_refinements':generator.refinements,
                   'outer_large_integers':generator.large_integers,
                   'elapsed_seconds':time.perf_counter()-start})
    return result


def run_task(task):
    try:
        return _run_task(task)
    except Exception as exc:
        return {'key':task_key(task),'task':task,'error_type':type(exc).__name__,
                'error_message':str(exc),'traceback':traceback.format_exc()}


def cp_interval(k,n,alpha):
    return (0. if k==0 else float(beta_distribution.ppf(alpha/2,k,n-k+1)),
            1. if k==n else float(beta_distribution.ppf(1-alpha/2,k+1,n-k)))


def summarize(rows,mode):
    expected={f'{model}:{N}:{index}:{outer}' for model in (1,2)
              for N in MAIN_N+DIAGNOSTIC_N for index in range(3)
              for outer in range(2 if mode=='benchmark' else (2000 if N in MAIN_N else 200))}
    actual=[r['key'] for r in rows]
    if len(set(actual))!=len(actual) or set(actual)!=expected:
        raise ValueError('Summary requires the exact complete task key set')
    for r in rows:
        model,N,index,outer=map(int,r['key'].split(':'))
        if (r['model'],r['N'],r['true_beta'],r['outer_index'],r['B'])!=(model,N,BETAS[index],outer,100):
            raise ValueError('Task fields do not match its declared identity')
        if not 0<=r['K_gt']<=r['K_ge']<=100 or r['K_ge']-r['K_gt']!=r['ties']:
            raise ValueError('Invalid exceedance counts')
    cells=[]
    for model in (1,2):
        for N in MAIN_N+DIAGNOSTIC_N:
            for true in BETAS:
                group=[r for r in rows if r['model']==model and r['N']==N and r['true_beta']==true]
                expected_count=2 if mode=='benchmark' else (2000 if N in MAIN_N else 200)
                if len(group)!=expected_count:
                    raise ValueError('Calibration cell is incomplete')
                fitted=np.asarray([r['beta'] for r in group])
                k=[r['K_ge'] for r in group]
                reject=sum(x<5 for x in k)
                lo,hi=cp_interval(reject,len(group),.01/18)
                bias=float(fitted.mean()-true)
                se=float(fitted.std(ddof=1)/np.sqrt(len(group))) if len(group)>1 else None
                recovery=None
                if N==30000 and se is not None:
                    margin=float(norm.ppf(1-.01/12))*se
                    recovery={'bias_interval':[bias-margin,bias+margin], 'pass':abs(bias)+margin<=.005}
                gate=(lo>=5/101-.03 and hi<=5/101+.03) if N in MAIN_N else None
                cells.append({'model':model,'N':N,'true_beta':true,'outer_tests':len(group),
                    'mean_beta':float(fitted.mean()),'bias':bias,'bias_mc_se':se,
                    'sd_beta':float(fitted.std(ddof=1)),
                    'K_ge_histogram':np.bincount(k,minlength=101).tolist(),
                    'ties_total':sum(r['ties'] for r in group),
                    'raw_float_ties_total':sum(r['raw_float_ties'] for r in group),
                    'rejections_at_005':reject,'cp_interval_99pct_family':[lo,hi],
                    'calibration_screen_pass':gate,'recovery':recovery,
                    'rejection_rates':{str(p):sum(x<round(p*100) for x in k)/len(k) for p in (.01,.05,.2,.5)},
                    'median_task_seconds':float(np.median([r['elapsed_seconds'] for r in group])),
                    'max_task_seconds':max(r['elapsed_seconds'] for r in group),
                    'ks_refinements':sum(r['ks_refinements'] for r in group),
                    'inverse_refinements':sum(r['inverse_refinements']+r['outer_inverse_refinements'] for r in group),
                    'large_integers':sum(r['large_integers']+r['outer_large_integers'] for r in group)})
    complete=(mode=='full' and len(rows)==39600)
    passed=complete and all(c['calibration_screen_pass'] for c in cells if c['N'] in MAIN_N) and all(c['recovery']['pass'] for c in cells if c['recovery'] is not None)
    projected=sum(c['median_task_seconds']*(2000 if c['N'] in MAIN_N else 200) for c in cells)
    return {'mode':mode,'completed_tasks':len(rows),'expected_full_tasks':39600,
            'complete':complete,'calibration_pass':bool(passed),'cells':cells,
            'projected_sequential_seconds_from_cell_medians':projected,
            'note':'Benchmark outcomes are timing diagnostics only; full gate cannot pass in benchmark mode.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=('benchmark','full'),required=True)
    parser.add_argument('--workers',type=int,default=1)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if not 1<=args.workers<=8: parser.error('workers must be 1..8')
    args.out.mkdir(parents=True,exist_ok=True)
    manifest={'mode':args.mode,'contract_sha256':hashlib.sha256((ROOT/'planning/AMENDMENT-1.md').read_bytes()).hexdigest(),
              'code_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').glob('*.py'))},
              'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__},
              'random_engine':'PCG64','B':100,'main_outer':2000,'diagnostic_outer':200,
              'main_N':MAIN_N,'diagnostic_N':DIAGNOSTIC_N,'betas':BETAS}
    manifest_data=(json.dumps(manifest,indent=2)+'\n').encode('utf-8')
    manifest_path=args.out/'manifest.json'
    if manifest_path.exists() and manifest_path.read_bytes()!=manifest_data:
        raise ValueError('Run identity changed; use a new output directory')
    manifest_path.write_bytes(manifest_data)
    path=args.out/'tasks.jsonl'
    rows=[json.loads(line) for line in path.read_bytes().splitlines()] if path.exists() else []
    completed={r['key'] for r in rows}
    if len(completed)!=len(rows): raise ValueError('Duplicate checkpoint task')
    tasks=[]
    cell=0
    for model in (1,2):
        for N in MAIN_N+DIAGNOSTIC_N:
            for index in range(3):
                count=2 if args.mode=='benchmark' else (2000 if N in MAIN_N else 200)
                for outer in range(count):
                    task=(model,N,index,outer,args.mode,cell)
                    if task_key(task) not in completed: tasks.append(task)
                cell+=1
    start=time.perf_counter()
    with path.open('ab') as output, ProcessPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(run_task,tasks,chunksize=1 if args.mode=='benchmark' else 5):
            if 'error_type' in result:
                with (args.out/'errors.jsonl').open('ab') as errors:
                    errors.write((json.dumps(result)+'\n').encode('utf-8'))
                pool.shutdown(wait=True,cancel_futures=True)
                raise RuntimeError(f"Calibration task {result['key']} failed: {result['error_type']}: {result['error_message']}")
            rows.append(result)
            output.write((json.dumps(result,separators=(',',':'))+'\n').encode('utf-8'))
            output.flush()
            if len(rows)%20==0:
                print(f'{args.mode}: {len(rows)} tasks complete; elapsed {time.perf_counter()-start:.1f}s',flush=True)
    summary=summarize(rows,args.mode)
    summary['wall_seconds_this_invocation']=time.perf_counter()-start
    (args.out/'summary.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf-8'))
    print(json.dumps({k:v for k,v in summary.items() if k!='cells'},indent=2))
    if args.mode=='full' and not summary['calibration_pass']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
