# Repository working rules

Read README.md, REPORT.md, AUDIT.md and PREREGISTRATION.md before changing the scientific work.

- The result is a partial numerical reproduction. Keep all five failed frozen comparisons visible.
- Preserve the exact frozen contract, numerical source and completed run records. Never change seeds, thresholds or data selection to obtain a match.
- New scientific work requires an explicit scope and independent merit review. Use new run directories; do not overwrite completed records or re-ingest over the saved derived manifest.
- Saved-run validation intentionally requires the recorded Windows Python build and dependency versions. Do not silently weaken that guard.
- Run the relevant tests, rebuild presentation changes, and run `python -m src.verify_publication`. Refresh PACKAGE-MANIFEST.json only after reviewing intentional changes.
- Preserve CREDITS.md, LICENSE, REPORT-LICENSE and THIRD_PARTY_NOTICES.md when redistributing.
- Historical review hashes identify the original reviewed bytes. EXPORT-TRANSFORMATIONS.json records public-copy edits; no scientific finding may be silently rewritten in a reviewer's name.
