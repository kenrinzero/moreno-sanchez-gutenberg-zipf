# Review and audit record

The result is a **partial numerical reproduction**, with five failed primary comparisons retained. See [REPORT.md](REPORT.md) for the scientific findings. This page summarizes the review chain and the limits of its independence.

## Scientific and reader reviews

The original implementation was produced by OpenAI Codex. Separate, fresh-context Codex reviewers checked the [design](planning/moreno-review-amendment-1.md), [implementation](planning/moreno-review-implementation.md), [completed calibration](planning/moreno-review-calibration-results.md), [corpus results](planning/moreno-review-primary-results.md), [precision audit](planning/moreno-review-precision-results.md), and [final scientific record](planning/moreno-review-final-scientific.md). A separate [reader review](planning/moreno-reader-review.md) checked presentation and source-native headline claims. These reviews are independent in context and production role, within one model family.

**Gemini 4 Carbon (High)** subsequently performed an independent different-family audit. [Its original scientific/code audit, public copy](AUDIT-2026-11-17.md) reports source inspection, clean-room fits and sampler comparisons, raw-record arithmetic and rebuild checks. Its principal verdict supports the scoped partial reproduction. [The adjudicated response](AUDIT-RESPONSE-2026-11-17.md) records applied repairs and corrects overstatements about individual-book transfers, Monte Carlo seed impossibility and exact sampler-distribution proof.

[Independent forensic adjudication](planning/gemini-forensics-review.md) and [independent correction review](planning/gemini-corrections-reader-review.md) accepted those qualifications and the corrected presentation. All 32 unit tests passed; path overrides, provenance rejection, deterministic rebuilds and desktop/mobile behavior were checked. An [independent release review](planning/moreno-publication-review.md) passed the clean export, including a corrected cold-clone receipt dependency. The package also includes the DejaVu font notices for SVG glyph outlines. No review is independent human conceptual replication.

## Preserved limits

- Five of 25 predeclared numerical comparison bands fail. Strict-cutoff sensitivity passing all bands does not identify the authors' historical procedure.
- Same-procedure Monte Carlo scale estimates make a seed-only explanation strained under their assumptions, not logically impossible. Near-equal LR totals do not identify individual transfers. Historical causation remains unresolved.
- The 400 selected precision pairs do not estimate a whole-corpus error rate; 36 remain unresolved, and 61,750 other pairs lack that precision audit.
- Adaptive high-precision KS comparisons use conservative margins and numerical checks, not formal interval proofs for every transcendental operation. The high-precision reference also serves as the rare near-one production fallback.
- Calibration was a fresh run. The frozen calibration runner's unmanifested-resume edge case remains a documented limitation; do not adopt orphan records. Corpus and precision runners reject them.
- Saved-run validation requires the exact recorded Windows Python build and dependency versions. The standalone HTML does not require Python or network assets.

## Public-copy provenance

The private investigation preserves all original review bytes and pre-correction presentation snapshots. This clean export omits those archives and workstation scratch scripts. It retains the frozen contract, calibrated numerical source and complete run records unchanged. [EXPORT-TRANSFORMATIONS.json](EXPORT-TRANSFORMATIONS.json) records source/public hashes for transformed prose and exclusions; historical hash references identify the original files. [PACKAGE-MANIFEST.json](PACKAGE-MANIFEST.json) identifies current public files. Public export is packaging, not a new simulation or replacement for the earlier reviews.
