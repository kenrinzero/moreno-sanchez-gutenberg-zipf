# Independent precision-audit runner review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for the frozen precision subset audit after validated pass A is complete.** This approves the reviewed selection, execution and interval logic, not unseen precision results.

Reviewed `src/precision.py`, SHA-256 `6eff9e843f5a1589ab5e5e8adb306743eb5013c25d393f54919fcb4a04c44a12`, and `tests/test_precision.py`, SHA-256 `22fbbee42cfb56a9b143b743be7e89baee3a6a97001505ebcf7eaa2a57780ac7`.

Selection matches Amendment 1: independently for each model, pass-A K_ge strata 1–3, 4–5, 6–10 and 11–20; at most 50 per stratum; SHA-256 ordering of UTF-8 `2026111705:model:PGid`; no refilling. Model/PG pairs are unique, while one PG book may legitimately be selected under both models. All eight strata, including empty ones, are reported in the final summary.

Each selected pair receives a fresh PCG64 stream `[2026111705,model,PG_id]` and exactly 10000 refitted trials. No selecting trials are reused and no outcome-dependent stopping is present. The same book is reloaded from the archive, checked against its digest/N/L, and its deterministic beta/KS must equal pass A. Pointwise 95% Clopper-Pearson intervals are recomputed from K_ge/B. Status is rejected when the upper endpoint is below .05, non-rejected when the lower endpoint is at least .05, and unresolved otherwise. The worst-case conditional Monte Carlo standard error is correctly .005.

The supplied calibration must pass the full re-derived gate, and selecting pass A must match its contract, environment and calibration-artifact hashes. Numerical code, archive, CSV and ingest identities are checked. The precision manifest pins selection, source-pass records/manifest/completion, calibration artifacts, source data and numerical implementation.

Checkpoint handling rejects orphan, duplicate, unknown and mismatched pairs. Exact integer model/PG identity, selection fields, source/statistic identity, counters, interval endpoints and reported status are validated on resume and before append. Worker and record-validation failures are preserved and stop execution. The final persisted records are reread and validated against the entire expected pair set; summary status/stratum totals derive from those reread records. Unselected book/model pairs remain explicitly outside the high-precision audit.

The initial provenance gaps identified in review were corrected: selecting-pass alignment with the supplied calibration, whole-archive/metadata pinning, source manifest/completion hashes, strict pair identities, explicit empty-stratum coverage and persisted-derived summaries are all present.

## Verification

The reviewer independently ran the two precision tests: **2/2 passed**, exit code 0. They exercise 400 unique selections, iteration-order invariance, empty selection, interval/status boundaries and corruption of identities/counts/intervals. A separate reconstruction using literal seed text and raw SHA-256 digest ordering matched **400/400 synthetic selected pairs**.

The completed calibration was independently accepted in `moreno-review-calibration-results.md`; this runner review did not inspect or infer any real precision-audit outcomes. Selection depends only on the specified pass-A counts and deterministic hash ordering, and must remain unchanged after pass-A results become available.

## Interpretation limits

Intervals concern each selected book/model's conditional bootstrap tail probability. They do not provide simultaneous coverage of the selected set, whole-corpus high-precision estimates, uncertainty about the natural-language generating process, or an unbiased sample of all books. A .005 SE bound does not force a threshold decision: unresolved intervals must remain unresolved. These limits are correctly preserved by the runner's output language and the frozen contract.
