"""Retrieve excluded source bytes without altering preserved derived manifests."""
import argparse
import hashlib
from pathlib import Path
import tempfile
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
    'data/raw/PG_English_wordfreqs.zip':(
        'https://ndownloader.figshare.com/files/2284750',26349768,
        '6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61'),
    'paper/paper.pdf':(
        'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0147073&type=printable',2017278,
        '5234b7edbd72dc71989dbcc87d3fb712af5db136ef5203e625920f24148c971d'),
}


def import_source(name,source):
    _,size,digest=SOURCES[name]
    payload=source.read_bytes()
    if len(payload)!=size or hashlib.sha256(payload).hexdigest()!=digest:
        raise ValueError(f'{name}: supplied file is not the recorded source; nothing installed')
    target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        if target.read_bytes()!=payload:raise ValueError(f'Existing {name} differs; left untouched')
    else:
        with target.open('xb') as sink:sink.write(payload)
    print(f'Imported and verified {name}')


def fetch(name):
    url,size,digest=SOURCES[name]
    target=ROOT/name
    if target.exists():
        if target.stat().st_size!=size or hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Existing {name} differs from the recorded source; left untouched')
        print(f'Verified existing {name}')
        return
    target.parent.mkdir(parents=True,exist_ok=True)
    temp=None
    try:
        request=Request(url,headers={'User-Agent':'Gutenberg-Zipf-Reproduction/1.0'})
        with urlopen(request,timeout=60) as response, tempfile.NamedTemporaryFile(dir=target.parent,suffix='.part',delete=False) as sink:
            temp=Path(sink.name);hasher=hashlib.sha256();received=0
            while chunk:=response.read(1024*1024):
                received+=len(chunk)
                if received>size: raise ValueError(f'{name}: source exceeds the recorded byte count')
                sink.write(chunk);hasher.update(chunk)
        if received!=size or hasher.hexdigest()!=digest:
            raise ValueError(f'{name}: source checksum/size mismatch; no file installed')
        # Exclusive creation preserves any file another process created during download.
        with target.open('xb') as sink, temp.open('rb') as source:
            while chunk:=source.read(1024*1024):sink.write(chunk)
        print(f'Downloaded and verified {name}: {digest}')
    finally:
        if temp is not None:temp.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper',action='store_true',help='Also retrieve the publisher PDF')
    parser.add_argument('--archive',type=Path,help='Import an already downloaded frequency ZIP after exact verification')
    parser.add_argument('--paper-file',type=Path,help='Import an already downloaded publisher PDF after exact verification')
    args=parser.parse_args()
    if args.archive:import_source('data/raw/PG_English_wordfreqs.zip',args.archive)
    if args.paper_file:import_source('paper/paper.pdf',args.paper_file)
    try:
        fetch('data/raw/PG_English_wordfreqs.zip')
        if args.paper or args.paper_file:fetch('paper/paper.pdf')
    except URLError as exc:
        parser.exit(1,f'Source download failed: {exc}. Download through the credited Figshare/publisher page, then use --archive PATH or --paper-file PATH to import the exact recorded bytes. No derived manifest was changed.\n')


if __name__=='__main__':main()
