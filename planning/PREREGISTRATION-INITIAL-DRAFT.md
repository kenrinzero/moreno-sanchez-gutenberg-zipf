# Statistical contract — DRAFT, NOT FROZEN

Created 2026-11-17. No corpus fit or simulation has run in this member. The seed discloses prior 400-book and 1,500-book prospecting; neither this document nor its later freeze makes this an unexposed confirmatory replication.

## Proposed fixed inputs and estimands

- Published PLoS ONE article, DOI 10.1371/journal.pone.0147073.
- Figshare 1515919 v3, file 2284750, `PG_English_wordfreqs.zip`, 26,349,768 bytes, MD5 `e269dc5e82b0038aae9f9e297dcdb286`. Acquire and manifest SHA-256 before use.
- Keep exactly the released positive-integer PG vectors; discard archive metadata entries only. Do not retokenize, filter books by current language labels, or replace the corpus.
- f1 and f2 on the full integer support with a=1 and bounded 1<beta<=4 MLE. N is the type count, L the sum of frequencies. Record every boundary/numerical exception.
- Primary goodness-of-fit: 100 refitted simulations, p=K/100 and acceptance p>=0.05. Resolve statistic ties explicitly at freeze. Secondary: p>0.05 and plus-one p, with exact K retained.
- Primary LR: population variance of per-type log ratios, strict p_LR<0.05. Report sample-variance sensitivity and sign/variance degeneracies.

## Proposed comparisons inherited from exposed prospecting

- Exact custody/structure/count/length checks: **Type A**. Expected 31,075 vectors and L>100; min L=115 (PG29156, seed lead), max L=4,659,068 (PG29765, seed ID lead). Source Figure 4 lengths: 83,720, 239,018 and 2,081; corresponding PG IDs from the seed require data/catalog checks.
- Table 1 margins: within 3% of printed targets; interior cells within max(5%, 50 books), using absolute difference. Table 2 nonzero cells: same max(5%, 50 books) band; printed zero cells: at most 5. These are tolerance bands, not confidence intervals. Emit every cell and exact difference regardless of pass/fail. **Type A arithmetic; Type B interpretation.**
- f2:f1 ratio at 0.05: within 0.1 of the exact table-derived 12,315/4,524. Also report the entire p0=0.01,...,0.50 curve. No unpublished tolerance is to be retrofitted to make a curve pass.
- Figure 8 means/SDs, Figure 9 accepted-length quantiles and maxima: descriptive diagnostics unless an explicit pre-run amendment defines gates.
- Second independent 100-draw pass: report model-wise 2x2 status tables, agreement/kappa, net fraction changes and thresholds. The seed's 500-2,000 f2 switches and net +/-4% are prior predictions; define whether the latter is relative or percentage-point change before freezing, not after seeing data.

## Calibration design to settle

The seed asks for 2,000 null p-values per model at N in {300, 3,000, 30,000}, calibration at 0.01 and beta recovery within 0.005. It omits true-beta settings and the meaning of 'recovered'. A single raw uniformity test against continuous U(0,1) is inappropriate for a finite 101-point MC grid and an estimated-parameter bootstrap. Freeze a simulation design with discrete/rank-aware reference, declared familywise handling or explicit descriptive status, ensemble bias rather than each replicate's error, and numerical tail checks. Keep original and amended requirements visible.

## Still required before freezing

1. Independent Step-0/design review and precise calibration contract.
2. Random stream naming and two run seeds; tested numerical tolerances and overflow behavior without tuning real-data acceptance.
3. High-precision audit: fixed effort versus a valid sequential interval; selection rule; retained unresolved flags and interval convention.
4. Figure 7(a) 1,000-book bins, sort/tie order and remainder handling; default full-data final partial bin with a sensitivity to dropping it is a proposal, not yet frozen.
5. Freeze date, immutable document hash and an amendment policy; all later substantive changes must precede their affected runs and explain what data had been seen.

No scientific gate is currently marked passed. Publication is outside this setup session.
