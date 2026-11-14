# Results

Generated outputs (figures, tables, maps, trained models). Not
version-controlled (see `.gitignore`); subfolders are created as
needed.

Folder names and question numbers:

- `effort_reduction_curve/` holds the effort-reduction curve (RQ1),
  written by `experiments/effort_reduction_curve/run.py`.
- `effort_reduction_curve_forest_only/` holds the same curve under the
  forest-only background (robustness check), written by the same
  script with `--background forest_only`.
- `effort_reduction_curve_buffer_300m/` and
  `effort_reduction_curve_buffer_1000m/` hold the same curve with a
  buffer between training and test (sensitivity analysis), written by
  the same script with `--buffer-m 300` and `--buffer-m 1000`.
- `effort_reduction_curve_buffer_comparison/` holds the differences
  between those two runs and the curve without buffer, paired by seed,
  written by `experiments/effort_reduction_curve/compare_buffer.py`.
- `tables/rq2_sample_150_seed0.csv` is the subsample of 150 presences
  of RQ2 (segmentation mask), drawn with seed 0 at the end of
  `notebooks/02_citizen_science/acacia_observations.ipynb` on every
  run.
