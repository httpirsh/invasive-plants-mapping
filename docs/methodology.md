# Methodology

Methodological questions not tied to a single research question:
their current state, and what is still open. The research questions
and the shared design (prediction task, reference-data pipeline,
temporal design) are in [`research_questions.md`](research_questions.md);
dataset provenance is in [`data/README.md`](../data/README.md); the
reasoning behind each decision is in
[`thesis/notes.md`](../thesis/notes.md#decisões).

**Grounded in** notes name the work an option comes from. The paper's
finding is in [`literature.md`](literature.md), not repeated here.

## Data Quality

What was checked before modelling, and what was decided:

- **Citizen science:** duplicates (37% of pilot records share a 10 m
  pixel), coordinate accuracy (missing for about 80% of pilot
  records), quality grade, taxonomic consistency, observer dominance.
- **Decided:** research grade only; known positional accuracy above
  30 m dropped, missing values kept and marked; one presence per
  pixel. Counts and reasons per step:
  [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed).
- **Satellite (still to check when the Sentinel-2 arm resumes):** cloud
  contamination, missing observations, alignment with observation
  locations.

**Grounded in:** Gillespie et al. (2024); Brown et al. (2025) (research
grade); Ball et al. (2026) (label impurity); Karasiak et al. (2022)
(nearby samples).

## Validation

- Random splits alone are not acceptable: nearby observations make
  train and test sets too similar.
- **Adopted: spatial block holdout, 10 km blocks**, five spatial
  splits, used in every experiment so far.
- **Expert side: a buffer on top of the blocks (supervisor,
  recalled).** Expert polygons are contiguous patches, so a validation
  pixel can sit next to a training pixel inside a kept block. Buffer
  given as "20/30"; assumed to be 20–30 m (my decision, not confirmed),
  although the empirical variogram and Karasiak's own software point
  to pixels (200–300 m). Not implemented yet: stated as a known
  limitation in the January report. Reasoning:
  [`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km).
- **Open: independent validation**, with a reference not drawn from
  the citizen-science source, so that biased training data are not
  evaluated only on equally biased test data. Plan: compare the
  predictions with the COS 2023 *Acacia* class, without spatial
  overlap with the expert polygons used for training. Not done yet.

**Grounded in:** Karasiak et al. (2021/2022) and Le Rest et al. (2014)
(spatial leakage; buffer set to the autocorrelation range); Mahoney,
Johnson & Silge (2023) (block holdout at least as robust as buffered
leave-one-out); Ratsakatika et al. (2026) (validation choice can
change the RQ1 result). Domingo et al. (2023) is a counter-example
with no spatial cross-validation confirmed.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
with the same presence-vs-background Random Forest used for the
embeddings (see
[RQ1](research_questions.md#rq1--foundation-models-vs-conventional-approaches)).
It answers *how well can this be done without foundation models?*

- **Status: on hold.** TESSERA ran first (supervisor). Extracting
  Sentinel-2 at the labelled points turned out to cost about as much
  as the full raster, because the points cover almost the whole pilot
  extent. Still open: how to make the extraction affordable (fewer
  scenes, coarser resolution, or a different environment). See
  [`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo).
- **Feature set (mine, not confirmed by the supervisor):** the annual
  composite of Ball et al. (2026) — the 2023 median of all 12 bands
  plus NDVI, NDWI and NBR. The flowering-phenology features of Domingo
  et al. (2023) are added later, as an ablation. See
  [`thesis/notes.md`](../thesis/notes.md#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al).
- **Background:** the uniform-random pool shared by both label sources
  and every point of the effort-reduction curve (step 7 of the
  [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)).

**Grounded in:** Sentinel-2 at 10 m for *Acacia* — Mouta et al. (2021);
Domingo et al. (2023). Flowering-season features — Domingo et al.
(2023); Martins et al. (2016). Random Forest — Mouta et al. (2021);
Domingo et al. (2023); Eskandari et al. (2025); Ball et al. (2026).

## Foundation Models

**Adopted: TESSERA only.** AlphaEarth (access not confirmed) and
fusion of embeddings with conventional features (needs the Sentinel-2
arm) are possibilities for the work plan, not committed.

**Grounded in:** TESSERA (Feng et al., 2025) and AlphaEarth (Brown et
al., 2025), compared by Ball et al. (2026); fusion is motivated by the
same paper's classifier-dependent result.

## Evaluation

**Adopted: ROC-AUC and the continuous Boyce index** (Hirzel et al.,
2006), used in every RQ1 notebook. Never report a metric without
stating what was evaluated, on which data, and under which split.

**Grounded in:** Hirzel et al. (2006) (presence-only evaluation
without confirmed absences); Gillespie et al. (2024) reported AUC.

## Error Analysis

Go beyond aggregate metrics: where and why do models fail? Candidate
dimensions: region, land-cover context (COS), observation density,
observer, quality of the citizen-science record. Not started: the
region dimension needs RQ3 and the land-cover dimension needs the
segmentation-mask comparison. The
habitat-concentration finding of
[RQ1](research_questions.md#rq1--foundation-models-vs-conventional-approaches)
stands in as an informal error explanation for now.

## Final Map

Document the area mapped, how pixel probabilities become a map, any
threshold used, and uncertainty where available. Interpret the map in
light of the validation results and known data limitations. A
confidence layer based on dissimilarity to the training data is part
of RQ3 (to confirm; see
[RQ3](research_questions.md#rq3--spatial-sampling-concentration)). Not started.

**Grounded in:** mapping uncertainty alongside predictions was done by
the Michigan Deepbiosphere preprint (2026).
