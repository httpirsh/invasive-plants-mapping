# Mapping Invasive Alien Plants with Earth Observation Foundation Models

Master's Thesis — Artificial Intelligence and Data Science
University of Coimbra

## Overview

This project investigates the mapping of invasive alien plants through
the combination of citizen science observations, satellite imagery,
and Earth Observation Foundation Models.

## Research Question

Can Earth Observation Foundation Models improve the mapping of
invasive alien plants when combined with citizen science observations
and satellite imagery?

See [`docs/research_questions.md`](docs/research_questions.md) for the
full (preliminary) set of research questions.

## Research Workflow

The repository is organized to mirror the logical progression of the
thesis, not as a generic software project. Each stage builds on the
previous one:

1. **Problem exploration** — define the problem, research questions,
   and review the state of the art.
2. **Citizen science** — understand the citizen science dataset on its
   own terms (species, coordinates, dates, quality, bias) before using
   it for modelling.
3. **Satellite data** — understand the Earth Observation data on its
   own terms (sensor, resolution, bands, cloud cover, availability).
4. **Data integration** — combine citizen science observations with
   satellite information into a labelled dataset.
5. **Baseline** — establish the simplest credible modelling approach
   (conventional features + conventional ML model) as a point of
   comparison.
6. **Foundation models** — investigate Earth Observation Foundation
   Models and the representations/embeddings they produce.
7. **Experiments** — compare increasingly sophisticated approaches in
   a controlled way (baseline vs. foundation-model embeddings vs.
   fusion vs. ablations).
8. **Evaluation** — assess models with appropriate metrics and
   spatially aware validation, watching for class imbalance and
   spatial leakage.
9. **Final analysis and mapping** — compare experiments, generate
   final predictions and maps, and interpret results.
10. **Thesis writing** — write up the work following the same
    narrative: introduction → state of the art → data → methodology →
    experiments → results → discussion → conclusion.

This workflow is provisional and expected to evolve as the research
progresses.

## Project Structure

```
invasive-plants-mapping/
│
├── data/                     # Datasets (raw, intermediate, processed, external)
├── notebooks/                # Exploration, analysis and experimentation (main research environment)
├── src/                      # Reusable code, extracted from notebooks once stable
├── experiments/              # Experiment configurations and runs
├── results/                  # Figures, tables, maps and trained models produced by the work
├── docs/                     # Research questions, literature review, methodology, notes
└── thesis/                   # Thesis manuscript, mirroring the chapters of the written thesis
```

### `data/`

Datasets used in the project, split into `raw/` (as obtained),
`interim/` (intermediate processing), `processed/` (final, model-ready
data) and `external/` (auxiliary data such as shapefiles or land cover
products). Dataset provenance is documented in
[`data/README.md`](data/README.md). Data files are not
version-controlled (see `.gitignore`).

### `notebooks/`

The main environment for exploration, analysis and experimentation.
Numbered subfolders follow the research progression described above,
from problem exploration through final analysis. See
[`notebooks/README.md`](notebooks/README.md).

### `src/`

Python modules. Code is only moved here from notebooks once it becomes
reusable/stable and would otherwise be duplicated. Not everything
needs to have a corresponding module from the start. See
[`src/README.md`](src/README.md).

### `experiments/`

Configuration and organization for the controlled experiments that
compare baseline, foundation-model, fusion and ablation approaches.
See [`experiments/README.md`](experiments/README.md).

### `results/`

Outputs produced by the work: figures, tables, maps and trained
models. See [`results/README.md`](results/README.md).

### `docs/`

Research questions, literature review, dataset documentation,
methodology notes, experiment notes and meeting notes.

### `thesis/`

The thesis manuscript itself, organized by chapter so that the
repository tells the same story as the written thesis. See
[`thesis/README.md`](thesis/README.md).

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Project metadata is also declared in `pyproject.toml`.

## For AI Assistants

See [`CLAUDE.md`](CLAUDE.md) for the conventions used in this
repository (data handling, commit rules, notebook conventions, current
research stage).

## Status

This project is at an early stage. The structure above is intentionally
flexible: the exact methodology, datasets, foundation model(s) and
experiments will be defined and refined as the research progresses.

---

This README will be updated as the thesis progresses.
