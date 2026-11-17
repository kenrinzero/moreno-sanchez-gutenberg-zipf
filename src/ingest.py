"""Validate the exact released frequency ZIP; never extract archive paths."""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import re
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MD5 = 'e269dc5e82b0038aae9f9e297dcdb286'
EXPECTED_SHA256 = '6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61'
NAME = re.compile(r'PG_English_wordfreqs/PG([1-9][0-9]*)\.freqs\Z')


def main() -> None:
    started = time.perf_counter()
    archive = ROOT / 'data/raw/PG_English_wordfreqs.zip'
    raw = archive.read_bytes()
    if len(raw) != 26349768 or hashlib.md5(raw).hexdigest() != EXPECTED_MD5 or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Released archive identity mismatch')
    rows = []
    seen = set()
    metadata_count = 0
    directories = 0
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for entry in zf.infolist():
            if entry.filename.startswith('__MACOSX/'):
                metadata_count += 1
                continue
            if entry.is_dir():
                directories += 1
                continue
            match = NAME.fullmatch(entry.filename)
            if not match:
                raise ValueError(f'Unrecognized data member: {entry.filename!r}')
            pg_id = int(match.group(1))
            if pg_id in seen:
                raise ValueError(f'Duplicate PG identifier: {pg_id}')
            seen.add(pg_id)
            content = zf.read(entry)  # zipfile checks this member's CRC.
            lines = content.splitlines()
            if not lines or any(not line or not line.isdigit() for line in lines):
                raise ValueError(f'Non-positive-integer syntax: {entry.filename}')
            frequencies = list(map(int, lines))
            if min(frequencies) <= 0:
                raise ValueError(f'Nonpositive frequency: {entry.filename}')
            if any(a > b for a, b in zip(frequencies, frequencies[1:])):
                raise ValueError(f'Vector is not sorted ascending: {entry.filename}')
            length = sum(frequencies)
            if length <= 100:
                raise ValueError(f'L<=100: {entry.filename}')
            rows.append({'pg_id': pg_id, 'N': len(frequencies), 'L': length,
                         'hapax_types': frequencies.count(1), 'max_frequency': frequencies[-1],
                         'member_bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
            if len(rows) % 5000 == 0:
                print(f'Validated {len(rows)} vectors', flush=True)
    if len(rows) != 31075:
        raise ValueError(f'Unexpected corpus size: {len(rows)}')
    rows.sort(key=lambda row: row['pg_id'])
    by_id = {row['pg_id']: row for row in rows}
    anchors = {29156:115, 29765:4659068, 27027:83720, 9365:239018, 28879:2081}
    checks = {str(pg_id): {'observed_L': by_id[pg_id]['L'], 'expected_L': expected,
                           'pass': by_id[pg_id]['L'] == expected} for pg_id,expected in anchors.items()}
    if not all(check['pass'] for check in checks.values()):
        raise ValueError(f'Length anchor mismatch: {checks}')
    sorted_lengths = sorted(row['L'] for row in rows)
    edge_values = (115,5291,25739,34378,89476,103767)
    edge_ranks = {str(value): [i+1 for i,length in enumerate(sorted_lengths) if length == value] for value in edge_values}
    derived = ROOT / 'data/derived'
    derived.mkdir(parents=True, exist_ok=True)
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    csv_data = out.getvalue().encode('utf-8')
    (derived/'books.csv').write_bytes(csv_data)
    report = {
        'date':'2026-11-17', 'archive_sha256': EXPECTED_SHA256,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'books_csv_sha256':hashlib.sha256(csv_data).hexdigest(),
        'vectors':len(rows), 'unique_ids':len(seen), 'metadata_entries_ignored':metadata_count,
        'other_directories':directories, 'positive_integer_sorted_vectors':True,
        'minimum':min(rows,key=lambda row:row['L']), 'maximum':max(rows,key=lambda row:row['L']),
        'total_tokens':sum(row['L'] for row in rows), 'total_types_across_books':sum(row['N'] for row in rows),
        'minimum_type_count':min(row['N'] for row in rows),
        'maximum_type_count':max(row['N'] for row in rows),
        'books_with_N_below_300':sum(row['N'] < 300 for row in rows),
        'length_anchor_checks':checks, 'figure5_edge_ranks_one_based':edge_ranks,
        'scope':'deterministic data validation; no model fit, bootstrap or acceptance verdict',
        'elapsed_seconds':round(time.perf_counter()-started,3),
    }
    (derived/'ingest.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
