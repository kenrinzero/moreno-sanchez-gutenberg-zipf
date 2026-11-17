# Independent primary-results audit and bounded forensics

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: execution integrity and primary arithmetic PASS; complete reproduction of the frozen numerical targets FAILS.** The defensible result is a partial reproduction: the f2 advantage, f2 acceptance total and acceptance ratio reproduce within their declared bands, but five primary comparisons do not. No diagnosed numerical or input error explains those failures. A declared cutoff sensitivity is informative but cannot replace the frozen inclusive primary result.

The reviewer independently parsed all 31075 pass-A records, reconstructed the signed tables without importing the project's reporting code, and compared them to a fresh reading of the preserved publisher PDF (printed pp.12–13). Pass-A records SHA-256 is `ca86298a6d41da4bb5eaa6ad1c6e2f8a4c085ced1a3a51ed3e25aeb47e5df54b`. Completion digest, exact metadata/ID coverage, source-member digests, N/L, seed, simulation counters and LR p-value arithmetic agree. Totals are 177927677 types and 1961738645 tokens. Later raw-vector numerical checks independently verified every member digest and its positive counts/N/L. No project source, threshold, seed or control-plane file was changed.

## Primary tables

Table 1, columns R>0 / R<0 / total:

| Group | Run | Paper |
| --- | --- | --- |
| f1 only | 3731 / 75 / 3806 | 3614 / 81 / 3695 |
| f2 only | 99 / 11479 / 11578 | 120 / 11366 / 11486 |
| Both | 448 / 470 / 918 | 431 / 398 / 829 |
| Total | 4278 / 12024 / 16302 | 4165 / 11845 / 16010 |

Table 2, columns significant preference for f1 / f2:

| Group | Run | Paper |
| --- | --- | --- |
| f1 only | 1722 / 0 | 1666 / 0 |
| f2 only | 0 / 9567 | 0 / 9423 |
| Both | 0 / 4 | 0 / 3 |
| First three rows | 1722 / 9571 | 1666 / 9426 |
| Neither | 456 / 11285 | 510 / 11431 |

The run accepts f1 for **4724** books versus 4524 published (+200, +4.42% relative), and f2 for **12496** versus 12315 (+181, +1.47%). The ratio is about **2.6452** versus 2.7221. There are 14773 neither-model books, zero significant contradictions to a sole accepted model, zero exact-zero LR values and zero LR degeneracies.

The five failed comparisons are:

| Comparison | Run minus paper | Frozen allowed absolute difference |
| --- | ---: | ---: |
| f1-only total | +111 | 110.85 |
| Both, R<0 | +72 | 50 |
| Both-model intersection | +89 | 24.87 |
| Neither, significant f1 | -54 | 50 |
| f1 accepted total | +200 | 135.72 |

The first misses by only 0.15 book beyond the real-valued tolerance; the frozen rule still fails it. Rounding its allowed difference upward would change the rule after seeing results. All exact differences and all passing comparisons remain in the independent JSON, rather than reporting only the failures.

## Source and convention forensics

The publisher methods specify 100 Monte Carlo tests, maximum-likelihood fitting on 1<beta<=4 and discrete KS; the Appendix's f2 inversion and f1 rejection match the implemented distributions algebraically. The current head/tail decomposition changes the computational route, not the intended iid null. The Figure 7, 8 and 9 captions support inclusive p>=p0. The source has no released per-book random seeds or paired historical fit/KS outputs in this evidence set, preventing an exact historical classification comparison.

Both models have zero exact and raw floating-point statistic ties across pass A. Strict `D_sim>D_obs` therefore changes no acceptance decisions. The plus-one estimate `(K+1)/101` also leaves all inclusive .05 classifications unchanged. LR variance conventions cannot change the absolute-fit f1 total. The only observed beta=4 book is PG26513, rejected under both models; the constrained-boundary case cannot explain a +200-book total.

There are 177 f1 and 511 f2 records exactly at K=5. The **predeclared strict p>.05 sensitivity** removes these, yielding f1=4547, f2=11985 and intersection=812. Reconstructing all tables with that convention puts every declared numerical table/total/ratio comparison inside its band. In detail, strict Table 1 rows are [3667,68,3735], [83,11090,11173], [395,417,812], total [4145,11575,15720]; strict Table 2 rows are [1677,0], [0,9240], [0,4], first-three total [1677,9244], neither [501,11612].

This is a genuine sensitivity finding, **not evidence that the authors implemented strict comparison** and not authorization to adopt it as primary. In particular, the printed inclusive captions oppose that attribution, and f2's absolute difference from its printed total increases from 181 to 330 under the strict convention even though it stays inside its 3% tolerance. Preserve both facts. A cutoff implementation difference is a plausible unresolved explanation, not an established correction to the paper.

## Independent numerical checks

The post-result diagnostic script `work/moreno_fit_forensics.py` imports no project numerical code. It rereads every original frequency vector and computes the expanded mean of log frequency. It independently solves each f1 score using an **analytic derivative of an Euler–Maclaurin zeta expansion**, unlike the production sixth-order finite-difference derivative. It then evaluates discrete KS directly at exact integer support endpoints. Its score formula is checked against 80-digit mpmath at eight beta values spanning the observed interior range and boundary.

Across **all 31075 f1 fits**, the maximum absolute beta difference is **2.0228263508670352e-12** (PG9454); maximum KS difference is **2.542965837903921e-13** (PG9225). Thus observed f1 fits and KS values agree well inside the frozen tolerances under a separately derived score and endpoint calculation.

A second route uses 80-digit mpmath differentiation/root solving and direct high-precision Hurwitz-zeta/power survival. It covers **36 model/book pairs from 18 books**, selected by N/L/beta/KS extrema, four length-spaced f1 K=4 cases, four K=5 cases, and the Figure 4 anchors (deduplicated). Both models are tested for each selected book. Maximum beta discrepancy is **1.0636647908527297e-12** and maximum KS discrepancy **1.3251631537796594e-13**. It includes the actual constrained boundary. This selected check is not an all-corpus high-precision bootstrap rerun.

Pass A recorded 624 f1 and 86 f2 inverse refinements, one f1 support value above 2^52, and 0/2 f1/f2 KS refinements. These events are retained; no clipping or deletion was found. Previously accepted calibration, direct-sampler tests and kernel review remain relevant. The additional checks strongly constrain an observed-fit numerical explanation; they do not prove that every random variate or every unobserved author implementation detail is identical.

## Interpretation and unresolved cause

The exact archive identity, all-book coverage, source transcription, observed likelihood fits and discrete KS implementation provide no identified defect to repair. The f1 excess cannot honestly be labeled a floating-point failure, a different corpus, a plus-one/tie artifact, or an upper-bound effect on present evidence. Nor can it yet be attributed solely to Monte Carlo randomness: the original seeds and per-book results are unavailable, and one pair of new runs would not recover them.

Pass B remains an independent stability measurement; it must not replace A, even if some counts are closer to the paper. The selected 10000-draw audit concerns conditional bootstrap precision for its declared subset and cannot estimate a whole-corpus correction. Preserve the five primary failures and report the strict-cutoff alignment as a convention-sensitive lead with unresolved attribution. No genre, dependence, misconduct, or causal explanation follows from this discrepancy.

## Evidence

- `work/moreno_primary_review.py` and `work/moreno-primary-independent.json`: independent raw-record arithmetic, all primary gates, full K grids, sensitivities, counts and integrity checks.
- `work/moreno_fit_forensics.py` (SHA-256 `1727a26009074b331c8de9624e2a4646a86946999e732340301f3a4798ee1297`) and `work/moreno-fit-forensics.json` (SHA-256 `052b78e140893ec6247a604211b61abf2455cc81b098687848d3e13dc94b8b9f`): raw-vector all-f1 comparison and 36 high-precision checks.
- `work/moreno-source-review.txt`: fresh layout extraction of preserved `paper/paper.pdf`, whose SHA-256 is `5234b7edbd72dc71989dbcc87d3fb712af5db136ef5203e625920f24148c971d`.

This memo reviews completed pass A only. Actual complete B/precision artifacts and the assembled report/reader receive a separate final interpretation review.

Reporting follow-up: the subsequently added `strict_table_comparison` helper in `src/report.py` (SHA-256 `731f7dc64dae268190ee4dbc278fcfca1e8cd9bb00252e924a394e486ed7ec6d`) exactly matches this independent strict Table 1, Table 2, acceptance counts, ratio 2.6358038266989223 and all-band outcome. The independent verification reran all four report/reader tests successfully. Its separate field preserves the inclusive primary result; aggregate numerical counters correctly sum the recorded fields. Final rendering of these findings remains part of the completed-output review.
