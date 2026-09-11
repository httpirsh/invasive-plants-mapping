# Notebooks

The main environment for exploration, analysis and experimentation.
Subfolders are numbered to follow the research progression; a notebook
in a later folder may depend on outputs from an earlier one, but the
numbering is not a strict pipeline that must be re-run end to end.

| Folder | Purpose |
|---|---|
| `01_problem_exploration/` | Understand the problem, review the state of the art, frame the research questions |
| `02_citizen_science/` | Explore the citizen science dataset on its own (species, coordinates, dates, quality, bias) |
| `03_satellite/` | Explore the satellite/Earth Observation data on its own (source, resolution, bands, cloud cover) |
| `04_data_integration/` | Combine citizen science observations with satellite information into a labelled dataset |
| `05_baseline/` | Simplest credible modelling approach using conventional features |
| `06_foundation_models/` | Extract and explore Earth Observation Foundation Model representations |
| `07_experiments/` | Controlled comparisons between baseline, foundation-model and fusion approaches |
| `08_final_analysis/` | Compare experiments, generate final predictions/maps, error analysis |

Code that becomes reusable or stable enough to be shared across
notebooks should be moved into `src/`, not duplicated between
notebooks.
