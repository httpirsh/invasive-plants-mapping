# Experiments

Configurations and runs for the controlled experiments defined per
research question in
[`docs/research_questions.md`](../docs/research_questions.md).
Subfolders are created when the first experiment is run.

- `effort_reduction_curve/run.py`: the effort-reduction curve (RQ1),
  leave-one-block-out, presence-background logistic regression,
  sensitivity at a fixed fraction of predicted area. Writes to
  `results/effort_reduction_curve/`; read and plotted by
  `notebooks/07_foundation_models/effort_reduction_curve.ipynb`.
  With `--buffer-m METRES` it drops, in each fold, the training points
  within that distance of a test point of the fold and writes to
  `results/effort_reduction_curve_buffer_<METRES>m/`. The
  `--background forest_only` option still exists but is not run under
  this design (`results/README.md`).
- `effort_reduction_curve/compare_buffer.py`: compares the runs with
  `--buffer-m 300` and `--buffer-m 1000` with the curve without
  buffer, paired by fold. Run after them; writes to
  `results/effort_reduction_curve_buffer_comparison/`.

## What goes here and what goes in `notebooks/`

Status: my own proposal, **Own reasoning (no source found)** — no
literature was consulted for it.

- **`notebooks/`:** what is read once to explore, decide or
  understand. It is not run again when the data change.
- **`experiments/`:** what is run again when the data or the
  parameters change and whose table goes into a doc or the thesis. It
  is a script with fixed inputs, seeds and output folder in `results/`
  (with a `run.json` and the hashes of the inputs); the notebook only
  reads the results and plots them.
- The criterion is for analyses. Data-preparation notebooks (02 to 05)
  are pipeline steps, stay in `notebooks/` and follow the run order in
  [`notebooks/README.md`](../notebooks/README.md).
- Code shared by an experiment script and a notebook goes in `src/`
  (see [`src/README.md`](../src/README.md)).
- This applies to new work. What already exists is not moved unless I
  ask for it.
