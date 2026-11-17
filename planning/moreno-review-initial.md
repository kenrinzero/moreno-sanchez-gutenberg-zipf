# Independent design review — Moreno-Sanchez Gutenberg Zipf

Reviewer: Codex subagent `Codex scientific reviewer`, fresh context not involved in producing Step 0 or the contract. Date: 2026-11-17. Review only; no member or control-plane file was edited, no corpus fit or simulation was run. The parent will incorporate this review in the session log.

## Disposition

**Step-0 mathematics and source transcription: accepted, with the small precision clarification below. Original DRAFT: not execution-ready. Amendment 1: substantively sound; conditional acceptance pending the six concrete freeze clarifications listed below and a reread of the final text.** This is acceptance of a design, not empirical calibration, a reproduction result, or publication readiness.

Read CHARTER, current week log, project brief/log, container and member AGENTS, STEP0, PREREGISTRATION, SCOPE, provenance, targets, exposed seed and the source PDF. Independently checked PDF text and rendered publisher pages 12–14. Reviewed amendment hash `554d5fb7a8da9f7d497d85b52aaf208c2305a798c80763792623888c2cf1918a`; Step-0 hash `d2602e0ad2d6fe0441a9a0440e832882b8833ea2acf7e2a0cd7ca43f64a62793`; original draft hash `6fee4d5bb40fa40a276fb52430716b17b81bb1e4a4ac52a9e3e1da57cdd69b9a`.

## 1. Independently verified mathematics and primary source

- The f1/f2 masses and survival functions agree with paper equations (3)–(4). Survival means `P(X>=n)`. The likelihood sample size is the number of types N, not token length L. Compression must preserve multiplicity weights.
- The f2 log-mass expression and score in STEP0 are correct. Its second derivative is `-q^2 exp(tq)/expm1(tq)^2`, strictly negative. The f1 log-likelihood second derivative is `-N Var(log X)`. Both are concave; an upper-bound optimum at beta=4 is legitimate under the source constraint. Finite nonempty samples do not have an optimum at beta=1, where the likelihood tends to minus infinity; a numerical lower guard is an exception, not an estimated boundary solution.
- `floor(U^(-1/t))` has the claimed f2 law in exact arithmetic. The rejection envelope for f1 is correct, including the monotonicity proof and `C=12/pi^2` at beta=2. Conditional tail sampling at a=65 is also valid. Its envelope is `C_a=1/[a^beta*zeta(beta,a)*(1-(a/(a+1))^t)]`; the acceptance probability simplifies to `(a/n)*(1-(1+1/a)^(-t))/(1-(1+1/n)^(-t))`.
- Multinomial head frequencies 1–64 plus the analytic residual tail, followed by independent conditional-tail sampling, gives exactly the same unordered iid sample in exact arithmetic. It is a worthwhile speed improvement, provided the tail probability is checked independently and numerical renormalization is explicit.
- The full discrete KS endpoints `u` and `u+1` are correct. Between observed frequencies empirical survival is constant and model survival decreases; its absolute difference is maximized at an endpoint. This includes the unobserved gaps and the final tail. A direct support-grid verifier should include missing integers, repeated frequencies, minimum frequency above 1, and the point beyond the maximum.
- Source Table 1 entries, all Table 2 entries, Figure 8 moments, and Figure 9 legend ranges agree with `targets.json`. The Table 1 margins are f1=4524, f2=12315, both=829, union=16010, neither=15065; ratio=12315/4524. Table 2's total excludes its separate neither row.
- The rendered Figure 9 caption unequivocally uses `p>=0.05`, as do Figures 7 and 8. Figure 4 uses `p>1/2`. The correction to the September seed is correct. Figure 5's 15 groups of 2000 do not account for all 31075 books; the source does not uniquely resolve the remainder convention.
- The LR formula reproduces the paper's asymptotic comparison. Its variance denominator is not specified clearly enough in the source to eliminate the proposed population/sample sensitivity. Neither LR preference nor KS non-rejection demonstrates a word-generating mechanism.

Primary source: Moreno-Sanchez, Font-Clos and Corral, [PLoS ONE article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0147073), preserved publisher PDF, especially pp. 4–6, 8–10, 12–16.

## 2. Finite-grid p-values and composite-null calibration

Conditional on an observed vector and its fitted beta, repeated bootstrap exceedance indicators are iid Bernoulli with parameter `q=P(D_sim>=D_observed | beta_hat,N)`. Thus K is binomial and binomial Monte Carlo intervals concern q. They do not cover corpus sampling error, model misspecification, dependence between real word frequencies, or the bootstrap's approximation error.

If the observed statistic and 100 null statistics were exchangeable and tie-free, K would be uniform on 0,...,100. Under that ideal reference, the inclusive `K/100>=0.05` convention rejects with probability 5/101; the strict convention rejects with probability 6/101. At thresholds .01,.20,.50 the corresponding inclusive ideal rejection fractions are 1/101,20/101,50/101. With ties, `>=` is conservative in the exchangeable setting. With a fitted composite null, exchangeability is not exact, even after refitting. A continuous-uniform KS test is therefore unsuitable; a discrete-uniform reference is a benchmark, not an exact validity theorem.

Amendment 1 correctly makes this distinction and uses an empirical calibration-error screen. Its 18 simultaneous 99% Clopper-Pearson intervals inside `[5/101-.03,5/101+.03]` are a defensible, explicitly coarse screen. Passing allows roughly 2–8% null rejection at the .05 rule; the report must retain that practical meaning. Failure can reflect real approximation/conservatism rather than a coding error. Other threshold results remain necessary diagnostics.

Minor STEP0 precision clarification: for every tested threshold `p0=j/100` with `1<=j<=50`, inclusive K/100 and inclusive `(K+1)/101` yield the **same classification** (`K>=j`). Plus-one changes reported p-values, and can change other cutoffs, but cannot explain differences along this particular .01–.50 threshold grid. Also, 1900 is only an approximate draw count: the exact fixed-SE condition at q=.05 is B>=1900, while worst-case SE<=.005 requires B>=10000.

Supporting primary references: [Genest and Remillard (2008)](https://www.numdam.org/article/AIHPB_2008__44_6_1096_0.pdf) establishes asymptotic parametric-bootstrap validity under regularity, not universal finite-sample exactness. [Phipson and Smyth (2010; author manuscript)](https://arxiv.org/abs/1603.05766) concerns exact discrete Monte Carlo/permutation p-values; its plus-one rationale should not be misrepresented as making this composite-null bootstrap exact.

## 3. Recovery, numerical tails and computational cost

The seed's unqualified beta recovery within .005 was not a valid correctness criterion. For f1, the leading unconstrained MLE bias is `kappa3(log X)/(2*N*Var(log X)^2)`. Independent 50-digit zeta differentiation gives the following leading biases at N=300: .00219953 at beta=1.6, .00415466 at beta=2, and .01243823 at beta=3. These are analytic asymptotic calculations, not simulated observations. Correct estimation can therefore fail the proposed .005 small-N criterion. Beta=4 introduces constrained-boundary bias as well.

Amendment 1's independent numerical optimizer comparison, bias/MC-SE reporting at all N, and .005 ensemble equivalence screen only at N=30000 are sensible. Declare whether its six recovery intervals are pointwise 99% or simultaneous; a Bonferroni 99%/6 specification is simple and affordable. Use an explicit beta bracket-width stopping condition and define any score tolerance as a per-observation score, avoiding an undocumented N-dependent criterion.

Heavy-tail overflow is a real regime, not merely a pathological API case. For f2, tail probability above approximately 2^53 is about 1.05e-8 at beta=1.5, 2.67e-10 at beta=1.6, and 1.11e-16 at beta=2. Billions of draws make the first two relevant. Silent int64 casts, clipping and redraws change the null. Float exponentiation can also misfloor a value close to an integer below 2^52. A high-precision/arbitrary-integer fallback is preferable to merely counting large float values. Refine ambiguous inverse values adaptively; a fixed 80 digits is insufficient to floor all very large values, although 80 digits is an appropriate minimum for many oracle comparisons. Stop visibly if the numerical representation cannot support the draw.

Large-integer log-mass and survival evaluation should have explicit error tolerances and independently checked asymptotic remainder bounds. Near equality of observed and bootstrap KS values needs refinement if numerical errors could change the exceedance sign: small KS errors alone do not guarantee the same K. Preserve strict and inclusive counts and exact numerical ties.

Full nested calibration at three betas, three N values, two models, 2000 outer replicates and 100 inner replicates represents 40,359,600,000 type observations before head/tail compression, and 3,636,000 fits including outer fits. At beta=2 alone it is 13,453,200,000 observations. The two full corpus passes imply 71,171,070,800 type observations using the parent's ingest total of 177,927,677 types. These are workload calculations, not benchmarks. Head/tail compression and synthetic timing should precede execution; cost is substantial but not inherently prohibitive. Do not silently reduce cells after examining calibration results.

The parent corrected an early N-range message: minimum N is 27, whereas N=84 belongs to the minimum-L book. That claim was supplied by the parent, not independently re-ingested in this review. Small-N and maximum-N diagnostic settings, plus all-one/upper-bound cases, should accompany the principal calibration range.

## 4. Reproduction bands and Monte Carlo audit

The inherited bands are compatibility tolerances rather than inferential intervals. Amendment 1 correctly grades pass A as primary and does not let pass B replace an unfavorable result. Keep the exact differences visible. The tolerance for a printed cell of 3 is 50, so passing that band is weak evidence about the rare event. Similarly, even one significant LR preference opposite the sole KS-accepted model contradicts the paper's categorical statement that this never happens; list and investigate every such book even if the zero-cell tolerance of five passes.

Two independent B=100 passes with fixed named streams are a valid stability audit. Report switch directions, net counts, agreement and kappa together; high overall agreement can conceal differences in the smaller accepted group. The exposed +/-4% prediction needs the chosen relative-count interpretation, as the amendment now supplies. It is not a new confirmatory prediction.

The proposed precision follow-up is a defensible **scope reduction**: up to 200 selected books per model, four declared pass-A strata, fresh fixed B=10000 trials, all other books explicitly below the precision target. Conditional on selection, fresh independent trials permit ordinary fixed-binomial intervals for each selected q. Reusing the selection trials or stopping early according to the estimate would require another inference argument. The 10000-draw maximum SE bound does not ensure the .05 classification is resolved. Describe the selected strata; the subset is not a representative sample of all books and must not be used unweighted to infer whole-corpus precision or acceptance changes.

## 5. Six required freeze clarifications

1. Specify the precision audit interval confidence and decision rule. Recommended: pointwise 95% two-sided Clopper-Pearson; reject if upper<.05, non-reject if lower>=.05, otherwise unresolved. Explicitly disclaim a simultaneous guarantee across all selected books.
2. Define Figure 4's exponent check for f1/f2 panels (a)/(b) only. Panel (c) is f3 and deferred.
3. Give an explicit RNG tuple schema with disjoint role IDs for outer data generation and inner null simulation. Inner replicate 0 must not reuse its outer sample stream. Prefix/model/N/beta/outer/inner indexing must have an unambiguous mapping.
4. Add near-integer inverse refinement below the large-value fallback threshold, adaptive precision sufficient to determine the integer, and tests at U=1 and near inverse boundaries. No outcome-dependent redraws.
5. Declare quantitative numerical oracle tolerances for log mass, survival/KS and inverse rounding; resolve numerical comparisons capable of changing K. State the score-tolerance normalization and recovery-interval multiplicity convention.
6. Add N=27,84,210347 diagnostic coverage with explicit status, and require reporting of every contradictory Table 2 case regardless of aggregate tolerance.

After these clarifications, I see no remaining mathematical-design blocker to freezing the contract and implementing calibration. Execution, actual numerical error certification, calibration passage, and scientific interpretation still require their own evidence.
