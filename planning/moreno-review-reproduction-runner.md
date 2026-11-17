# Independent reproduction-runner review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for the reviewed runner, conditional on its full-calibration gate actually passing. No unresolved runner blocker.** Calibration was still in progress during this review. No calibration outcomes were adjudicated and no corpus bootstrap was executed by the reviewer.

Reviewed versions:

- `src/reproduce.py`: SHA-256 `815a14e97e489a44f7524d7f6ea191431e5a5d3ec84aca251c3e80f2ebaf0b6f`.
- `tests/test_reproduction_records.py`: SHA-256 `2822c69db3dfe4954a7715adc52d45ebcdf7e77ea1060a7e8b4168f3ca854ea8`.

The four calibrated modules (`models.py`, `reference.py`, `bootstrap.py`, `calibrate.py`) retained the hashes recorded in the implementation review. This runner review did not require modifying those modules.

## Seed separation and coverage

Pass A uses prefix 2026111703 and pass B uses 2026111704. Every book/model constructs its own PCG64 generator from `[pass_seed, model_id, PG_id]`. This separates models and passes and makes task scheduling/worker count irrelevant to their random streams. The pass seed is stored in every book record and checked on resume; copying a record from the other pass is rejected.

Both models run with B=100 for every input book. The input requires exactly 31075 rows and 31075 distinct PG identifiers. Workers verify each archive member's SHA-256, N and L before fitting. Before writing completion, the runner rereads the persisted checkpoint and requires exactly the expected 31075 unique books, validating every record again. Completion therefore certifies the saved artifact rather than merely an in-memory counter.

## Calibration and runtime gate

The runner requires the frozen full configuration: PCG64, B=100, the declared three primary and three diagnostic sample sizes, the three true betas, and the 2000/200 outer counts. It rejects incomplete or failed calibration and any nonempty calibration error record.

It reads all calibration task records and re-derives the full summary with the frozen summarizer, which enforces the exact 39600-task key set, task identities, count consistency and per-cell coverage. It compares that result to the stored summary. A summary claiming success cannot substitute for the task records.

The four calibrated module hashes, contract hash and Python/NumPy/SciPy/mpmath versions must still match. The pass manifest pins hashes of the calibration manifest, complete task file and summary. This is materially stronger than trusting summary flags alone.

## Custody and checkpoint safety

The runner checks the full ZIP against the known SHA-256, checks that ingest names the same archive, and checks the book-metadata CSV against ingest. It pins the ingest JSON and CSV hashes as well as the archive hash. Per-member checks in workers independently protect the actual vectors consumed.

An existing checkpoint without its manifest is rejected. An existing manifest must byte-match the requested pass identity and current dependencies. Resumed records must have the expected PG identifier, N, L, source digest and pass seed, valid B/exceedance/tie/refinement counters, finite fitted beta and KS values, and internally consistent LR fields. The LR p-values are re-derived from the saved R, variance and N. Duplicate and unknown checkpoint books are rejected.

Fresh worker results receive the same record validation before append. Worker failures preserve PG identity, exception and traceback and stop execution. Record-validation failures are also recorded and abort the run. Partial/truncated JSON is rejected rather than silently salvaged; any such recovery remains an explicit repair, not a hidden retry. Completion records a hash of the entire saved book-results file.

## Findings corrected during review

The initial runner accepted calibration summary flags without re-deriving the result, validated resumed records mainly by PG identifier, and could adopt an orphan checkpoint under a newly written manifest. Those were blockers because they could turn missing/mismatched work into apparent coverage or mix pass identities. All are resolved in the reviewed version.

Additional corrections make full-mode configuration explicit, check ingest's archive identity, retain per-record pass seeds, revalidate the final persisted artifact, check LR numerical consistency and tie/refinement invariants, and record validation failures. These changes affect execution/provenance handling only; the calibrated numerical kernels remain unchanged.

## Verification and limits

The reviewer independently ran `python -m unittest discover -s tests -p test_reproduction_records.py -v`: **5/5 tests passed**, exit code 0. They cover wrong-pass/source identity, malformed counts and fits, orphan checkpoints, a plausible success summary without task records, and inconsistent LR p-values. Static review additionally checked the seed tuples, full configuration, final reread and error propagation.

This PASS permits use of the runner after its calibration gate succeeds. It is not a claim that calibration has passed or that 31075 books have been processed. Downstream reporting must verify completion's results-file hash and pass identity before presenting a completed pass. Numerical adequacy and the scientific interpretation remain under the frozen contract and the earlier implementation review's stated limits.

The reviewer made no source/control-plane edits; findings were implemented by the parent. This memo is the review artifact for the parent's session record.
