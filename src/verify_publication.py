"""Verify public package bytes, links, credits and protected scientific identities."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'PACKAGE-MANIFEST.json'
IGNORED={'PACKAGE-MANIFEST.json','data/raw/PG_English_wordfreqs.zip','paper/paper.pdf','paper/paper.txt'}
PROTECTED=('models.py','reference.py','bootstrap.py','calibrate.py','reproduce.py','precision.py','ingest.py')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    return {p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file()
            and not any(x in p.relative_to(ROOT).parts for x in ('.git','.venv','__pycache__','work'))
            and p.suffix!='.pyc' and p.relative_to(ROOT).as_posix() not in IGNORED}


class Reader(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.anchors=[];self.external_assets=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('#'):self.anchors.append(a['href'][1:])
        if (tag=='script' and a.get('src')) or (tag=='link' and a.get('rel')=='stylesheet'):
            self.external_assets.append(a)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest',action='store_true',help='Record intentionally reviewed package changes')
    args=parser.parse_args();files=inventory()
    if any(p.stat().st_size>=100*1024*1024 for p in files.values()):raise ValueError('File exceeds GitHub normal blob limit')
    for name,p in files.items():
        if p.suffix in ('.md','.json','.jsonl','.csv','.py','.html','.svg','.txt','.cff') or p.name in ('LICENSE','REPORT-LICENSE'):
            raw=p.read_bytes();text=raw.decode('utf-8')
            if b'\r\n' in raw:raise ValueError(f'CRLF drift: {name}')
            private_pattern=r'[A-Za-z]:[\\/]Users[\\/]|/'+'root/'+r'|gh[pousr]_[A-Za-z0-9]{30}|github_pat_[A-Za-z0-9_]{30}|sk-proj-[A-Za-z0-9]{20}'
            if re.search(private_pattern,text):
                raise ValueError(f'Private path or credential-shaped string: {name}')
    receipt=json.loads((ROOT/'EXPORT-TRANSFORMATIONS.json').read_bytes())
    for name,digest in receipt['source_sha256'].items():
        if name.startswith(('results/pass-','results/calibration-001/','results/precision-001/','data/derived/')) or name in ('planning/AMENDMENT-1.md','planning/CONTRACT-FREEZE.json') or name in {f'src/{x}' for x in PROTECTED}:
            if sha(ROOT/name)!=digest:raise ValueError(f'Protected scientific artifact changed: {name}')
    for name,change in receipt['transformations'].items():
        if sha(ROOT/name)!=change['export_sha256']:raise ValueError(f'Stale transformation receipt: {name}')
    html=(ROOT/'index.html').read_text(encoding='utf-8');dom=Reader(html)
    if len(dom.ids)!=len(set(dom.ids)) or not set(dom.anchors)<=set(dom.ids):raise ValueError('Reader anchor identity error')
    if dom.external_assets or '@@' in html:raise ValueError('Reader external runtime asset or placeholder')
    for token in ('OpenAI Codex (GPT-6)','Gemini 4 Carbon (High)','CC BY 4.0','MIT','Partial numerical reproduction.'):
        if token not in html:raise ValueError(f'Reader lacks required credit/license/verdict: {token}')
    report=json.loads((ROOT/'results/report.json').read_bytes())
    if report['acceptance']['f1']['observed']!=4724 or report['acceptance']['f2']['observed']!=12496 or report['all_declared_table_bands_pass']:
        raise ValueError('Primary headline differs from release result')
    payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',html,re.S).group(1))
    portable=json.loads(json.dumps(report))
    for source in portable['source_passes'].values():source.pop('path',None)
    if payload['report']!=portable:raise ValueError('Embedded report differs')
    entries={name:{'bytes':p.stat().st_size,'sha256':sha(p)} for name,p in sorted(files.items())}
    if args.write_manifest:
        MANIFEST.write_bytes((json.dumps({'algorithm':'SHA-256','excludes':sorted(IGNORED),'files':entries},indent=2)+'\n').encode())
    else:
        recorded=json.loads(MANIFEST.read_bytes())['files']
        if entries!=recorded:raise ValueError('Package inventory/hashes changed; review before refreshing manifest')
    print(json.dumps({'status':'PASS','files':len(entries),'html_ids':len(dom.ids),'primary_result':'partial; five failed comparisons retained'}))


if __name__=='__main__':main()
