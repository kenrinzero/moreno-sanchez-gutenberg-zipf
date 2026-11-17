# Independent public-release packaging review

Date: 2026-11-17. Reviewer: Codex reader/release reviewer, separate from the export producer.

**Verdict: PASS for the reviewed clean export. No release-packaging blockers remain.** The user has already authorized publication. This review adds no approval gate and does not certify a deployed commit or live Pages response; those are the parent's remaining publication-verification steps.

## Scope and independence

Reviewed the clean repository at `the public repository` against the original investigation. I previously reviewed the reader and presentation corrections but did not create this export, licensing text, source importer, or transformation receipts. This is separate-context/production-role review within Codex's model family, not an additional cross-family or human scientific replication. I did not rerun a broad scientific audit or alter repository files.

## Reader, credits, and licensing

- The default reader, README and report retain the partial numerical reproduction: f1 4,724, f2 12,496, 2.65 times as many f2 acceptances, and five failed frozen comparisons. Non-rejection, prior pilot exposure, the 400-pair subset limit, unresolved historical cause and strict-cutoff nonreplacement qualification remain clear.
- The reader's visible footer names OpenAI Codex (GPT-6), Gemini 4 Carbon (High), and Kenrin with distinct roles. README/CREDITS distinguish implementation, initial same-family reviews, later cross-family audit, and subsequent Codex correction checks. They avoid presenting any of these as independent human conceptual replication or as Gemini's endorsement of unreviewed later wording.
- Paper and dataset authors Isabel Moreno-Sanchez, Francesc Font-Clos and Alvaro Corral receive separate, linked attribution. The public figures are identified as recomputations, not copied author plots; the dataset is identified as the authors' exact release rather than a newly scraped corpus.
- LICENSE supplies the MIT text for original software. REPORT-LICENSE identifies CC BY 4.0 for original prose, figures/design and project-generated results, limits the grant to what the project can license, and separates embedded JavaScript/software. THIRD_PARTY_NOTICES preserves source/dependency terms and attribution. The included Figshare metadata identifies the source dataset as CC BY 4.0. This is a packaging-consistency check, not a legal opinion about protectability or enforceability.
- Current reader/README/report/audit-summary surfaces contain no stale claim that publication is unauthorized or that the completed result is still pending. The historical Gemini audit is prominently labeled a pre-correction public copy and linked to the adjudication. PUBLICATION.md correctly awaits actual deployment identity rather than inventing a completed release.

## Reproducibility and export integrity

- README explicitly retains the exact recorded Windows Python build/package guard. It does not imply that normalized paths establish a Linux/macOS saved-run rebuild. It distinguishes standalone HTML viewing and standard-library package checks from the scientific runtime.
- Raw ZIP/PDF are excluded from Git and described as on-demand inputs. The source downloader/importer checks exact length and SHA-256, preserves a mismatched existing destination, and does not re-ingest or rewrite the derived manifest. The documented manual import route handles hosts that decline automated requests. Both focused source-import tests passed independently.
- The standard-library publication verifier passed on the reviewed export: 114 manifested files, 14 unique reader IDs, correct embedded report and partial verdict. The staged set is exactly those 114 files plus PACKAGE-MANIFEST.json; no raw ZIP/PDF, scratch work, or private review-script directory is staged.
- Independently verified all **102 included original hashes**, all **27 original/public transformation pairs**, and all **15 excluded-artifact hashes and byte counts** against the original investigation. Every included file differing from its recorded original has a transformation entry; every exclusion is outside the public manifest. Whole replacements of README/AUDIT/AGENTS are correctly classified as transformations.
- Examined the audit/reviewer/seed diffs: changes generalize routing labels and workstation references, add historical-copy context, or replace public-facing packaging prose. No reviewed scientific verdict was silently changed in an auditor's name. Scientific kernels, frozen contract, derived manifests and completed calibration/corpus/precision records match their original bytes.
- Independently checked 75 local Markdown/HTML link targets for existence, containment in the export, and staging: no missing or escaping targets. A scan of staged text found no workstation paths, private-key headers, or the tested credential-shaped strings. Parent-reported Second Reader and cold full rebuild checks provide additional coverage; I do not claim the pattern scan proves absence of every possible secret.

## Issue found and resolved during this review

A receipt refresh briefly moved the locally present but Git-ignored ZIP/PDF into `transformations`, incorrectly calling them replaced public documents. Because the verifier hashes every transformation, this would fail in a clean clone without the source inputs. I reported the issue before publication. The producer restored both files to `excluded_source_artifacts` and removed them from included-source/transform entries.

I independently rechecked the corrected receipts and ran the verifier in `work/moreno-public-cold-final/`: the raw ZIP and PDF are absent, its receipt/manifest are byte-identical to the reviewed export, and verification passes for all 114 files. The blocker is resolved. The parent separately reports that the cold tracked-file export rebuilds JSON, HTML, REPORT, PNG and SVG byte-identically and passes the original 32 plus two new importer tests; this memo's own execution covered the package verifier and two focused importer tests.

## Reviewed package identity

SHA-256 values before deployment-record updates:

- `index.html`: `dcc2c240527dbae732b1112891b693f9f6cb049d95402c3c2549d2af6a42aee5`
- `README.md`: `3c4e43fed06b956a8fa47a35d774dc3fde0008d542830f68061e162b49d41e8f`
- `CREDITS.md`: `284918d9c3147c5c43905b8f241a267b9fbe026634314448a2a6d8a0d6391718`
- `EXPORT-TRANSFORMATIONS.json`: `920bc5ccfb0f8202ced929d8cbb3b8a9f4fa45854756cb31f362955ec5fd1f92`
- `PACKAGE-MANIFEST.json`: `d9569fc9260e3e22c8bc3fe66efcee60ffdc8c78608794d1862beb05a759b620`

Final commit/Pages verification and corresponding intentional publication-record/manifest refresh remain ordinary authorized release steps. No source, export, or control-plane file was changed by this reviewer.

