# Independent report-code review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for the reviewed aggregation code.** This is a code/arithmetic review using synthetic fixtures; no incomplete calibration result or real corpus outcome was adjudicated.

Reviewed `src/report.py`, SHA-256 `899376275840a916d3597e286c51757ed5c502dfcb83475a2a54e98028e73276`, and `tests/test_report.py`, SHA-256 `56f4c1b6b2540a2fbdf2f1b0d5ebbf5e9420ccf26d84495b4c144bf8941029c1`.

The primary Table 1 signed cells, row/column margins, accepted-model totals and ratio use pass A and the frozen tolerances. Table 2 uses strict p_LR<.05, separates the neither row, and excludes it from the displayed first-three-row total. Every significant LR preference opposite the sole KS-accepted model is listed individually even if the aggregate zero-cell band passes. Exact-zero LR and degenerate LR cases remain visible.

Two-pass status tables, switch directions, agreement, kappa and relative accepted-count change are computed from aligned PG identifiers. Deterministic N/L/source hashes, fitted beta/KS and LR results must agree across passes. Pass B and pooled B=200 do not replace the primary pass-A gates.

The implementation now distinguishes strict p-threshold sensitivity, strict bootstrap-statistic/tie sensitivity using K_gt, and sample-variance LR sensitivity. The plus-one invariance check uses integer arithmetic and correctly verifies unchanged inclusive classifications on p0=.01,...,.50. The acceptance curve and length-bin calculations follow the frozen threshold grid and 1000-book grouping, with the final partial bin flagged separately.

Figure 9 diagnostics use accepted books sorted by (L, PG_id), split into four near-equal count groups with extra books assigned first. The output identifies this as a reconstructed grouping, rather than an established author convention. Empty acceptance sets yield unavailable values; singleton sets have unavailable sample SD. A zero f1 denominator fails the ratio gate with an explanation instead of crashing or emitting NaN.

Loading requires the expected pass/seed, completion identity and count, matching result-file hash, exactly 31075 unique validated books and the original metadata hash. A/B provenance and calibrated module hashes must agree. The report retains pass-source hashes and now pins its own code and target-transcription hashes. Strict JSON serialization rejects accidental non-finite output.

## Independent verification

The reviewer independently ran the three report unit tests: **3/3 passed**, exit code 0. Those tests cover signed cells, neither exclusion, strict threshold, sample-variance sensitivity, A/B switches, empty acceptance and deterministic drift.

A separate reviewer-authored nine-book fixture checked all six signed Table 1 cells, an exact-zero LR case, Table 2 significant cells, neither exclusion, two contradictory books, strict p threshold and directed switches. Expected Table 1 rows were `[1,1,2]`, `[1,1,2]`, `[1,1,3]`, total `[3,3,7]`; expected Table 2 first-three total was `[2,3]` with a separate neither row `[1,1]`. All assertions passed. The zero-acceptance result serialized as strict JSON. Script and output are `work/moreno_report_review_probe.py` and `work/moreno_report_review_probe.json`.

After those tests, the final provenance-only additions (report/target hashes and strict JSON output) were read directly; the aggregation logic was unchanged.

## Limits

Passing the numerical bands does not establish exact reproduction, and a listed contradictory book remains scientifically meaningful even when a zero-cell tolerance passes. Interpretation and presentation must preserve that distinction. The high-precision audit status is currently explicitly pending and must be updated when that separate audit is incorporated. This review covers aggregation code, not actual corpus values, the completed visualizer, or publication.
