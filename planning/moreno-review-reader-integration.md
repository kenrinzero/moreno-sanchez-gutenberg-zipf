# Independent reader and report integration review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for the reviewed data integration and presentation logic.** No unresolved blocker remains in this review. This is not a scientific verdict on incomplete corpus runs or a browser/accessibility sign-off on the eventual rendered artifact. Final results, generated `REPORT.md`, and the completed reader remain subject to the separate result review.

Reviewed source SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `src/build_reader.py` | `4199df0361b32deac7596b2be8361f46eb004b252cfefb97f02fd6ff6d5facf5` |
| `src/report.py` | `8b51d34f5bdd49a0d875702b1aab4f42418005a75ffad9c659435a08793f1ec6` |
| `src/reader.html` | `0e5c6dec6298975fd78db56dfd52212ef212c620c4cc2285cb7d2d4ea9fefb44` |
| `tests/test_reader.py` | `e15deeff805e17cca68f934bc83f506aca907c68f93245c3b950da908d7f2082` |

## Artifact integration

The builder revalidates the complete calibration from its raw records and binds both complete corpus passes to its contract, runtime, numerical implementation and artifact digests. It rederives report arithmetic from the validated per-book records. The precision loader checks the fixed seed, 10000 draws, pointwise 95% interval convention, numerical/runner hashes, source-pass record/manifest/completion identities and shared calibration/data provenance. It independently regenerates the declared selection, requires exact selected-pair coverage, validates persisted pairs, and recomputes model/status and all eight stratum totals. An optional precision summary or manifest digest included by `report.py --precision` must equal the artifacts actually being rendered.

The builder also checks the ingest digest, 31075 vectors, exact token total 1961738645, five successful length anchors, and exactly the two declared Figure 4 pairs: PG27027/model1 and PG9365/model2. The exponent anchors must equal the corresponding pass-A deterministic fits and round to the printed exponents. Embedded report paths are removed for portability; displayed aggregates and precision pairs are embedded without rendering-time network requests. Strict JSON serialization rejects non-finite values; legitimate unavailable estimates render as unavailable.

## Presentation and diagnostic coverage

Primary pass A, independent pass B and the fresh bounded precision audit remain distinct. The reader preserves the interpretation of acceptance as non-rejection, the conditional Monte Carlo meaning of precision intervals, pointwise rather than simultaneous coverage, and the absence of a whole-corpus precision guarantee. Neither-model books remain in the corpus, and the Table 2 total excludes that separate row. Individual significant contradictions are displayed even if a numerical zero-cell tolerance passes.

The template exposes comparison bands, signed tables, accepted exponent moments with both SD conventions, reconstructed length quartiles, switches/net changes/kappa, all eight precision strata, strict p-cutoff and statistic-tie sensitivities, sample-variance LR sensitivity, pooled-200 diagnostics and degenerate/zero LR counts. All 36 calibration cells are visible, including the 18 supplementary extreme-size diagnostics; the primary and recovery screens are identified and are not promoted to universal calibration guarantees. The source-exposed 500–2000 f2-switch and ±4% f2 net-change predictions are separately labeled historical predictions, not acceptance gates. The latter is correctly restricted to f2; f1's net change is descriptive.

The final 75-book length bin is identified, has its own denominator and can be hidden without changing the all-corpus curve. The figures are identified as recomputations rather than digitized author points. The page states the exposed-pilot status, model/seed constraints, author-selection limitation of the two Figure 4 anchors, same-family AI review limitation, and excluded causal/f3/holdout claims. These descriptions are consistent with the frozen scope. The interpretation of any actual mismatch is reserved until complete results exist.

## Verification and corrections

The reviewer independently ran the reader and report tests: **4/4 passed**, exit code 0. They cover null-safe rendering, deterministic pass drift, unavailable acceptance ratios and signed table/neither-row arithmetic. A separate synthetic-only loader probe accepted a coherent fixture and rejected six corruptions: seed, draw count, confidence level, numerical hash, report-summary mismatch and missing selected pair. Evidence is saved in `work/moreno_reader_loader_review_probe.py` and `work/moreno-reader-loader-independent.json`. These checks did not read partial corpus-fit outcomes.

Issues found and corrected during this review were missing precision-design/provenance alignment; unbound calibration identities; report/precision inconsistency; nullable-number formatting; absolute embedded paths; hidden calibration diagnostics and exposed predictions; unlabeled sensitivity output; invalid paragraph/table nesting; unchecked hardcoded anchors; the overbroad f1 historical-prediction label; and vacuous acceptance of an incomplete exponent-anchor list. No project source or control-plane file was edited by this reviewer.

Remaining verification is output-specific: inspect the completed A/B/precision artifacts and generated report, confirm all actual findings and limitations are carried into the reader, and check the final page and controls at desktop/mobile sizes. This integration PASS does not imply those later checks have already occurred.
