# Notebooks

The main environment for exploration, analysis and experimentation.
Subfolders are numbered to follow the research progression; a notebook
in a later folder may depend on outputs from an earlier one, but the
numbering is not a strict pipeline that must be re-run end to end.

| Folder | Purpose |
|---|---|
| `01_problem_exploration/` | Understand the problem, review the state of the art, frame the research questions |
| `02_citizen_science/` | Download, explore and clean the iNaturalist data: *Acacia* observations and other plants |
| `03_expert_reference/` | Explore and clean the expert reference data (contents, geometry, origin, spread, COS classes) |
| `04_satellite/` | Explore the satellite/Earth Observation data on its own (source, resolution, bands, cloud cover) |
| `05_data_integration/` | Combine the cleaned data with satellite information into a labelled dataset; all data together for QGIS |
| `06_baseline/` | Simplest credible modelling approach using conventional features |
| `07_foundation_models/` | Extract and explore Earth Observation Foundation Model representations |
| `08_experiments/` | Controlled comparisons between baseline, foundation-model and fusion approaches |
| `09_final_analysis/` | Compare experiments, generate final predictions/maps, error analysis |

Folders are created when a stage starts. Within a folder, each
dataset has one notebook: part 1 explores it (nothing changed), part 2
cleans it and saves the result to `data/interim/`.

Run order: `02_citizen_science/acacia_observations` →
`02_citizen_science/other_plants_observations` →
`03_expert_reference/expert_polygons` →
`04_satellite/tessera_embeddings` →
`04_satellite/sentinel2_download` →
`04_satellite/tessera_spatial_autocorrelation` →
`05_data_integration/qgis_overview` →
`05_data_integration/segmentation_mask` →
`07_foundation_models/one_class_method_selection` →
`07_foundation_models/presence_background_citizen_science` →
`07_foundation_models/expert_arm_classifiers` →
`07_foundation_models/effort_reduction_curve` →
`07_foundation_models/forest_only_background_check` →
`07_foundation_models/expert_polygon_redundancy_check` →
`07_foundation_models/expert_polygon_geographic_diversity` →
`07_foundation_models/label_purity_check`.

When to move code into `src/` instead: [`src/README.md`](../src/README.md).
