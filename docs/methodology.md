# Methodology

Methodological questions that are still **open**. Decisions already
made or proposed (prediction task, absences, temporal design) are in
[`research_questions.md`](research_questions.md); dataset provenance is
in [`data/README.md`](../data/README.md).

## Data Quality

Check before modelling.

- **Citizen science:** duplicates (37% of pilot records share a 10 m
  pixel), coordinate accuracy (missing for ~80% of pilot records),
  quality grade, taxonomic consistency, observer dominance.
- **Satellite:** cloud contamination, missing observations, alignment
  with observation locations.

Open: whether to keep `casual`-grade records; how to handle records
with unknown or coarse positional accuracy; whether to deduplicate
per pixel.

## Validation

- Random splits alone are not acceptable: nearby observations make
  train and test sets too similar.
- Candidates: spatial blocking, grouped K-fold, geographically
  separated test regions (needed for RQ3), with attention to spatial
  leakage and autocorrelation.
- Open: an independent validation reference not drawn from the same
  citizen-science source (candidates: COS 2023, OrtoSat). Without it,
  biased training data evaluated on equally biased test data hides
  the bias.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
→ conventional classifier. It answers *how well can this be done
without foundation models?* Establish it early, but do not
over-optimise it before the foundation-model pipeline exists.

Open: feature set (bands, indices, seasonal composites); classifier
(Random Forest, XGBoost, Logistic Regression). Note Ball et al. (2026)
found a compact neural network beat Random Forest on embeddings.

## Foundation Models

Open:

- Which model(s): TESSERA (accessible, MIT), AlphaEarth (access
  unconfirmed), other.
- Frozen embeddings vs. fine-tuning.
- Whether to also test fusion (embeddings + conventional features).

## Evaluation

Candidate metrics: precision, recall, F1, ROC-AUC, PR-AUC — final
choice depends on class balance and the cost of false positives vs.
false negatives. Never report a metric without stating what was
evaluated, on which data, and under which split.

## Error Analysis

Go beyond aggregate metrics: where and why do models fail? Candidate
dimensions: region, land-cover context (COS), observation density,
observer, quality of the citizen-science record.

## Final Map

Document the area mapped, how pixel probabilities become a map, any
threshold used, and uncertainty where available. Interpret the map in
light of the validation results and known data limitations.
