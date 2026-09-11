# src

Reusable Python modules, introduced only once code becomes stable
enough that it would otherwise be duplicated across notebooks. This
folder is expected to stay mostly empty in the early stages of the
project.

| Folder | Purpose |
|---|---|
| `data/` | Loading and basic access to raw/processed datasets |
| `preprocessing/` | Cleaning and intermediate processing of citizen science and satellite data |
| `features/` | Conventional (non-foundation-model) feature engineering |
| `foundation_models/` | Loading Earth Observation Foundation Models and extracting embeddings |
| `models/` | Model definitions and training code |
| `evaluation/` | Metrics and spatially aware validation utilities |
| `visualization/` | Plotting and mapping helpers |
