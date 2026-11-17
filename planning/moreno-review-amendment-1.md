# Amendment 1 final design review

Reviewer: Codex subagent `Codex scientific reviewer`, independent fresh context. Date: 2026-11-17.

**Verdict: PASS for statistical-contract freeze and implementation of calibration. Zero remaining design blockers.** This does not certify an implementation, empirical calibration, corpus reproduction, scientific conclusion or publication.

Reviewed the entire final `planning/AMENDMENT-1-DRAFT.md`, SHA-256:

`840c71fab0c0d62da6bf8b974bf79d3ef8de9479fe3cf071adfcc6b7ff15ef86`

This follows `moreno-review-initial.md`. The original draft's unresolved points have now been replaced by explicit choices, and all six freeze clarifications from the initial review are present:

- Precision follow-up has fresh fixed 10000-draw streams, pointwise 95% Clopper-Pearson intervals, declared reject/non-reject/unresolved rules, no simultaneous guarantee, and an explicit maximum of 200 selected books per model. Remaining books are flagged below the precision target. This is transparently a narrower audit than the exposed seed contemplated.
- Figure 4 exponent checks cover only scoped f1/f2 panels; f3 receives an input-length check only.
- RNG tuple schemas separate outer and inner generation with disjoint roles, and separate calibration, numerical tests, passes A/B and precision follow-up with fixed prefixes. Tasks own their streams, independent of worker scheduling.
- Inverse sampling includes near-integer and large-support high-precision fallback, adaptive floor determination and arbitrary integers. No clipping, redraw or silent retry is allowed. Mean-frequency validation is explicitly prohibited where the model's first moment is infinite.
- Numerical tolerances specify log-mass error, survival/KS error, beta root/bracket error and cross-optimizer agreement. Score stopping cannot bypass parameter error without a curvature argument. Near KS comparisons include fitted-beta uncertainty and require higher-precision refitting rather than a widened tie tolerance. Large-N recovery intervals use the declared six-comparison adjustment.
- N=27,84,210347 diagnostic cases and boundary/all-one cases are included. Every contradictory Table 2 significance case is reported even if the numerical zero-cell tolerance passes.

The principal calibration screen is scientifically coherent as a bounded error check: 2000 outer replicates in each of 18 cells, B=100 refitted inner trials, simultaneous 99% binomial intervals, and an allowed absolute rejection-rate discrepancy of .03 around the ideal 5/101 reference. This is deliberately a coarse screen; it must not later be described as exact uniformity or universal bootstrap validity. Supplementary sample sizes remain diagnostics, not silently additional calibrated claims.

The sampling head/tail decomposition is exact in real arithmetic; implementation still has to establish numerical accuracy, inverse-floor handling, correct tail weighting and independent direct-sampler agreement. Its efficiency should be measured before launching calibration. Primary calibration represents 40,359,600,000 type observations before compression; supplementary diagnostics add 25,507,509,600, for 65,867,109,600 total equivalent observations. These are workload arithmetic, not runtime estimates.

Source verification remains as recorded in the initial memo: masses, MLE derivatives, rejection envelope and discrete KS endpoints are correct; Tables 1–2, Figure 8 moments and Figure 9 ranges/caption match the preserved publisher source. The plus-one transformation leaves inclusive classifications unchanged on all requested thresholds j/100, j=1,...,50; retain it as a reported p-value sensitivity rather than predicting classification changes on that grid.

Freeze may preserve the reviewed body unchanged and record this hash/acceptance in separate metadata. Any substantive body change requires its own version and review appropriate to the change. The current approval is strictly for this design, with future numerical and empirical gates still outstanding.

No member or control-plane files were edited by this reviewer. Review artifacts are under the chat workspace `work/`; the parent owns clock-out and incorporation of evidence into the project record.
