# Independent completed-calibration review

Reviewer: Codex subagent `Codex scientific reviewer`. Date: 2026-11-17.

**Verdict: PASS under the frozen calibration contract.** The completed raw records independently satisfy all 18 primary calibration screens and all six large-N recovery screens. This permits the gated corpus reproduction; it does not establish a corpus result.

The reviewer parsed all 39600 records from `results/calibration-001/tasks.jsonl` and independently reconstructed the expected task-key set, per-cell sample sizes, rejection counts, binomial intervals, fitted-beta means/MC errors, recovery intervals and all 101 K bins. The implementation's summarizer was not called by this audit. Every recomputed count and interval agreed with the saved summary. Records had valid trial/count identities and finite beta/KS values; no nonempty numerical-error file was present. The four numerical/calibration module hashes and frozen contract hash matched the run manifest.

Artifact hashes checked:

- Tasks: `c1e88753e418592bfecb64cf6498579b2195f2dcf9ee7e10fa70a873a1b32b79`.
- Manifest: `e611d7b02d9225c1b0866a2622476efc8a8750108194070cb203878a6bff8d11`.
- Summary: `2646f7eac1f6b6dce542f09784e3a0d241ed0e581a6384919465d4b185d3d624`.

The 18 primary cells each contain 2000 outer samples. Their rejection rates at the inclusive .05 rule range from 4.2% to 5.4%. Every simultaneous 99% Clopper-Pearson interval lies inside the frozen `[5/101-.03,5/101+.03]` screen. All six simultaneous large-N bias intervals are comfortably inside [-.005,.005]; across them the most negative endpoint is about -.0013193 and the most positive is about .0009210.

Supplementary cells each contain 200 outer samples and retain their descriptive status. In particular, f2 at N=210347 and beta=1.5 has 18/200 rejections (9%); its wide adjusted interval is approximately [.0351,.1796] and includes 5/101. This observation does not fail a primary gate and does not establish calibration at that extreme N. Small-N bias is also visible: for example, f1 at N=27 and beta=3 has mean error about +.1934. This supports retaining the distinction between numerical correctness and finite-sample estimator bias. It does not, by itself, adjudicate the paper's separate beta-versus-token-length or genre explanation.

The run records 894 KS comparison refinements, 33971 inverse refinements and 279 large-integer draws, counting both outer and inner samples where recorded. The rare numerical paths therefore mattered in actual calibration. Their presence is not a numerical failure; unresolved numerical errors would have stopped the gate.

Review script: `work/moreno_calibration_review.py`. Full independently reconstructed results: `work/moreno-calibration-independent.json`. The script completed with exit code 0 and all assertions passed. Review began only after all 39600 tasks were complete. No gates, thresholds, cells or seeds were altered in response to these outcomes.

This is bounded empirical calibration on the declared settings. It is not exact finite-sample uniformity, calibration at every possible parameter/sample size, or evidence that real word-type frequencies are independent.
