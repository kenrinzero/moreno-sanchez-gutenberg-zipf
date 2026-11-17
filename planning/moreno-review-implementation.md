# Independent numerical implementation review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17. Continuing the explicitly authorized fresh-context review of frozen Amendment 1, hash `840c71fab0c0d62da6bf8b974bf79d3ef8de9479fe3cf071adfcc6b7ff15ef86`.

**Verdict: PASS to execute the predeclared full synthetic calibration. No unresolved implementation blocker in the reviewed kernels and runner.** This does not establish that the calibration passes, that the real corpus reproduces, or that the publication gate is satisfied.

## Scope and checked versions

Read and reviewed `src/models.py`, `src/reference.py`, `src/bootstrap.py`, `src/calibrate.py`, `tests/test_models.py`, and `tests/test_calibration.py`. The parent made corrections during this review; the reviewer made no source or control-plane edits. Initial findings were communicated before full calibration, and the current source was reread after the corrections.

Reviewed file SHA-256 values:

| File | SHA-256 |
| --- | --- |
| src/models.py | 987d60f41678d3330a62c3ca3bf6a7f42f2e601d4103b822a6e91c31e3a92b37 |
| src/reference.py | 0981ad21d3f94c951f4b6d26ef70574b8f8a5de01830285f6cebd3e1b526839e |
| src/bootstrap.py | 873f06c65ab9cc40fc78089bcf469a94c43cc47dbbc7b63b0ad062fddffc554e |
| src/calibrate.py | 510889a5db872f57b7f8d654f07dc8bae8a8841acc1b41a71332d242e00b5a7c |
| tests/test_models.py | 5fcec230ab079cefd45285ce49eac573f1b82d232ea8d9312fff9fbbed3f3bd3 |
| tests/test_calibration.py | 9ada36bc4673ab5859ffe4404025e6eb1ef1cfcfda6bd11fef7b875d8bc1c431 |

## Correctness assessment

The head/tail decomposition uses the correct analytic probabilities and conditional distribution. The f1 rejection probability simplifies correctly at the tail cutoff, and its large-n expansion has negligible omitted terms at the chosen cutoff. The f2 score and its small-argument series are correct. The revised sixth-order f1 zeta derivative reduces the cancellation seen in the initial implementation. KS checks both sides of every empirical jump with integer-support survival, including gaps and the final tail.

Inverse sampling retains the exact binary input U and beta, uses rational/integer-root arithmetic for the small rational exponents and interval arithmetic for other exceptional inverse values, and refines near-integer fast-path values. It retains large values as Python integers and does not redraw an inconvenient result. The large-support log-mass and survival approximations were checked against independent direct high-precision formulas through support 10^500.

The ordinary likelihood/KS reference uses a different high-precision root-solving path from the fast kernels, with a precision-dependent bisection budget. Integer n+1 is formed before conversion to high precision. Adaptive KS comparison now includes parameter bracket width, requires sign separation at successive precision levels, and permits structural ties only under an equal-parameter argument plus matching, separated maximizing witnesses. The f2 beta=4 case uses exact rational KS arithmetic. Exhausting the precision cap raises an exception instead of forcing a tie. Raw binary64 equalities and refined ties are stored separately.

The bootstrap guard `4e-9/(min(beta,fitted)-1)+4e-12` is conservative relative to the tested 1e-9 parameter-error target. For f2, the survival derivative is bounded by `1/[e*(beta-1)]`; for f1 a usable bound is `E(log X)<=1/(beta-1)`. These bounds explain the dependence on beta. Root convergence of a finite-difference score alone would not establish the actual parameter error; the added oracle comparisons supply empirical numerical evidence.

## Findings resolved during review

1. Constructors originally truncated fractional support and multiplicities, accepted malformed shapes, and could overflow the total count. They now require exact one-dimensional positive integers, reject booleans, and check the sum before conversion to int64.
2. The initial KS refinement used fixed 80-digit arithmetic and 180 bisections, then interpreted numerical equality as an exact tie. The adaptive, bracket-aware comparison and structural tie checks replace that behavior.
3. The original sampling test lacked the contract's separate direct sampler, and the expanded-likelihood test recompressed the sample before comparison. Tests now compare a direct sampler and an independent raw-observation likelihood sum.
4. Zero/negative bootstrap B values originally returned empty results. Invalid B is now rejected.
5. Calibration completeness originally depended mainly on the row count. It now checks the exact expected key set, identities, per-cell counts and exceedance-count consistency. Benchmark mode cannot satisfy the full gate.
6. The runner now reports beta SD, all 101 K bins, raw/refined ties, and numerical refinement counts. Failed workers preserve task identity, exception and traceback before aborting; they cannot be silently omitted from a passing calibration.
7. An independent extreme-support probe found a final-KS tolerance miss: f1 on the one-observation histogram `{10^500: 1}` had beta error approximately 1.65e-13 but KS error approximately 6.99e-11 because of sensitivity near beta=1. The new beta<1.05 fallback refits at high precision and explicitly checks the final KS tolerance, raising if binary64 cannot meet it. This case is now a regression.

## Verification evidence

The reviewer ran separate numerical probes recorded in `work/moreno_kernel_review_probe.json`. Before the near-one repair, nine of ten model/histogram comparisons met the final-KS tolerance; ordinary cases had maximum beta error about 1.39e-13 and maximum KS error about 7.37e-14. The tenth exposed the issue above. The repaired adaptive f2 comparison correctly distinguished histograms with supports `[1,10^100]` and `[1,10^100+1]`, despite their binary64 indistinguishability.

The parent reported 18 passing tests: 15 kernel tests and three calibration-record tests. The reviewer launched a separate full-suite rerun; its completion result is recorded in the addendum below. Tests cover source identities and normalization, extreme support, full-grid KS, independent fitting, boundary optima, inverse rounding, sampler agreement, meaningful uncompressed likelihood, LR degeneracy, exact/near ties, invalid inputs and calibration completeness. The tests are necessary correctness evidence, not a substitute for the 39,600-task empirical calibration.

The runner's binomial interval and recovery formulas match the frozen contract: 18 primary cells, 2000 outer samples each; 18 supplementary cells, 200 samples each; B=100; inclusive rejection K<5; simultaneous 99% primary Clopper-Pearson screen; six-comparison recovery interval at N=30000. Outer and inner RNG roles are disjoint, benchmark streams are separate, and process workers isolate the high-precision contexts. Checkpoint manifests pin code, contract, environment and run mode.

## Limits to retain in the report

- Adaptive KS comparison uses conservative numerical margins and oracle checks. It is not a rigorous interval proof covering every transcendental library operation. The interval-based inverse-floor branch has a stronger local arithmetic guarantee than the entire fitted-KS computation.
- The high-precision reference also serves as the rare beta<1.05 production fallback. Fast-versus-reference independence applies to the ordinary fast branch; the fallback's regression is an end-to-end precision check, not a second independent implementation of that same reference solver.
- Synthetic calibration is still pending at this review. It tests the declared grid and approximation bounds; it does not establish iid behavior of real word frequencies.
- No real-corpus fitting was performed by this reviewer. Data identity and the reported runtime benchmark were not independently re-ingested or rerun as part of this numerical review.

The remaining work is execution and interpretation of the frozen calibration, followed by the separately gated corpus runs. No thresholds, seeds or calibration cells should change in response to the forthcoming results.

## Independent test completion

The reviewer's separate `python -m unittest discover -s tests -v` run completed successfully: **18/18 tests passed in 23.464 seconds**, exit code 0. This includes the near-one precision regression and the close-KS comparison regression. The implementation PASS above is final for the reviewed versions.
