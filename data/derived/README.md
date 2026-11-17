# Deterministic corpus metadata

`books.csv` contains one row per released frequency vector: PG identifier, type count N, token length L, hapax count, maximum count, raw member size and SHA-256. `ingest.json` records archive identity, structural checks and source length anchors. Regenerate with `python -m src.ingest` from the member root. No model estimates or acceptance decisions are present.
