# Check of the Gemini 4 Carbon audit

Codex, 2026-11-17. The original external audit is preserved unchanged in the private investigation; [its public copy](AUDIT-2026-11-17.md) is transformed as recorded in EXPORT-TRANSFORMATIONS.json. Original audit (SHA-256 `6f6780c8961ca947cc42876efbce5ad1564270d9e7aafd312428d02d817ec4ed`). This response distinguishes verified findings, applied repairs and claims that need qualification.

The scientific verdict remains **partial numerical reproduction**: f1 accepts 4,724 books and f2 accepts 12,496; five of the 25 frozen primary comparisons fail. No kernel, frozen contract, input, calibration record, corpus record or precision record changed. Gemini supplies an additional review from a different model family, not independent human replication.

## Disposition of implementation findings

| Finding | Disposition |
|---|---|
| Windows separators in saved pass paths; ignored `--A`; missing `--B` | Fixed. New reports store project-relative forward-slash paths; the reader accepts historical separators, resolves saved relative paths from the project root, and uses both explicit overrides for loading and hash checks. |
| Mixed CWD-relative defaults | Fixed in the reader and static figure exporter. Explicit CLI paths remain relative to the caller's CWD. The original README already required running from the project directory, so this was partly interface consistency rather than a failure of that documented workflow. |
| Figure 7(a) final-bin clipping, overlap and inconsistent line | Fixed. Both formats use visible concentric hollow rings at the unchanged coordinates, blue outer f1 and orange inner f2; both omit the connecting line to the 75-book remainder. Static markers are unclipped. |
| Weak null-output assertions | Fixed. Tests now parse the rendered tables and assert the specific mean, SD, relative-change, kappa and ratio cells for zero/one accepted-book cases. Added path-resolution and override regression coverage. |
| Duplicate trial-count guard | Removed the unreachable subset check after the complete record validator. Malformed-record rejection remains tested. |
| Local import in `models.py` | Deferred as optional style cleanup, not a functional defect. No evidence shows incorrect behavior. Changing the hash-pinned numerical kernel solely to hoist an import would invalidate saved execution identity without improving the result. |
| Normalization ZIP member name | Fixed in the receipt: the historical SVG member is explicitly `figure3-7-before-lf.svg`. Original archive bytes and hashes remain intact. |
| Accessibility and download timer | Added decimal `aria-valuetext`, column-header scope, and a 60-second blob revocation delay. The longer delay is conservative cleanup, not a guarantee about every browser's Save-As behavior. |
| Review attribution | Reader, report and README now distinguish the initial fresh-context same-family reviews from Gemini's subsequent different-family review. Earlier signed review records remain historical. |

**Runtime qualification:** the audit missed an earlier gate: `validate_calibration` checks the full recorded Windows `sys.version` string, not just Python's version number. On a different native platform this fails before the old backslash path is reached. Path handling is corrected, but a full saved-run rebuild on Linux/macOS is not claimed. The README now states this exact-runtime limit; execution safeguards were preserved.

## Qualifications to the new forensic arguments

A separate reviewer, independent of production, rederived these points from the saved passes and targets; see [the adjudication](planning/gemini-forensics-review.md).

1. **LR totals:** 2,178 versus 2,176 significant-f1 books, and 20,856 versus 20,857 significant-f2 books, are correct. The +56/-54 f1 row differences largely balance. Near-equal cardinalities do not prove identical membership, identify 56 individual transfers, or exclude all LR implementation differences. Author per-book labels are unavailable. All three cited near-1.96 cases remain nonsignificant under both the exact 0.05 critical value and rounded 1.96; changing those critical values changes zero present labels.
2. **Seed variation:** under independent books and repeated identical procedures, the identity is `E[switches] = 2 Var(total)`. Observed switches/2 estimate one-run variance; their square root is a plug-in SD. Comparing two independently random totals requires estimating the difference SD by `sqrt(switches)`. The A-minus-paper gaps are therefore about **8.7, 4.8 and 5.1** estimated difference-SDs for f1, f2 and both, rather than 12.3, 6.7 and 7.3. These are large diagnostic discrepancies under the stated assumptions, not exact tail probabilities or mathematical proof that seed luck is impossible. The unknown historical procedure remains relevant.
3. **Sampler comparison:** the reported eight direct-sampler comparisons corroborate selected bootstrap exceedance probabilities at finite precision. They do not prove exact equality of the entire bootstrap distribution. This check did not rerun Gemini's 16,000 additional draws; its reported z range is attributed to Gemini. The model-level head/tail identity rests on the mathematical derivation, with empirical tests checking implementation over their covered cases.

None of these qualifications alters the frozen numerical verdict or identifies a historical cause.

## Verification and publication boundary

All 32 unit tests pass. The report, reader, written report and static figures rebuild byte-identically from another working directory. Historical Windows path records still load; explicit relocated A/B directories produce the same reader, and a tampered relocated B completion record is rejected. The scientific JSON object is unchanged after excluding the reporting-code hash and path metadata. All 41 protected input, contract, numerical-source and run-artifact files match the before-fix hashes. [Verification receipt](planning/gemini-correction-checks.json).

The original presentation and reporting bytes are preserved in the private correction snapshot (excluded; hash in EXPORT-TRANSFORMATIONS.json). Older audit hashes and review scopes refer to those earlier versions; the new receipt identifies current outputs. The updated static figure has been inspected visually. Desktop/mobile browser checks passed at 1280/390 px with both rings visible, no document overflow, working controls, decimal slider accessibility values and zero console errors/warnings. The [independent correction review](planning/gemini-corrections-reader-review.md) passed with no blockers; it independently checked path overrides, preserved hash checks and byte-identical rebuilds.

At the time of this correction review, publication had not been authorized. The user subsequently authorized the clean public export. See PUBLICATION.md for the release record and EXCLUDED-FILES.md for export boundaries; publication does not change the scientific verdict.
