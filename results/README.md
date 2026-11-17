# Completed run inventory

- `calibration-001/`: 39,600 outer tests, B=100 inner refits; 36,000 primary and 3,600 supplementary tasks. All frozen primary calibration/recovery screens pass. Manifest and full JSONL task records are preserved.
- `pass-A/`: primary complete 31,075-book run, B=100 per model, seed prefix 2026111703. Completion hash verifies the exact per-book file.
- `pass-B/`: independent complete 31,075-book run, B=100 per model, seed prefix 2026111704. Its classifications audit stability and never replace A.
- `precision-001/`: 400 selected book/model pairs, B=10,000 fresh draws, prefix 2026111705. All eight strata have 50 pairs; 36 intervals remain unresolved and 61,750 other pairs are not precision audited. Manifests, pair rows and summaries are preserved.
- `report.json`: recomputed primary Tables 1-2, every tolerance/difference, separate strict-cutoff tables, full 2x2 stability counts, precision summary, sensitivities, accepted-exponent moments and figure data. Five primary comparisons fail.
- `figure4-anchors.json`: deterministic observed-data exponent/KS anchors, not bootstrap maximum-selection replication.
- `benchmark-001/`, `benchmark-002/`, `benchmark-003/`: developmental synthetic timing diagnostics. They are not calibration passes or corpus results; the manifested full calibration is the execution gate.

All 31,075 corpus records remain present, including short/atypical books. The precision subset is stratified and cannot estimate whole-corpus classification-error rates. [Complete report](../REPORT.md), [audit record](../AUDIT.md).
