"""Generate prose/tables from the final report; scientific review remains external."""
import json
from pathlib import Path
from .build_reader import LABELS

ROOT=Path(__file__).resolve().parents[1]


def main():
    r=json.loads((ROOT/'results/report.json').read_bytes())
    ps=r['precision_summary'];a=r['acceptance'];s=r['stability']
    lines=['# Gutenberg Zipf model comparison',
           '',f"The power-law survival model f2 is accepted for {a['f2']['observed']:,} of 31,075 books ({100*a['f2']['observed']/31075:.2f}%), compared with {a['f1']['observed']:,} ({100*a['f1']['observed']/31075:.2f}%) for the power-law mass model f1. The ratio is {r['acceptance_ratio']['observed']:.4f}; the published Table 1 implies 2.7221.",
           '',('All predeclared table-comparison bands pass; individual counts are not exact matches.' if r['all_declared_table_bands_pass'] else '**Partial numerical reproduction: some predeclared table-comparison bands fail.** See every exact difference below.'),
           '', '“Accepted” means not rejected by the specified full-support fit test at p>=0.05. It does not prove that the model generates natural language. These are the frozen primary pass-A results, with 100 refitted simulations per book/model. Pass B measures Monte Carlo stability and never substitutes for pass A.',
           '', '[Open the interactive reader](index.html). [Machine-readable report](results/report.json).',
           '', '## Published-table comparison',
           '', 'Targets are transcribed from the publisher PDF, Tables 1–2, pp. 12–13. The bands were frozen after exposure to the September pilot results: they are reproduction tolerances, not confidence intervals. The seed already contained earlier numerical results; this is not an unexposed confirmatory study.',
           '', '| Table / group / column | This run | Paper | Difference | Allowed difference | Band |',
           '|---|---:|---:|---:|---:|---|']
    for name,cols in (('table1',['R>0','R<0','Total']),('table2',['Significant f1','Significant f2'])):
        for group,values in r[name].items():
            for col,g in zip(cols,values): lines.append(f"| {name} / {LABELS[group]} / {col} | {g['observed']} | {g['expected']} | {g['difference']:+} | {g['tolerance']:g} | {'PASS' if g['pass'] else 'FAIL'} |")
    for model,g in r['acceptance'].items():
        lines.append(f"| {model} accepted total | {g['observed']} | {g['expected']} | {g['difference']:+} | {g['tolerance']:g} | {'PASS' if g['pass'] else 'FAIL'} |")
    g=r['acceptance_ratio']
    lines.append(f"| f2/f1 acceptance ratio | {g['observed']:.6f} | {g['expected']:.6f} | {g['difference']:+.6f} | {g['tolerance']:g} | {'PASS' if g['pass'] else 'FAIL'} |")
    lines+=['','Table 2’s displayed total covers its first three groups only; its separate neither-model row is excluded from that total. R>0 favors f1, R<0 favors f2; significance is pLR<0.05. A relative preference does not imply an adequate absolute fit.',
            '',f"Every significant opposite-preference case is retained, even if a printed-zero cell remains within its five-book tolerance: **{len(r['contradictory_books'])} cases**."]
    if r['contradictory_books']:
        lines+=['','| PG ID | KS group | R | pLR | K f1 | K f2 |','|---:|---|---:|---:|---:|---:|']
        for q in r['contradictory_books']:lines.append(f"| {q['pg_id']} | {q['category']} | {q['R']:.8g} | {q['p_lr']:.8g} | {q['K_f1']} | {q['K_f2']} |")
    strict=r['strict_cutoff_table_comparison']
    lines+=['','## Bounded discrepancy investigation','',
            f"The predeclared strict-cutoff sensitivity p>0.05 yields f1 {strict['acceptance']['f1']:,}, f2 {strict['acceptance']['f2']:,}, ratio {strict['ratio']:.4f}. {'All' if strict['all_comparison_bands_pass'] else 'Not all'} numerical comparison bands pass under that sensitivity. The printed Figure 7/8/9 captions support the inclusive primary convention, so this is a convention-sensitivity clue, not evidence of what the authors implemented. No threshold or primary classification was changed.",
            '', 'A fresh-context reviewer reread/hash-verified every raw vector and independently refit all 31,075 f1 models with an analytic Euler–Maclaurin zeta derivative. Maximum beta disagreement was 2.023e-12 and KS disagreement 2.543e-13. Another 36 independent 80-digit f1/f2 comparisons at extreme, K4/K5 and anchor cases also agree. No input or observed-fit numerical cause was diagnosed. Primary statistic ties are zero; plus-one p-values leave these grid decisions unchanged.',
            '', 'The authors’ per-book seeds and full implementation were not located in the inspected paper, dataset and author-publication sources. The residual historical cause remains unassigned. This bounded investigation does not prove that author code is unavailable everywhere. [Review and evidence](planning/moreno-review-primary-results.md).',
            '', '## Monte Carlo stability','','| Model | Accepted A | Accepted B | A only | B only | Switches | Relative net change | Kappa |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for m,v in s.items(): lines.append(f"| {m} | {v['A_accepted']} | {v['B_accepted']} | {v['A_only']} | {v['B_only']} | {v['switches']} ({100*v['switches']/31075:.2f}%) | {100*v['relative_accepted_count_change']:+.3f}% | {v['kappa']:.5f} |")
    lines+=['','| Model / pass-A status | B accepted | B rejected |','|---|---:|---:|']
    for m,v in s.items():lines.extend([f"| {m} / A accepted | {v['both_accept']} | {v['A_only']} |",f"| {m} / A rejected | {v['B_only']} | {v['both_reject']} |"])
    p=r['exposed_prediction_checks']
    lines+=['',f"The exposed pilot prediction of 500–2,000 f2 switches is {'met' if p['f2_switches_500_to_2000']['within_prediction'] else 'not met'} ({s['f2']['switches']}). The predicted relative accepted-count change within ±4% is "+', '.join(f"{m}: {'met' if v['within_prediction'] else 'not met'}" for m,v in p['net_relative_change_within_4pct'].items())+'. These predictions are reported diagnostics, not calibration or reproduction gates.',
            '', 'At an ideal conditional bootstrap probability of 0.05, B=100 has Monte Carlo standard error about 0.02179. Two runs can therefore disagree about individual books while their corpus totals remain close. That uncertainty concerns the fitted-null simulation, not natural-language model uncertainty.',
            '', '## Fixed 10,000-draw precision audit',
            '',f"The prespecified hash ordering selects up to 50 pairs per model in each pass-A K stratum 1–3, 4–5, 6–10 and 11–20. The completed audit contains {ps['selected_pairs']} book/model pairs, with fresh fixed B=10,000 runs and no early stopping or reuse of the selecting trials. The other {ps['not_precision_audited_pairs']:,} pairs are **not precision audited**. This stratified subset cannot estimate a whole-corpus classification error rate.",
            '', '| Model | Rejected | Non-rejected | Unresolved |','|---|---:|---:|---:|']
    for m,v in ps['models'].items():lines.append(f"| {m} | {v['rejected']} | {v['non_rejected']} | {v['unresolved']} |")
    changes=r['precision_reclassifications']
    lines+=['',f"Within these selected pairs, {sum(sum(v.values()) for v in changes.values())} interval-resolved determinations disagree with the original pass-A call. "+'; '.join(f"{m}: {v['A_accepted_now_rejected']} A-accepted to rejected, {v['A_rejected_now_non_rejected']} A-rejected to non-rejected" for m,v in changes.items())+'. These are conditional Monte Carlo findings within the selected subset, not whole-corpus errors.']
    lines+=['','Classification uses pointwise 95% Clopper–Pearson intervals: upper<0.05 rejects, lower>=0.05 does not reject, otherwise unresolved. These intervals quantify conditional Monte Carlo uncertainty; they are not simultaneous guarantees across the selected pairs. Worst-case Monte Carlo SE is 0.005.',
            '', '| Model | Selecting K range | Candidates | Audited |','|---|---|---:|---:|']
    for v in ps['strata']:lines.append(f"| f{v['model']} | {v['stratum'][0]}–{v['stratum'][1]} | {v['candidates']} | {v['selected']} |")
    lines+=['','The exact selected list and all intervals are in [pairs.jsonl](results/precision-001/pairs.jsonl); the reader offers a CSV download.',
            '', '## Sensitivities and figures',
            '', 'The machine-readable report contains every centile cutoff from 0.01 to 0.50; all 31,075 books are included. The reader redraws the scoped versions of Figures 3 and 7(a). Length bins sort by (L,PG ID), use 31 full 1,000-book bins and a separately marked 75-book remainder. A toggle removes only that remainder from the length plot.',
            '', 'Strict p>0.05, strict statistic exceedance Dsim>Dobs, sample-variance LR and pooled B=200 results are preserved as sensitivities. Plus-one p=(K+1)/101 changes p-values but keeps the centile-grid classifications identical for cutoffs 0.01–0.50. Off-grid thresholds can differ.',
            '', '| Model | Accepted beta mean | Population SD | Sample SD | Paper mean / SD |','|---|---:|---:|---:|---|']
    for m,v in r['beta_moments'].items():lines.append(f"| {m} | {v['mean']:.6f} | {v['sd_population']:.6f} | {v['sd_sample']:.6f} | {v['printed']['mean']:.2f} / {v['printed']['sd']:.2f} |")
    lines+=['','Figure 9 length quartiles are descriptive reconstructions, sorted by (L,PG ID) among accepted books, with nearly equal groups and extra books assigned first. The seed’s p>0.05 caption claim was corrected from the native source: the published caption uses p>=0.05. Figure 4 instead uses p>1/2 for its illustrative selection.',
            '', '## Method and calibration',
            '', 'The observation is a word type’s positive token count n; the fitting sample size N is the number of types, not total token length L. Models: f1(n)=n^(-beta)/zeta(beta), f2(n)=n^(1-beta)-(n+1)^(1-beta), with a=1 and 1<beta<=4. There is no fitted lower cutoff or observed-maximum truncation. Each simulated vector has N observations and is refitted before computing the discrete KS statistic at both sides of every support jump.',
            '', 'All 39,600 nested calibration tasks completed: 18 primary cells with 2,000 outer samples, and 18 supplementary cells with 200. Each outer sample has 100 refitted inner draws. Every primary CP screen and all six N=30,000 ensemble recovery intervals pass. An independent fresh-context reviewer recomputed the gates and full cell summaries from all raw records. The primary 0.05 rejection rates range from 4.2% to 5.4%. The screen is bounded calibration error around 5/101, not exact rank uniformity.',
            '', 'Supplementary results remain visible: f2 at N=210,347 and beta=1.5 rejects 18/200 (9%; a wide adjusted interval includes 5/101). Small-N estimator bias can be substantial, so universal ±0.005 bias was not a valid requirement; the frozen recovery screen applies only at N=30,000. Full per-cell counts, beta bias/SD, K histograms and refinement counters are in [the calibration summary](results/calibration-001/summary.json) and the reader.',
            '', 'Independent high-precision formula/optimization checks cover ordinary and extreme supports; the sampler keeps arbitrary integer tails rather than clipping them. Adaptive fitted-KS comparisons use conservative numerical margins and increasing precision, not a formal interval proof for every transcendental operation. The high-precision reference also serves as the rare beta<1.05 fallback, so fast-versus-reference independence does not supply a second implementation of that fallback.',
            '', '## Data, scope and audit',
            '', 'All 31,075 released vectors are preserved with no filtering: 1,961,738,645 tokens; N ranges from 27 to 210,347. The exact ZIP, per-member hashes, deterministic ingest and all five length anchors are verified. The scoped Figure 4 estimates round to the printed 1.96 and 1.89. Reproducing those rounded estimates does not reproduce the seed-dependent historical maximum-book selection.',
            '', 'This is an independent implementation, reviewed first by fresh-context AI agents of the same model family and then by Gemini 4 Carbon of a different model family. Review independence concerns context, production role and model family, not independent human conceptual replication. The core assumes iid types under its null; it does not show that real word types are independent. No cross-project code was copied or adapted: Axtell and Pilgrim–Hills were high-level precedent only.',
            '', 'Deferred: full f3 reproduction, length-tail fit, genre causation, alternate tokenization, SPGC overlap and holdouts. No novelty or intent claim is made. [Frozen contract](planning/AMENDMENT-1.md), [freeze record](planning/CONTRACT-FREEZE.json), [audit record](AUDIT.md), [Step 0](STEP0.md).',
            '', '## Primary sources',
            '', '- Moreno-Sánchez, I., Font-Clos, F. & Corral, Á. (2016). [Large-Scale Analysis of Zipf’s Law in English Texts](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0147073). PLOS ONE 11(1): e0147073. CC BY. Preserved publisher PDF, especially Tables 1–2 and Figures 3–4, 7–9.',
            '- Authors’ [word frequencies from Project Gutenberg English texts, v3](https://figshare.com/articles/dataset/Word_frequencies_from_Project_Gutenberg_English_texts/1515919/3), CC BY 4.0. PG_English_wordfreqs.zip, file 2284750. SHA-256 `6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61`.', '']
    lines+=['', '## Credits and licensing', '', 'Research, implementation and presentation by OpenAI Codex (GPT-6), directed by Kenrin. Cross-family audit by Gemini 4 Carbon (High), with separate Codex scientific and reader reviews. [Full credits](CREDITS.md). Original code: [MIT](LICENSE); original report, figures and result data: [CC BY 4.0](REPORT-LICENSE). [Third-party notices](THIRD_PARTY_NOTICES.md).', '']
    (ROOT/'REPORT.md').write_bytes('\n'.join(lines).encode('utf-8'))
    print('Generated REPORT.md from completed report.json')


if __name__=='__main__':main()
