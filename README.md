# Mapping Invasive Alien Plants with Earth Observation Foundation Models

Master's Thesis — Artificial Intelligence and Data Science,
University of Coimbra

## Research Question

How robust and data-efficient are Earth Observation foundation models
for invasive plant mapping when trained with citizen-science reference
data?

See [`docs/research_questions.md`](docs/research_questions.md) for the
secondary questions and design, and [`docs/literature.md`](docs/literature.md)
for how they follow from the literature.

## Project Structure

```
invasive-plants-mapping/
├── data/          # Datasets; provenance in data/README.md (files not versioned)
├── notebooks/     # Main research environment, numbered by research stage
├── src/           # Reusable code, extracted from notebooks once stable
├── experiments/   # Experiment configurations and runs
├── results/       # Generated figures, tables, maps and models (not versioned)
└── docs/          # Research questions, literature, open methodological questions
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Notebook outputs are stripped from what Git stores. After cloning, run
once:

```bash
pipx install nbstripout   # or: pip install --user nbstripout
nbstripout --install
```

Local notebooks keep their outputs; only the committed version is
stripped.

Repository conventions (data handling, commits, notebooks) are in
[`CLAUDE.md`](CLAUDE.md).
