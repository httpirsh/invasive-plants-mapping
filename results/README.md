# Results

Generated outputs (figures, tables, maps, trained models). Versioned,
except heavy files such as rasters and trained models (see
`.gitignore`); subfolders are created as needed.

Folder names and question numbers:

- `effort_reduction_curve/` holds the effort-reduction curve (RQ1),
  written by `experiments/effort_reduction_curve/run.py`: `per_fold.csv`,
  `summary.csv`, `pooled_curve.csv`, `paired_differences.csv`,
  `test_sizes.csv`, `nominal_levels.csv`, `run.json`;
  `curve_by_source.png` is drawn from them by
  `notebooks/07_foundation_models/effort_reduction_curve.ipynb`.
- `effort_reduction_curve_buffer_300m/` and
  `effort_reduction_curve_buffer_1000m/` hold the same curve with a
  buffer between training and test (sensitivity analysis), written by
  the same script with `--buffer-m 300` and `--buffer-m 1000`.
- `effort_reduction_curve_buffer_comparison/` holds the differences
  between those two runs and the curve without buffer, paired by fold,
  written by `experiments/effort_reduction_curve/compare_buffer.py`.
- `tables/rq2_sample_150_seed0.csv` is the subsample of 150 presences
  of RQ2 (segmentation mask), drawn with seed 0 at the end of
  `notebooks/02_citizen_science/acacia_observations.ipynb` on every
  run.

Deleted folders (their files are in the Git history):

- `effort_reduction_curve_forest_only/` — the curve under a
  forest-only background, run with the presence-vs-background Random
  Forest under five random block holdouts, superseded on 2026-11-17 by
  the presence-only design of RQ1 (`thesis/notes.md#rq1-presence-only`)
  and not re-run; deleted on 2026-11-17, last present at commit
  `7197628`. The other curve folders were regenerated on
  2026-11-17 by the rewritten scripts (`run.json` in each).
