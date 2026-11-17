# Implementation

Run modules from the member root. Python 3.13.17 and the exact numerical dependency versions in `../requirements.txt` were used. Every simulation task owns its PCG64 stream; process scheduling does not enter the seed.

- `ingest.py`: validate the released ZIP and write deterministic book metadata.
- `models.py`: strict integer histograms, compressed likelihoods, constrained maximum likelihood, discrete KS and full-support sampling.
- `reference.py`: high-precision formulas, optimization and difficult-comparison handling.
- `bootstrap.py`: fixed-B, refitted null simulations with inclusive/strict counts and numerical diagnostics.
- `calibrate.py`: frozen synthetic grid, checkpoint identity and completeness checks, calibration and recovery screens.
- `reproduce.py`: independently seeded complete passes A/B, gated on successful full calibration.
- `precision.py`: prespecified stratified selection and fresh fixed 10,000-draw audit.
- `report.py`: per-book arithmetic, table gates, sensitivities and cross-pass stability.
- `build_reader.py` and `reader.html`: checked standalone interactive reader with embedded aggregates.
- `write_report.py`: complete numerical prose report from the final machine-readable report.
- `plot_figures.py`: standalone PNG/SVG exports of the scoped Figures 3 and 7(a); optional plotting dependency in `../requirements-figures.txt`.

No simulation kernel should be changed underneath a manifested run. Preserve completed runs, amend the contract when required, and use a new output directory for changed code. A fresh run is preferred; reproduction/precision checkpoints require a matching manifest. Calibration's current fresh run was not resumed; its orphan-checkpoint edge case remains a known runner limitation and must not be used to adopt unmanifested records.

The high-precision reference is separately implemented from the ordinary fast formulas, but also serves as the rare near-one production fallback. Fitted-KS refinement has conservative numerical checks, not a universal interval proof. See the implementation review in the planning folder.
