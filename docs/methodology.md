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
grade and a positional-uncertainty filter); Ball et al. (2026)
(tolerance to label impurity). One presence per pixel is my own
reasoning, with no source found.

## Validation

- Random splits alone are not acceptable: nearby observations make
  train and test sets too similar.
- **Adopted: spatial block holdout, 10 km blocks**, five spatial
  splits, used in every experiment so far.
- **Expert side: a buffer on top of the blocks (supervisor,
  recalled).** Expert polygons are contiguous patches, so a validation
  pixel can sit next to a training pixel inside a kept block. Buffer
  given as "20/30"; assumed to be 20–30 m (my decision, not
  confirmed). The literature does not give a fixed value: the distance
  is estimated from the measured autocorrelation range, and
  underestimating it is the unsafe direction. In this project's
  variogram of TESSERA embeddings the semivariance still rises at
  400–500 m and levels off between 500 m and 1 km (binned means, no
  model fitted). The buffer is not part of the design; it is reported
  as a sensitivity analysis (next item). Reasoning:
  [`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km).
- **No buffer between training and test blocks; its effect is reported
  as a sensitivity analysis (my decision).**
  The papers read agree that blocks alone leave residual proximity
  across block borders and recommend blocks combined with a buffer.
  In the five splits of the RQ1 curve, the presences in training that
  lie close to a test point are 17 of 21 507 within 30 m, 445 (2.1%)
  within 300 m and 1 821 (8.5%) within 1 km, the last ranging from
  under 1% to 27% between seeds
  ([`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb)).
  Removing every training point within 300 m or 1 km of a test point
  leaves the 90% against 0% difference of RQ1 within 0.0014 ROC-AUC,
  with the same sign; with 1 km, ROC-AUC at fixed levels falls by up
  to 0.0075, so the levels without buffer are slightly optimistic.
  Whether that fall comes from less proximity or from less training
  data was not tested. Table and criterion: `thesis/notes.md`, linked
  above; script
  [`compare_buffer.py`](../experiments/effort_reduction_curve/compare_buffer.py).
- **Open: independent validation**, with a reference not drawn from
  the citizen-science source, so that biased training data are not
  evaluated only on equally biased test data. Plan: compare the
  predictions with the COS 2023 *Acacia* class, without spatial
  overlap with the expert polygons used for training. Not done yet.

**Grounded in:** Karasiak et al. (2022) and Le Rest et al. (2014)
(spatial leakage; buffer set to the autocorrelation range estimated
from the data); Mahoney et al. (2023) (blocks combined with an
exclusion buffer performed best); Ratsakatika et al. (2026) (blocks
are necessary but not sufficient, and a buffer can change the
comparison between representations). The *Acacia* mapping papers
(Martins et al., 2016; Mouta et al., 2021; Domingo et al., 2023) all
use random splits.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
with the same presence-vs-background Random Forest used for the
embeddings (see
[RQ4](research_questions.md#rq4--foundation-models-vs-conventional-features)).
It answers *how well can this be done without foundation models?*

- **Status: on hold.** TESSERA ran first (supervisor). Extracting
  Sentinel-2 at the labelled points turned out to cost about as much
  as the full raster, because the points cover almost the whole pilot
  extent. Still open: how to make the extraction affordable (fewer
  scenes, coarser resolution, or a different environment). See
  [`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo).
- **Feature set (mine, not confirmed by the supervisor):** the annual
  composite of Ball et al. (2026) — the 2023 median of all 12 bands
  plus NDVI, NDWI and NBR. It is the simpler of that paper's two
  variants; its headline baseline is seasonal and includes Sentinel-1.
  The flowering-phenology features of Domingo et al. (2023) are added
  later, as an ablation. The *Acacia* mapping papers all find the
  signal in specific months or in differences between them, so the
  ablation may matter more than the annual composite. See
  [`thesis/notes.md`](../thesis/notes.md#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al).
- **Background:** the uniform-random pool shared by both label sources
  and every point of the effort-reduction curve (step 7 of the
  [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)).

**Grounded in:** Sentinel-2 at 10 m for *Acacia* — Mouta et al. (2021);
Domingo et al. (2023). Flowering-season features — Domingo et al.
(2023); Martins et al. (2016). Presence vs. random pseudo-absences
evaluated with ROC — Mouta et al. (2021). Random Forest — see
[RQ1](research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data).

## Foundation Models

**Adopted: TESSERA only.** AlphaEarth (access not confirmed) and
fusion of embeddings with conventional features (needs the Sentinel-2
arm) are possibilities for the work plan, not committed.

**Grounded in:** TESSERA (Feng et al., 2026) and AlphaEarth (Brown et
al., 2025), compared by Ball et al. (2026); fusion is motivated by the
same paper's classifier-dependent result.

## Evaluation

**Adopted: ROC-AUC and the continuous Boyce index** (Hirzel et al.,
2006), used in every notebook of the effort-reduction curve. Never report a metric without
stating what was evaluated, on which data, and under which split.

**Known limits of the Boyce index as computed here**
(`src/evaluation.py`):

- It uses ten adjacent windows of one tenth of the observed score
  range, which is the fixed-class form, not the moving window over
  [0, 1] of Hirzel et al. (2006). With ten values the rank correlation
  moves in coarse steps, so 0.99 is about one swap away from 1.
- The index is rank-based and cannot rank models whose curves all rise
  monotonically; a value near 1 says only that presences become more
  frequent as the score rises.
- It is unstable to small changes in the background pool: see
  [`thesis/notes.md`](../thesis/notes.md#fundo-uniforme-reconstruido-2465).
- **Use:** the index is reported next to ROC-AUC and no conclusion
  rests on it alone. The presence-to-expected curve that Hirzel et al.
  (2006) recommend is not computed; this is a stated limitation.
  Reasoning:
  [`thesis/notes.md`](../thesis/notes.md#simplificacao-desenho-2026-11-13).

**Grounded in:** Hirzel et al. (2006) (presence-only evaluation
without confirmed absences); Gillespie et al. (2024) reported AUC;
Phillips et al. (2009) (AUC against background has a maximum below 1).

## Error Analysis

Go beyond aggregate metrics: where and why do models fail? Candidate
dimensions: region, land-cover context (COS), observation density,
observer, quality of the citizen-science record. Not started: the
region dimension needs RQ3 and the land-cover dimension needs the
segmentation-mask comparison of RQ2. The habitat-composition finding
of
[RQ1](research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data)
stands in as an informal error explanation for now.

## Final Map

Document the area mapped, how pixel probabilities become a map, any
threshold used, and uncertainty where available. Interpret the map in
light of the validation results and known data limitations. A
confidence layer based on dissimilarity to the training data is part
of RQ3 (to confirm; see
[RQ3](research_questions.md#rq3--transferability-away-from-the-sampled-area)). Not started.

**Grounded in:** Ratsakatika et al. (2026) mapped the area of
applicability of Meyer & Pebesma (2021) alongside the predictions of a
model on embeddings.
