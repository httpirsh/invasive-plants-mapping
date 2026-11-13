# src

Reusable Python modules, extracted from notebooks only once code is
stable and would otherwise be duplicated. Subfolders (e.g. `data/`,
`features/`, `evaluation/`) are created when first needed.

Modules:
- `burned_areas.py`: downloads the ICNF burned areas and applies the
  burned-between-observation-and-2023 rule (used by both
  citizen-science notebooks).
- `grid.py`: 10 m pixel ids (EPSG:32629), to match observations to
  the pixel the model sees.
- `embeddings.py`: loads the RQ1 pilot's fetched TESSERA embeddings
  and assigns 10 km spatial-block ids, for the one-class and
  presence-vs-background notebooks under `07_foundation_models/`.
- `background.py`: samples, builds and loads the two background pools.
  Building is done only by
  `notebooks/05_data_integration/background_pools.ipynb`; every other
  notebook loads a pool with `load_background`.
- `manifest.py`: writes and checks `data/processed_manifest.csv`, so
  that a notebook stops when a derived file or one of its inputs has
  changed.
- `evaluation.py`: continuous Boyce index (Hirzel et al., 2006), used
  by the same notebooks to evaluate presence-only/presence-background
  models.
