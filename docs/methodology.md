# Methodology

Methodological questions that are still **open**. Decisions already
made or proposed (prediction task, other-plant classes, temporal
design) are in [`research_questions.md`](research_questions.md);
dataset provenance is in [`data/README.md`](../data/README.md).

**Grounded in** notes name the work that already used an option and
from which the idea comes.

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

**Grounded in:** research-grade-only observations were used by
Gillespie et al. (2024) and Brown et al. (2025). Positional accuracy
and per-pixel duplicates are motivated by Ball et al. (2026), where
label impurity lowered accuracy, and by Karasiak et al. (2022), where
nearby train and test samples inflated accuracy: duplicates in one
pixel act the same way.

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

**Grounded in:** Karasiak et al. (2022) showed with
Sentinel-2 that non-spatial cross-validation overestimates accuracy,
while spatial leave-one-out matches real map quality; the spatial
validation requirement comes from there. The old-growth forest
preprint (2026) showed buffered spatial validation narrows
the embedding advantage over Sentinel features, so the validation
choice can change the RQ1 result. Domingo et al. (2023) is a
counter-example: high accuracy, but no spatial cross-validation
confirmed.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
→ conventional classifier. It answers *how well can this be done
without foundation models?* Establish it early, but do not
over-optimise it before the foundation-model pipeline exists.

Open: feature set (bands, indices, seasonal composites); classifier
(Random Forest, Logistic Regression, compact neural network). Ball et
al. (2026) found a compact neural network beat Random Forest on
embeddings.

**Grounded in:**

- Sentinel-2 at 10 m for *Acacia*: Mouta et al. (2021, *A. longifolia*,
  northern Portugal, fusion of eight classifiers) and Domingo et al.
  (2023, *A. dealbata*, Galicia, time series with Random Forest).
- Flowering-season features: Domingo et al. (2023) used
  flowering-period spectral differences; Martins et al. (2016) got the best accuracy with flowering-season ASTER imagery.
  Seasonal composites covering the winter flowering of *A. dealbata*
  follow them.
- Random Forest: Mouta et al. (2021), Domingo et al. (2023),
  Eskandari et al. (2025, best of the algorithms tested) and Ball et
  al. (2026).

## Foundation Models

Open:

- Which model(s): TESSERA (accessible, MIT), AlphaEarth (access
  unconfirmed), other.
- Whether to also test fusion (embeddings + conventional features).

**Grounded in:** TESSERA (Feng et al., 2025) and AlphaEarth
(Brown et al., 2025) are the two models compared by Ball et
al. (2026); TESSERA was also evaluated on tree species by its authors.
Fusion is motivated by Ball et al. (2026), where the advantage of
embeddings depended on the classifier (linear models on embeddings
were weaker than neural networks on conventional composites), so the
two representations may carry complementary information.

## Evaluation

Candidate metrics: precision, recall, F1, ROC-AUC, PR-AUC — final
choice depends on class balance and the cost of false positives vs.
false negatives. Never report a metric without stating what was
evaluated, on which data, and under which split.

**Grounded in:** Ball et al. (2026) reported weighted and macro F1
(macro F1 exposes rare classes, relevant with several plant classes);
Gillespie et al. (2024) reported AUC; Domingo et al. (2023) and
Martins et al. (2016) reported overall accuracy.

## Error Analysis

Go beyond aggregate metrics: where and why do models fail? Candidate
dimensions: region, land-cover context (COS), observation density,
observer, quality of the citizen-science record.

## Final Map

Document the area mapped, how pixel probabilities become a map, any
threshold used, and uncertainty where available. Interpret the map in
light of the validation results and known data limitations.

**Grounded in:** mapping uncertainty alongside predictions was done by
the Michigan Deepbiosphere preprint (2026).
