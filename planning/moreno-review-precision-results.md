# Independent completed precision-audit review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS for the completed, predeclared selected-pair precision audit.** Selection, coverage, provenance, intervals, statuses and summary arithmetic agree with independently reconstructed expectations. This does not change the primary reproduction verdict or supply a whole-corpus high-precision correction.

## Artifact custody and execution

| Artifact in `results/precision-001` | SHA-256 |
| --- | --- |
| `manifest.json` | `8c3d42d2de46ce022ab563b0bd32f81a507cdb03e7e81c42841b2d70d2e39042` |
| `pairs.jsonl` | `6afc0672d9c43033d556db647e60d0e0e2cb5319bf564a2d99f0dd39df52cf58` |
| `summary.json` | `4c9152b5397d0015b09a1b5aaefe77c60eb9be9e887eb748fd131a0cff1cbc00` |

The reviewer checked actual hashes of the selecting pass A, its manifest/completion, complete calibration artifacts, frozen contract, archive, CSV, ingest and current numerical/precision-runner code. Runtime versions agree with calibration and pass A. All records retain seed 2026111705, B=10000, the unchanged deterministic fitted beta/KS and correct raw member identity/N/L. Every selected raw frequency vector was independently reread, hashed and counted. No error record was present. The existing reviewed runner implements fresh independent `[2026111705, model, PG_id]` streams and fixed 10000 draws; its code hash is unchanged. This review did not rerun the four million bootstrap replicates.

## Selection and coverage

Independent literal UTF-8 SHA-256 ordering of `2026111705:model:PGid`, using only completed pass-A K_ge, reproduces all **400 selected pairs** in the manifested order. There are 200 pairs per model and **399 distinct books**; one book's selection under both models is legitimate. There are no missing, duplicate or additional model/book pairs.

| Model | Selecting K range | Candidates | Selected |
| --- | --- | ---: | ---: |
| f1 | 1–3 | 1394 | 50 |
| f1 | 4–5 | 413 | 50 |
| f1 | 6–10 | 770 | 50 |
| f1 | 11–20 | 902 | 50 |
| f2 | 1–3 | 3923 | 50 |
| f2 | 4–5 | 1217 | 50 |
| f2 | 6–10 | 2096 | 50 |
| f2 | 11–20 | 2539 | 50 |

All eight strata have their fixed 50 selected pairs. **61750 book/model pairs have not received this precision audit.** The candidate counts and selected counts exactly match the persisted summary.

## Interval and status verification

The independent checker imports no project implementation. For every record it separately solves the binomial-tail equations `Pr_p(X>=K)=.025` for the lower endpoint and `Pr_p(X<=K)=.025` for the upper endpoint, with the standard K=0/n boundary definitions. This is an independent inversion route from the production beta-quantile formula. Across all **800 endpoints**, maximum absolute disagreement is **1.2490009027033011e-15**; maximum tail-probability residual at the saved endpoints is **1.366962099069724e-14**.

Statuses independently recompute as rejected if the upper endpoint is below .05, non-rejected if the lower endpoint is at least .05, and unresolved otherwise:

| Model | Rejected | Non-rejected | Unresolved |
| --- | ---: | ---: | ---: |
| f1 | 74 | 110 | 16 |
| f2 | 70 | 110 | 20 |
| Total | 144 | 220 | 36 |

All trial/tie/refinement identities agree. The audit records zero statistic ties, zero raw floating-point ties and zero support values above 2^52. It records two f1 and three f2 inverse refinements, and two f2 KS refinements. Those events remain visible rather than being dropped.

## What the selected results support

Within this deliberately selected subset, **38 resolved interval determinations oppose pass A's 100-draw threshold classification**: f1 has 8 previously accepted pairs now rejected and 9 previously rejected pairs now non-rejected; f2 has 12 and 9 respectively. Another **36 pairs remain unresolved** after 10000 fresh draws. The full per-stratum breakdown is in the independent JSON. These counts illustrate classification sensitivity around the cutoff; they are not estimates of the number of wrong decisions across the corpus.

The intervals are pointwise 95% statements about each pair's conditional bootstrap exceedance probability under its fitted null. Fresh draws keep the interval calculation separate from selection, but pointwise coverage is not a simultaneous guarantee for 400 intervals. A non-rejected label does not prove a language model true, and a resolved change from A does not establish a natural-language error. The worst-case Monte Carlo SE bound is .005; that bound does not force every interval away from .05. Retaining the 36 unresolved statuses is the correct completed outcome.

Selection excludes K=0 and K>20 and uses equal allocations across unequal candidate strata; do not present 38/400, 36/400 or the 144/220 totals as population rates. No reweighting or corpus-total correction was frozen or established. Pass A and its five failed comparisons remain primary, while pass B supplies the separate full-corpus stability audit when complete.

## Evidence and remaining review

Independent script: `work/moreno_precision_results_review.py`. Detailed result: `work/moreno-precision-results-independent.json`. Both were written outside the project; no member/control-plane file was edited. Completed B and the assembled report/reader remain for the later scientific presentation review.

Reporting follow-up: the new `precision_comparisons` helper was executed against the actual 400 records and exactly matches the independent 8/9 f1 and 12/9 f2 directional counts (38 total). Reviewed `src/build_reader.py` SHA-256: `fdcc6c810b5a88a1f8662ee300edc447ce079d5605b4fe85efb97e5c4a708e04`. The report's new field uses this helper; the loader rejects a differing saved field. Adjacent renderer wording explicitly limits these disagreements and unresolved pairs to the selected subset. No blocker in this reporting addition.
