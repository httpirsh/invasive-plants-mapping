# Mapping Invasive Alien Plants with Earth Observation Foundation Models

Master's Thesis — Artificial Intelligence and Data Science,
University of Coimbra

## Research Question

To what extent can citizen-science observations, turned into reference
data and represented by Earth Observation foundation-model embeddings,
reduce the amount of expert reference data needed to train a model
that maps *Acacia dealbata* in the Coimbra district?

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
├── results/       # Generated figures, tables, maps and models (versioned, except heavy files)
├── thesis/        # Decision log (notes.md) and document/ (LaTeX manuscript, synced with Overleaf)
└── docs/          # Research questions, literature, open questions, meetings, to-do
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

## Thesis Manuscript (Overleaf)

The manuscript lives in `thesis/document/`, synced with Overleaf via
`git subtree` (not a submodule, so a normal clone of this repo already
has the full text — no extra `--recurse-submodules` step).

One-time setup (only needed again on a fresh machine or if the
Overleaf project changes):

```bash
git remote add overleaf https://git.overleaf.com/<project_id>
git fetch overleaf
git subtree add --prefix=thesis/document overleaf main --squash
```

`<project_id>` and the git URL are in the Overleaf project menu →
**Git**. Overleaf prompts for your Overleaf email as username and a
token as password — generate the token once under Overleaf account
settings → **Git integration**; it is not your account password. Check
the Overleaf project's default branch name with `git ls-remote
overleaf` — it has been `main`, not `master`.

To sync afterwards:

```bash
# pull edits made in the Overleaf web editor into this repo
git subtree pull --prefix=thesis/document overleaf main --squash

# push local edits back to Overleaf
git subtree push --prefix=thesis/document overleaf main
```

Overleaf's git bridge only fast-forwards: always `pull` before editing
locally if the document was also touched in the web editor, to avoid a
conflicted push.
