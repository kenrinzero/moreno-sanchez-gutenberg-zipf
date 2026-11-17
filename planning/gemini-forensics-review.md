# Adjudication of Gemini's new forensic inferences

Reviewer: Codex `Codex scientific reviewer`. Date: 2026-11-17. Read-only review of the specified claims in `AUDIT-2026-11-17.md`, reviewed SHA-256 `6f6780c8961ca947cc42876efbce5ad1564270d9e7aafd312428d02d817ec4ed`. Original audit, project source and frozen results were not edited.

**Verdict: the quoted counts and variance identity check out; the individual-transfer, seed-impossibility and exact-sampler-proof conclusions require qualification. The path fix also does not establish POSIX rebuild support.** These corrections do not overturn the existing partial-reproduction verdict.

## 1. LR totals: verified aggregate agreement, unidentified individual changes

Audit line 29 correctly removes KS grouping by summing all four mutually exclusive Table 2 rows. Independently from the saved A records and published targets:

| Significant preference | Published | Recomputed | Difference |
| --- | ---: | ---: | ---: |
| f1 | 2176 | 2178 | +2 |
| f2 | 20857 | 20856 | -1 |

The significant-f1 changes are +56 in f1-only and -54 in neither, summing to +2. This is near agreement of **cardinalities**, not proof that the same individual books have the same LR classifications. Different memberships can cancel in aggregate. Author per-book LR/KS records are unavailable here, so there is no identified list of 56 transferred books and no basis to exclude all LR implementation differences.

The three quoted near-boundary cases are verified: PG26747 z=1.9597813194, PG1605 z=1.9596527881, PG12270 z=-1.9595155473. All are nonsignificant under both the exact two-sided .05 cutoff 1.9599639845 and rounded 1.96. Substituting 1.96 changes **zero** present-corpus LR labels. Their proximity alone does not explain the published count differences. The accepted maximum lengths and identities also check: PG43016, L=241358 for f1; PG5140, L=348992 for f2. Those matching endpoints do not establish all-book membership parity.

**Defensible wording:** “Pooling all KS groups gives almost identical aggregate significant-LR totals. The f1-only increase and neither decrease largely balance, which is consistent with a substantial KS-partition contribution. Individual transfers and the absence of LR implementation differences cannot be established without the authors' per-book results.”

## 2. Switch identity: unbiased variance estimate, not exact observed SD or impossibility proof

Audit line 30's identity is correct under independent books and two independent runs with the same per-book acceptance probabilities. Let T_A=sum(A_i), S=sum(1[A_i!=B_i]), and pi_i=Pr(A_i=1)=Pr(B_i=1). Then

`E[S] = 2 sum pi_i(1-pi_i) = 2 Var(T_A)`.

Thus **S/2 is unbiased for the one-run variance** under those assumptions. Its square root is a plug-in SD estimate, not the exact SD or an unbiased SD estimator. For the “both” category, use the per-book indicator that both models accept; no independence between models is needed for this identity, although independence between books and between runs still is.

An independently generated historical total H would itself fluctuate. Under the same-procedure hypothesis, `Var(T_A-H)=2 Var(T_A)`, so comparing A against H calls for estimated SD **sqrt(S)**, not sqrt(S/2):

| Outcome | A / B / paper | Observed S | Estimated one-run SD | Estimated A-minus-paper SD | Difference / latter SD |
| --- | --- | ---: | ---: | ---: | ---: |
| f1 | 4724 / 4728 / 4524 | 530 | 16.279 | 23.022 | 8.687 |
| f2 | 12496 / 12554 / 12315 | 1446 | 26.889 | 38.026 | 4.760 |
| Both | 918 / 907 / 829 | 301 | 12.268 | 17.349 | 5.130 |

All counts were independently recomputed. The audit's 12.3/6.7/7.3 multiples divide by the estimated variability of only one run and therefore overstate the standardized comparison of two random totals. If instead comparing H with the average of A and B, the appropriate variance is 1.5 Var(T_A), estimated by 3S/4; that is a different diagnostic and must be named.

The corrected discrepancies remain large relative to the estimated same-procedure Monte Carlo scale. But these plug-in multiples are **not exact tail probabilities or a formal test**: variance is estimated, the unknown author procedure and cross-book random-stream dependence matter, and no finite Bernoulli-tail argument makes these observed differences logically impossible. “Mathematically confirms ... cannot explain” and “rules out pure seed luck” are unjustified.

**Defensible wording:** “The observed switch counts estimate one-run Monte Carlo SDs of about 16.3, 26.9 and 12.3 books under the same-procedure independent-stream model. Accounting for variability in both totals, the published differences are about 8.7, 4.8 and 5.1 estimated difference-SDs. This makes seed-only variation a strained explanation under those assumptions, but does not rule it out mathematically or identify the historical cause.”

## 3. Direct sampler: useful empirical corroboration, not exact-distribution proof

Audit line 24 reports eight independent direct-sampler estimates, each with 2000 refitted draws, compared with 10000-draw head/tail estimates; reported z scores range from -0.920 to +1.168. This review assesses that inference, not a new execution of those 16000 draws. The audit does not provide the eight raw count pairs in that paragraph, so the reported z range is not independently reconstructed here.

Failure to detect a difference does not establish equality, especially without a prespecified equivalence margin. The comparison checks estimated bootstrap exceedance probabilities at eight selected observed statistics, not the entire bootstrap-statistic distribution or all parameter/tail regimes. At probability .05, the two-estimate standard error for 2000 versus 10000 independent trials is about .00534; a normal 95% difference interval has roughly a one-percentage-point half-width. Finite comparisons cannot prove exact sampling equality. The algebraic derivation of the head/tail decomposition supplies the model-level equality; numerical checks and these simulations corroborate its implementation within their tested coverage.

**Defensible wording:** “Eight selected literal-Appendix bootstrap tail estimates were statistically compatible with the stored head/tail estimates at the available Monte Carlo precision. This is useful independent empirical corroboration, alongside the mathematical derivation and numerical tests; it is not proof of exact distributional equality.”

## 4. Portability: backslashes are a real issue, but not the whole gate

Audit line 172 overstates what path normalization alone resolves. `src/build_reader.py:151` calls `reproduce.validate_calibration` before loading report paths. In `src/reproduce.py:79–81`, that validator compares the entire current runtime dictionary, including **full `sys.version`**, against the saved manifest. The saved Python string includes `[MSC v.1944 64 bit (AMD64)]`; a native Linux/macOS/WSL Python build has a different string even at the same Python version. It will fail with `Calibrated runtime changed` before reaching `Path(source['path'])`.

**Defensible wording/resolution:** Path serialization and path resolution need correction for portability, but that alone does not make the saved Windows-calibrated rebuild portable. Preserve frozen execution safeguards. Either document the manifested-runtime restriction; introduce an explicitly separate portable artifact-verification/rendering mode that does not claim the current runtime was calibrated; or rerun calibration and dependent simulations in new directories on the target platform. Do not silently weaken the numerical execution gate or claim tested POSIX support from a backslash-only repair.

Evidence read: saved A SHA-256 `ca86298a6d41da4bb5eaa6ad1c6e2f8a4c085ced1a3a51ed3e25aeb47e5df54b`, B SHA-256 `09fe9f9d328f80bf304748fcceb1aa689d38141b644210e37aa8fee250207ba7`, source-native `paper/targets.json`, calibration manifest and current validator/reader code. No new thresholds, simulations, primary classifications or attribution claims were introduced.
