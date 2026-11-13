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
- `tables/rq2_sample_150_seed0.csv` is the subsample of 150 presences
  of RQ2 (segmentation mask).

Obsolete folders:

- `temporal_window_2021_2025/`: runs made with the earlier uniform
  background pool; see its `OBSOLETE.md`.
- `rq2_per_source_check/`: the effort-reduction curve as written by
  the notebook, replaced by `effort_reduction_curve/` with identical
  tables; see its `OBSOLETE.md`.
