# Step 0 — discrete models, uncertainty and source audit

Authored 2026-11-17, before reproduction code or corpus estimates. This is a derivation and design record, not an independently accepted scientific verdict. Published locators below refer to the preserved 19-page publisher PDF. The September seed already contains numerical pilot results; all future work must disclose that exposure.

Lifecycle note: the derivation and execution design subsequently received fresh-context review; the settled conventions are in [Amendment 1](planning/AMENDMENT-1.md). The open-before-freeze section below records the original design questions. Its general plus-one warning is sharpened by the frozen/report convention: centile-grid decisions at 0.01–0.50 are identical, while off-grid decisions can differ.

## 1. What is sampled

For one book, N is its number of word types and each observation n_i is a type's positive integer token count. Its token length is L = sum_i n_i. The fitting sample size is N, never L. Counts of equal frequencies can compress the likelihood without changing the observation weights. All fits use a=1; no fitted lower cutoff and no upper truncation at the observed maximum.

For beta>1, with t=beta-1:

- f1(n)=n^(-beta)/zeta(beta), S1(n)=zeta(beta,n)/zeta(beta).
- f2(n)=n^(-t)-(n+1)^(-t), S2(n)=n^(-t).

Here S(n)=Pr(X>=n), not Pr(X>n). The f2 mass telescopes: sum from n=1 to M equals 1-(M+1)^(-t), tending to 1. In particular, at beta=2, f2(1)=1/2 whereas f1(1)=6/pi^2, about 0.6079. Their tails can have the same exponent while their hapax probabilities differ substantially. Distinguishing the models on the full support is therefore meaningful.

The stable f2 log mass is -t*log(n) + log(-expm1(-t*log1p(1/n))). Direct subtraction of near-equal powers loses precision at large n. The score of log f2 is -log(n)+q/expm1(t*q), q=log1p(1/n), and its derivative is negative. Thus the total log likelihood is concave on beta>1. The f1 score is -N*zeta'(beta)/zeta(beta)-sum log(n); its second derivative is -N*Var_beta(log X)<0. A bounded solver still needs explicit checks at both ends; concavity does not guarantee an interior optimum on 1<beta<=4.

## 2. Simulation and KS

For U uniform on (0,1], X=floor(U^(-1/t)) has Pr(X>=n)=Pr(U<=n^(-t))=n^(-t), exactly f2. Overflow or integer-range limits cannot be repaired by silently clipping X: that changes the null. Use a supported numeric representation or flag the parameter regime.

To obtain f1 by rejection from f2, accept with probability [f1(n)/f2(n)]/C where C=1/[zeta(beta)*(1-2^(-t))]. The ratio decreases with n because its denominator, apart from zeta(beta), is n*[1-(1+1/n)^(-t)] = t*integral_0^1 (1+s/n)^(-t-1) ds, which increases with n. Hence its maximum is at n=1. At beta=2, C=12/pi^2, about 1.215854. An independent sampler will be useful for calibration.

For discrete KS compare the empirical and fitted distribution on integer support. For each distinct observed u, include the discrepancy at u and u+1 in survival convention; gaps must not be treated as continuous jumps with a discrete model frozen on the wrong side. This covers the extrema on the intervening intervals, where empirical survival is constant and theoretical survival decreases. Every bootstrap replicate has exactly N observations and a newly fitted beta; comparing simulated samples against the original beta would calibrate a different test.

The paper does not release the per-book random seeds. Exact per-book historical classifications are therefore not the reproducibility target. Counts, uncertainty and stability are.

## 3. LR is relative evidence

Let d_i=log f1(n_i; beta1_hat)-log f2(n_i; beta2_hat). Then R=sum d_i, sigma^2=mean[(d_i-mean(d))^2] in the primary convention, and p_LR=erfc(abs(R)/sqrt(2*N*sigma^2)). The paper specifies p_LR<0.05 (p. 10). R>0 favors f1, R<0 favors f2. Record exact ties and zero variance explicitly. A sample-variance denominator is a sensitivity fork because the printed text does not settle the finite-N convention.

Table 2's 'Total LR test' sums only its first three rows. Its separate 'neither' row is not included in that total. The latter is essential evidence that preferring one model does not make it an adequate absolute fit.

## 4. Monte Carlo precision

If K of B independent refitted null statistics exceed the observed KS, K/B has conditional binomial standard error sqrt(p*(1-p)/B). At B=100 and p=0.05 this is about 0.02179. Two independent threshold classifications can disagree without a substantive change in the fitted model.

At the 0.05 cutoff, K/B>=0.05 means K>=5; K/B>0.05 means K>=6. A plus-one estimate (K+1)/(B+1) instead accepts K>=5 at an inclusive 0.05 cutoff too, but alters other thresholds and the reported grid. Preserve K and B, not just rounded p. The paper's 0.01 resolution supports K/100 as the primary reproduction convention; strict comparison and plus-one corrections are named sensitivities, not silent replacements.

For a single p near 0.05, about 1,900 draws gives a plug-in SE of 0.005; 10,000 gives the worst-case binomial bound 0.005 across p in [0,1]. A fixed-SE calculation is not an optional-stopping confidence guarantee. Freeze selection and stopping rules before the high-precision audit; report unresolved classifications instead of forcing them.

## 5. Source-native corrections and deterministic expectations

Tables 1-2 were read in text extraction and directly on rendered publisher pages 12-13; target entries are preserved in paper/targets.json. These are two views by the same producer, not independent double entry.

- Table 1 implies f1 acceptance 4,524/31,075, f2 acceptance 12,315/31,075, intersection 829, union 16,010, and neither 15,065. The f2:f1 ratio is about 2.722; 'around 2.6' is prose, not the exact table target.
- The **published Figure 9 caption (p. 14) uses p>=0.05**. The seed's claim that it uses p>0.05 is incorrect. Figures 7 and 8 also use the inclusive convention. Figure 4's illustrative maximum-length selection uses p>1/2; keep that distinct.
- Figure 5's 15 groups of 2,000 cover 30,000 books, not 31,075. Do not infer a unique remainder/tie convention from the caption; report reconstructed alternatives. This is diagnostic, not a reason to exclude books from Tables 1-2.
- Equation (5) explicitly restricts f3 to 1<beta<2. The broad 1<beta<=4 optimizer description must not be blindly applied to f3. Since the full f3 replication is deferred, this is a recorded boundary, not an executed correction.
- The seed's identification of Figure 4(c) as an index is a source lead awaiting catalog confirmation. Do not assert it as a new verified finding from the PDF alone.

## 6. Standing checklist walk

Number/delta/aggregation: reconcile all cells and margins, distinguish approximate prose from exact tables, and preserve Table 2's unusual total. Seed selection: independent complete pass seeds, not best-of-many selection. Configuration: full support, N vs L, refitting, discrete KS sides, p and variance conventions. Caption mismatch: corrected the seed's Figure 9 inequality. Scope: non-rejection and relative LR are not generative proof; no genre conclusion from this core. Fraud-pattern lenses identify no allegation: model-generated null samples are calibration inputs, not ground-truth language; simulated pilots cannot be presented as corpus results. No intent inference is licensed by a mismatch.

## Open before statistical freeze

Specify calibration distributions and finite-grid p-value checks, numerical tolerances, solver boundary behavior, bootstrap tie counting, per-book RNG derivation, high-precision stopping/selection, and visualizer length-bin remainder handling. Review Step 0 independently. Complete these before a statistical implementation; the deterministic custody and source checks can proceed now.
