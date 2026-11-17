# Scope and order

Selected by Codex under the user's delegation on 2026-11-17. Start with the released-data core; the larger September idea is preserved as historical planning, not an instruction to run every extension now.

1. **Source and contract (T1):** inspect the published equations and tables, derive the discrete models and test assumptions, distinguish known pilot results from new predictions, settle unresolved implementation conventions, and freeze the statistical contract.
2. **Custody and deterministic ingest (T2):** acquire the exact Figshare v3 archive; verify checksum, one positive-integer vector per PG identifier, 31,075 vectors, lengths, and Figure 4 anchors. Preserve all texts, including catalog oddities. Flag deviations.
3. **Calibration (T2):** validate f1/f2 sampling, MLE and discrete KS on simulated data, including heavy tails and numerical boundaries. No corpus-wide bootstrap until the calibration contract passes or a documented amendment resolves a defect.
4. **Reproduction (T2):** 100 refitted draws per text/model, Tables 1-2, f1/f2 threshold curves and length dependence. Store per-text estimates and random-stream identifiers. Compare against the predeclared bands, preserving every mismatch.
5. **Monte Carlo audit (T2):** a genuinely separate 100-draw pass; book-level switches and net totals; higher-precision follow-up with its stopping rule frozen in advance. Unresolved books stay flagged.
6. **Report and review (T1/T2):** self-contained results and a visualizer that redraws at least Figures 3 and 7(a) for the scoped models. Scientific review, deterministic and fresh-context reader gates, then the user's separate publication decision.

The source/custody session and subsequent acquisition are recorded separately. The statistical contract is now frozen in Amendment 1; execution and review evidence are recorded in AUDIT.md and the run artifacts. This scope does not expand automatically when the core finishes.

## Deferred

- Full f3 fit population and the Figure 1 length-tail model.
- Genre/finite-size attribution, SPGC re-tokenization overlap and later-book holdout.
- Statements that the core is novel: the September prior-art survey is historical; refresh it before a novelty claim.
- Any source edits in the paper library or Zipf dossier.

No cross-project code has been copied or adapted. Axtell and Pilgrim-Hills are **high-level precedent only**; no implementation was reused. Record a new method-provenance classification if code is later reused.
