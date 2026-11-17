# Source data custody

Isabel Moreno-Sánchez, Francesc Font-Clos and Álvaro Corral released *Word frequencies from Project Gutenberg English texts*, [Figshare version 3](https://doi.org/10.6084/m9.figshare.1515919.v3), under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The exact archive was acquired and verified on 17 November 2026: `PG_English_wordfreqs.zip`, file 2284750, 26,349,768 bytes; MD5 `e269dc5e82b0038aae9f9e297dcdb286`; SHA-256 `6c2e479e15b029d8c6a86380230aeb0edd422ae13a4f24e26b799a94c83c9a61`. ZIP CRCs and all 31,075 positive integer frequency vectors were checked. No Gutenberg book text is redistributed here.

The raw archive is not bundled. Run `python -m src.fetch_sources` to retrieve exactly these bytes from the authors' [file endpoint](https://ndownloader.figshare.com/files/2284750). The downloader does not re-ingest or replace derived manifests. The completed calibration, both corpus passes and precision results are included in [the run inventory](../../results/README.md).

[manifest.json](manifest.json), [the acquisition receipt](acquisition-2026-11-17.json) and [Figshare metadata](figshare-1515919.json) are preserved historical records: their `present` fields describe custody during the investigation, not whether an excluded file currently exists in your clone. The raw API metadata intentionally retains its exact original bytes, including its missing final newline. Derived manifests and per-member hashes remain unchanged.
