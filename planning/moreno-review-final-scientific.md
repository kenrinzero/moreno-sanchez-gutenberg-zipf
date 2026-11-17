# Final independent scientific review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for scientific interpretation as a partial numerical reproduction with a completed Monte Carlo stability audit.** This is not a pass of all reproduction targets. The frozen primary A verdict retains five failed comparisons, and the historical discrepancy remains unexplained. No unresolved numerical or scientific blocker was found after the report correction described below. Publication and browser/accessibility gates remain separate from this scientific review.

## Completed A/B integrity and stability

The independent checker imports no project implementation. It verifies complete 31075-book coverage in each pass, completion/manifest/record hashes, distinct fixed seeds, unchanged calibrated numerical code/runtime/contract/data identities, valid counters and absence of error records. Per-book input N/L/digest, fitted beta/KS and LR outputs are exactly identical across A and B. Thus the paired classification comparison varies the declared Monte Carlo stream rather than the data or deterministic fit.

| Model | Both accept | A only | B only | Both reject | Switches | Accepted A / B |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| f1 | 4461 | 263 | 267 | 26084 | 530 | 4724 / 4728 |
| f2 | 11802 | 694 | 752 | 17827 | 1446 | 12496 / 12554 |

The respective switch fractions are 1.70555% and 4.65326%; kappa values are 0.9338699056 and 0.9033000579. Relative accepted-count changes, using A's accepted count as denominator, are +0.084674% and +0.464149%. All values independently reproduce the report. The exposed f2 predictions of 500–2000 switches and a relative net change within ±4% are met; correctly, they are described as exposed diagnostics, not acceptance gates.

Both observed f1 totals exceed the published 4524. Their small difference from one another shows stability of these two new totals despite 530 changed book classifications. It does not establish the authors' historical implementation, prove a systematic error, or estimate a full distribution of run-to-run totals from only two passes. The final prose appropriately avoids those claims.

## Primary verdict and bounded discrepancy findings

All 25 primary table/total/ratio comparisons match the independent reconstruction. The five failures remain: f1-only total; both-model/R<0 cell; both-model intersection; neither/significant-f1 cell; and total f1 acceptance. The f2 total and f2/f1 ratio pass their frozen bands. There are no significant opposite-preference cases in primary A. Table 2's first-three-row total correctly excludes the neither row.

The strict p>.05 sensitivity passes all numerical comparison bands, while the published captions support the inclusive primary rule. The generated materials consistently preserve this as an unresolved convention-sensitive lead. The all-corpus f1 numerical forensics and 36 high-precision checks support the narrower conclusion that no input or observed-fit numerical cause was diagnosed. They are not presented as proof that every author detail or bootstrap draw is identical. The bounded author-source search is explicitly non-exhaustive, and no unsupported attribution, misconduct, genre or language-causation claim is made.

The report initially omitted the acceptance-total and ratio gate rows from its displayed comparison table, exposing only four of the five failures. This review identified the omission. The generator was corrected, and the regenerated `REPORT.md` now visibly contains **all 25 comparisons and all five FAIL labels**, including 4724 versus 4524, +200, tolerance135.72. No threshold, target or primary classification changed.

## Independent aggregate and presentation checks

The reviewer independently recomputed all 50 cutoff-curve points, both-model intersections, and **3200** length-bin/model/cutoff counts. All books are accounted for in 31 bins of 1000 plus the 75-book remainder, sorted by (L, PG identifier); geometric mean positions and partial-bin flags agree. The final partial bin has its own denominator. The plotted data are pass A, and hiding the remainder affects only the length plot.

Accepted beta means and population/sample SDs agree with independent standard-library calculations. They round to the printed Figure 8 summaries: f1 approximately 2.03/0.15 and f2 approximately 2.02/0.17. Reconstructed Figure 9 quartile counts/endpoints agree, and their descriptive rather than gated status is preserved. The pooled B=200 diagnostic is f1=4682 and f2=12437 and does not replace A. Strict statistic exceedance changes no classifications because primary ties are zero; sample-variance LR changes the significant-f2 both-model cell from 4 to 3, with no claim that this establishes the authors' convention. Plus-one centile-grid equivalence is independently checked.

The actual `index.html` embedded report equals the validated report with only local source-path fields removed; embedded precision pairs and calibration summary equal their completed artifacts. Its displayed report digest is correct. The PNG/SVG manifest pins the report and plot source and matches both exported files. The reviewer inspected the actual PNG: model legends, cutoff and fraction axes, logarithmic length axis, source-table reference diamonds at.05, remainder markers, f1/f2-only scope and partial-reproduction/non-rejection caption agree with the underlying data. This was scientific figure inspection, not a browser interaction audit.

Generated `REPORT.md`, `README.md` and the actual reader's visible text were read for consistency. The main f2-over-f1 result is adjacent to the partial-reproduction and non-rejection qualifiers. Pass A stays primary; B and pooled results remain diagnostics. The pre-exposure of September pilots, interpretation of comparison bands as tolerances, iid-type null limitation, limited review independence and deferred f3/causal/holdout scope are explicit.

## Precision and calibration interpretation

The final report includes the independently verified 400-pair precision audit: f1 has 74 rejected/110 non-rejected/16 unresolved; f2 has 70/110/20. The 38 resolved disagreements with A and 36 unresolved pairs remain limited to the selected subset. The 61750 unaudited pairs, fresh fixed 10000 draws, pointwise CP 95% coverage, lack of simultaneous guarantees and absence of whole-corpus extrapolation are clearly stated. Unresolved status is treated as a completed result rather than unfinished computation.

The complete 39600-case calibration and its primary/recovery passes remain pinned to the original verified artifacts. Supplementary extreme-size diagnostics are visible, including the f2, N=210347, beta=1.5 cell's 18/200 rejection count and broad interval. Calibration is described as a bounded screen under the modeled null, without promoting it to exact composite-null uniformity or independence of natural-language word types. The numerical margin/reference-fallback limitations are retained in the full report.

## Evidence and scope of sign-off

Independent script: `work/moreno_final_scientific_review.py`. Machine-readable verification: `work/moreno-final-scientific-independent.json`. Earlier primary, precision and calibration result memos contain the detailed reconstructions. No project source/control-plane file was edited by this reviewer.

Reviewed completed raw records:

- Pass A SHA-256: `ca86298a6d41da4bb5eaa6ad1c6e2f8a4c085ced1a3a51ed3e25aeb47e5df54b`.
- Pass B SHA-256: `09fe9f9d328f80bf304748fcceb1aa689d38141b644210e37aa8fee250207ba7`.
- Report JSON SHA-256: `86d0c55cc5b780a42fadd2d58252a11dd249b21263acebc5381fbcec72f6af3f`.
- Corrected `REPORT.md` SHA-256: `fa025f8c4e706c5b4fcd5082abd4ce7249e7d9d94c318748bacbbf02705909a1`.
- Final `README.md` SHA-256: `d2cea152946b42ab95bc21bfd14cb71b66197936d60155f4fad3a7b569b0ac29`.
- Final `index.html` SHA-256: `d8abf793d7570c1ceb8341a012f0fa482afeda3d6c4ebd26971f7f7061ca937b`.
- PNG SHA-256: `6a636fde96293890b3337d7840a58f6a3127a2ce448362cbbafcb2bcb36b0169`; SVG SHA-256: `6b43a75c170039a429542b49a46d50ba8651c60b6f1dddaba18a3a13f9aef28b`.

The final reader's stability column now explicitly says **Relative net change**, resolving the requested denominator-label clarification. Its embedded data and hashes were rechecked after that change. The README accurately distinguishes producer-reported localhost browser checks from untested direct-file navigation; this scientific review does not claim to have exercised browser controls.

The supported outcome is: **the released corpus reproduces the broad f2 advantage and approximate exponent summaries, fails five predeclared primary numerical comparisons, and demonstrates substantial book-level Monte Carlo switching despite similar aggregate totals. The historical discrepancy has not been assigned a cause.** This is ready scientifically for delivery as that partial result; the user's publication decision remains separate.
