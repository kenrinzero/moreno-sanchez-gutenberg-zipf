# Gutenberg Zipf model comparison

The power-law survival model f2 is accepted for 12,496 of 31,075 books (40.21%), compared with 4,724 (15.20%) for the power-law mass model f1. The ratio is 2.6452; the published Table 1 implies 2.7221.

**Partial numerical reproduction: some predeclared table-comparison bands fail.** See every exact difference below.

“Accepted” means not rejected by the specified full-support fit test at p>=0.05. It does not prove that the model generates natural language. These are the frozen primary pass-A results, with 100 refitted simulations per book/model. Pass B measures Monte Carlo stability and never substitutes for pass A.

[Open the interactive reader](index.html). [Machine-readable report](results/report.json).

## Published-table comparison

Targets are transcribed from the publisher PDF, Tables 1–2, pp. 12–13. The bands were frozen after exposure to the September pilot results: they are reproduction tolerances, not confidence intervals. The seed already contained earlier numerical results; this is not an unexposed confirmatory study.

| Table / group / column | This run | Paper | Difference | Allowed difference | Band |
|---|---:|---:|---:|---:|---|
| table1 / f1 only / R>0 | 3731 | 3614 | +117 | 180.7 | PASS |
| table1 / f1 only / R<0 | 75 | 81 | -6 | 50 | PASS |
| table1 / f1 only / Total | 3806 | 3695 | +111 | 110.85 | FAIL |
| table1 / f2 only / R>0 | 99 | 120 | -21 | 50 | PASS |
| table1 / f2 only / R<0 | 11479 | 11366 | +113 | 568.3 | PASS |
| table1 / f2 only / Total | 11578 | 11486 | +92 | 344.58 | PASS |
| table1 / Both / R>0 | 448 | 431 | +17 | 50 | PASS |
| table1 / Both / R<0 | 470 | 398 | +72 | 50 | FAIL |
| table1 / Both / Total | 918 | 829 | +89 | 24.87 | FAIL |
| table1 / Total: at least one accepted / R>0 | 4278 | 4165 | +113 | 124.95 | PASS |
| table1 / Total: at least one accepted / R<0 | 12024 | 11845 | +179 | 355.35 | PASS |
| table1 / Total: at least one accepted / Total | 16302 | 16010 | +292 | 480.3 | PASS |
| table2 / f1 only / Significant f1 | 1722 | 1666 | +56 | 83.3 | PASS |
| table2 / f1 only / Significant f2 | 0 | 0 | +0 | 5 | PASS |
| table2 / f2 only / Significant f1 | 0 | 0 | +0 | 5 | PASS |
| table2 / f2 only / Significant f2 | 9567 | 9423 | +144 | 471.15 | PASS |
| table2 / Both / Significant f1 | 0 | 0 | +0 | 5 | PASS |
| table2 / Both / Significant f2 | 4 | 3 | +1 | 50 | PASS |
| table2 / Neither / Significant f1 | 456 | 510 | -54 | 50 | FAIL |
| table2 / Neither / Significant f2 | 11285 | 11431 | -146 | 571.55 | PASS |
| table2 / Total of first three rows / Significant f1 | 1722 | 1666 | +56 | 83.3 | PASS |
| table2 / Total of first three rows / Significant f2 | 9571 | 9426 | +145 | 471.3 | PASS |
| f1 accepted total | 4724 | 4524 | +200 | 135.72 | FAIL |
| f2 accepted total | 12496 | 12315 | +181 | 369.45 | PASS |
| f2/f1 acceptance ratio | 2.645216 | 2.722149 | -0.076933 | 0.1 | PASS |

Table 2’s displayed total covers its first three groups only; its separate neither-model row is excluded from that total. R>0 favors f1, R<0 favors f2; significance is pLR<0.05. A relative preference does not imply an adequate absolute fit.

Every significant opposite-preference case is retained, even if a printed-zero cell remains within its five-book tolerance: **0 cases**.

## Bounded discrepancy investigation

The predeclared strict-cutoff sensitivity p>0.05 yields f1 4,547, f2 11,985, ratio 2.6358. All numerical comparison bands pass under that sensitivity. The printed Figure 7/8/9 captions support the inclusive primary convention, so this is a convention-sensitivity clue, not evidence of what the authors implemented. No threshold or primary classification was changed.

A fresh-context reviewer reread/hash-verified every raw vector and independently refit all 31,075 f1 models with an analytic Euler–Maclaurin zeta derivative. Maximum beta disagreement was 2.023e-12 and KS disagreement 2.543e-13. Another 36 independent 80-digit f1/f2 comparisons at extreme, K4/K5 and anchor cases also agree. No input or observed-fit numerical cause was diagnosed. Primary statistic ties are zero; plus-one p-values leave these grid decisions unchanged.

The authors’ per-book seeds and full implementation were not located in the inspected paper, dataset and author-publication sources. The residual historical cause remains unassigned. This bounded investigation does not prove that author code is unavailable everywhere. [Review and evidence](planning/moreno-review-primary-results.md).

## Monte Carlo stability

| Model | Accepted A | Accepted B | A only | B only | Switches | Relative net change | Kappa |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| f1 | 4724 | 4728 | 263 | 267 | 530 (1.71%) | +0.085% | 0.93387 |
| f2 | 12496 | 12554 | 694 | 752 | 1446 (4.65%) | +0.464% | 0.90330 |

| Model / pass-A status | B accepted | B rejected |
|---|---:|---:|
| f1 / A accepted | 4461 | 263 |
| f1 / A rejected | 267 | 26084 |
| f2 / A accepted | 11802 | 694 |
| f2 / A rejected | 752 | 17827 |

The exposed pilot prediction of 500–2,000 f2 switches is met (1446). The predicted relative accepted-count change within ±4% is f2: met. These predictions are reported diagnostics, not calibration or reproduction gates.

At an ideal conditional bootstrap probability of 0.05, B=100 has Monte Carlo standard error about 0.02179. Two runs can therefore disagree about individual books while their corpus totals remain close. That uncertainty concerns the fitted-null simulation, not natural-language model uncertainty.

## Fixed 10,000-draw precision audit

The prespecified hash ordering selects up to 50 pairs per model in each pass-A K stratum 1–3, 4–5, 6–10 and 11–20. The completed audit contains 400 book/model pairs, with fresh fixed B=10,000 runs and no early stopping or reuse of the selecting trials. The other 61,750 pairs are **not precision audited**. This stratified subset cannot estimate a whole-corpus classification error rate.

| Model | Rejected | Non-rejected | Unresolved |
|---|---:|---:|---:|
| f1 | 74 | 110 | 16 |
| f2 | 70 | 110 | 20 |

Within these selected pairs, 38 interval-resolved determinations disagree with the original pass-A call. f1: 8 A-accepted to rejected, 9 A-rejected to non-rejected; f2: 12 A-accepted to rejected, 9 A-rejected to non-rejected. These are conditional Monte Carlo findings within the selected subset, not whole-corpus errors.

Classification uses pointwise 95% Clopper–Pearson intervals: upper<0.05 rejects, lower>=0.05 does not reject, otherwise unresolved. These intervals quantify conditional Monte Carlo uncertainty; they are not simultaneous guarantees across the selected pairs. Worst-case Monte Carlo SE is 0.005.

| Model | Selecting K range | Candidates | Audited |
|---|---|---:|---:|
| f1 | 1–3 | 1394 | 50 |
| f1 | 4–5 | 413 | 50 |
| f1 | 6–10 | 770 | 50 |
| f1 | 11–20 | 902 | 50 |
| f2 | 1–3 | 3923 | 50 |
| f2 | 4–5 | 1217 | 50 |
| f2 | 6–10 | 2096 | 50 |
| f2 | 11–20 | 2539 | 50 |

The exact selected list and all intervals are in [pairs.jsonl](results/precision-001/pairs.jsonl); the reader offers a CSV download.

## Sensitivities and figures

The machine-readable report contains every centile cutoff from 0.01 to 0.50; all 31,075 books are included. The reader redraws the scoped versions of Figures 3 and 7(a). Length bins sort by (L,PG ID), use 31 full 1,000-book bins and a separately marked 75-book remainder. A toggle removes only that remainder from the length plot.

Strict p>0.05, strict statistic exceedance Dsim>Dobs, sample-variance LR and pooled B=200 results are preserved as sensitivities. Plus-one p=(K+1)/101 changes p-values but keeps the centile-grid classifications identical for cutoffs 0.01–0.50. Off-grid thresholds can differ.

| Model | Accepted beta mean | Population SD | Sample SD | Paper mean / SD |
|---|---:|---:|---:|---|
| f1 | 2.029883 | 0.148874 | 0.148890 | 2.03 / 0.15 |
| f2 | 2.023377 | 0.174043 | 0.174050 | 2.02 / 0.17 |

Figure 9 length quartiles are descriptive reconstructions, sorted by (L,PG ID) among accepted books, with nearly equal groups and extra books assigned first. The seed’s p>0.05 caption claim was corrected from the native source: the published caption uses p>=0.05. Figure 4 instead uses p>1/2 for its illustrative selection.

## Method and calibration

The observation is a word type’s positive token count n; the fitting sample size N is the number of types, not total token length L. Models: f1(n)=n^(-beta)/zeta(beta), f2(n)=n^(1-beta)-(n+1)^(1-beta), with a=1 and 1<beta<=4. There is no fitted lower cutoff or observed-maximum truncation. Each simulated vector has N observations and is refitted before computing the discrete KS statistic at both sides of every support jump.

All 39,600 nested calibration tasks completed: 18 primary cells with 2,000 outer samples, and 18 supplementary cells with 200. Each outer sample has 100 refitted inner draws. Every primary CP screen and all six N=30,000 ensemble recovery intervals pass. An independent fresh-context reviewer recomputed the gates and full cell summaries from all raw records. The primary 0.05 rejection rates range from 4.2% to 5.4%. The screen is bounded calibration error around 5/101, not exact rank uniformity.

Supplementary results remain visible: f2 at N=210,347 and beta=1.5 rejects 18/200 (9%; a wide adjusted interval includes 5/101). Small-N estimator bias can be substantial, so universal ±0.005 bias was not a valid requirement; the frozen recovery screen applies only at N=30,000. Full per-cell counts, beta bias/SD, K histograms and refinement counters are in [the calibration summary](results/calibration-001/summary.json) and the reader.

Independent high-precision formula/optimization checks cover ordinary and extreme supports; the sampler keeps arbitrary integer tails rather than clipping them. Adaptive fitted-KS comparisons use conservative numerical margins and increasing precision, not a formal interval proof for every transcendental operation. The high-precision reference also serves as the rare beta<1.05 fallback, so fast-versus-reference independence does not supply a second implementation of that fallback.

## Data, scope and audit

All 31,075 released vectors are preserved with no filtering: 1,961,738,645 tokens; N ranges from 27 to 210,347. The exact ZIP, per-member hashes, deterministic ingest and all five length anchors are verified. The scoped Figure 4 estimates round to the printed 1.96 and 1.89. Reproducing those rounded estimates does not reproduce the seed-dependent historical maximum-book selection.

This is an independent implementation, reviewed first by fresh-context AI agents of the same model family and then by Gemini 4 Carbon of a different model family. Review independence concerns context, production role and model family, not independent human conceptual replication. The core assumes iid types under its null; it does not show that real word types are independent. No cross-project code was copied or adapted: Axtell and Pilgrim–Hills were high-level precedent only.

Deferred: full f3 reproduction, length-tail fit, genre causation, alternate tokenization, SPGC overlap and holdouts. No novelty or intent claim is made. [Frozen contract](planning/AMENDMENT-1.md), [freeze record](planning/CONTRACT-FREEZE.json), [audit record](AUDIT.md), [Step 0](STEP0.md).

## Primary sources

- Moreno-Sánchez, I., Font-Clos, F. & Corral, Á. (2016). [Large-Scale Analysis of Zipf’s Law in English Texts](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0147073). PLOS ONE 11(1): e0147073. CC BY. Preserved publisher PDF, especially Tables 1–2 and Figures 3–4, 7–9.
- Authors’ [word frequencies from Project Gutenberg English texts, v3](https://figshare.com/articles/dataset/Word_frequencies_from_Project_Gutenberg_English_texts/1515919/3), CC BY 4.0. PG_English_wordfreqs.zip, file 2284750. SHA-256 `6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61`.


## Credits and licensing

Research, implementation and presentation by OpenAI Codex (GPT-6), directed by Kenrin. Cross-family audit by Gemini 4 Carbon (High), with separate Codex scientific and reader reviews. [Full credits](CREDITS.md). Original code: [MIT](LICENSE); original report, figures and result data: [CC BY 4.0](REPORT-LICENSE). [Third-party notices](THIRD_PARTY_NOTICES.md).
