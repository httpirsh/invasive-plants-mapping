# Methodology

Methodological questions that are still **open**. Decisions already
made or proposed (prediction task, other-plant classes, temporal
design) are in [`research_questions.md`](research_questions.md);
dataset provenance is in [`data/README.md`](../data/README.md).

**Grounded in** notes name the work that already used an option and
from which the idea comes — the paper's actual finding is in
[`literature.md`](literature.md), not repeated here.

## Data Quality

Check before modelling.

- **Citizen science:** duplicates (37% of pilot records share a 10 m
  pixel), coordinate accuracy (missing for ~80% of pilot records),
  quality grade, taxonomic consistency, observer dominance.
- **Satellite:** cloud contamination, missing observations, alignment
  with observation locations.

Decided: research grade only, for presences and other
plants. Positional accuracy: known values above 30 m
dropped, missing values kept and marked. Same pixel:
one presence per pixel; other plants in a presence's pixel dropped;
other plants one per pixel. Other-plant classes (to
confirm): 8 groups from GIFT growth forms and the national invasive
list; herbaceous only in COS classes where herbs are the top layer;
one other plant per pixel, the tallest group first.

**Grounded in:** Gillespie et al. (2024); Brown et al. (2025) (research
grade); Ball et al. (2026) (label impurity); Karasiak et al. (2022)
(nearby samples) — see `literature.md` for their findings.

## Validation

- Random splits alone are not acceptable: nearby observations make
  train and test sets too similar.
- **Adopted: spatial block holdout, 10 km blocks** (5 spatial splits,
  used throughout the RQ1 notebooks so far), with attention to spatial
  leakage and autocorrelation. Geographically separated test regions
  are the same idea at a larger scale, needed specifically for RQ3
  (distinct regions, not yet available); grouped K-fold remains a
  fallback if the 10 km blocks prove too few once RQ3 regions are
  added.
- **Expert-polygon side needs a buffer, not just block holdout
  (supervisor, recalled — see
  [`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)):**
  expert polygons are contiguous patches, so a validation pixel can
  sit right next to a training pixel even within a kept 10 km block.
  Buffer size given as "20/30"; **assumed to be 20–30 m (my
  decision, not confirmed by the supervisor)** — the empirical
  variogram and Karasiak's own software both point to pixels
  (200–300 m) instead, but this was not pursued further. Not yet
  implemented in the actual train/test split. **Deferred past the
  January report (scope decision, agreed in conversation,
  2026-11-10):** stated as a known, identified limitation of the
  current RQ1 result in the report, not fixed before it.
- Open: an independent validation reference not drawn from the same
  citizen-science source. Without it, biased training data evaluated
  on equally biased test data hides the bias. Narrowed to the COS 2023
  *Acacia* class only — an OrtoSat sample checked by hand was also
  considered and dropped, same manual-interpretation effort the
  supervisor called inefficient for multiclass training labels, see
  [`research_questions.md`](research_questions.md#other-open-points)
  and
  [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).
  Not attempted before the January report — deferred to the work plan.

**Grounded in:** Karasiak et al. (2021/2022) and Le Rest et al. (2014)
(buffer/spatial-leakage requirement, buffer = autocorrelation range,
not fixed); Mahoney, Johnson & Silge (2023) (block/cluster holdout at
least as robust as buffered leave-one-out); the old-growth forest
preprint (2026) (validation choice can change the RQ1 result); Domingo
et al. (2023) is a counter-example with no spatial cross-validation
confirmed — see `literature.md`.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
→ conventional classifier, not multiclass — presence-vs-background,
the method carried forward for this arm (one-class SVM tested and
dropped, see below) (see
[RQ1](research_questions.md#rq1--foundation-models-vs-conventional-approaches)
and [Other Plants as
Background](research_questions.md#other-plants-as-classes-adopted-direction)).
It answers *how well can this be done without foundation models?*
Phase 1 uses TESSERA only; the Sentinel-2 arm is deferred again
— a same-day attempt to start it found that point-level
extraction is not actually cheaper than a full raster download here
(points cover almost the whole pilot extent), so the original
supervisor sequencing stands as the real priority, not
just a temporary phasing. Feature set is decided below for whenever
this resumes; still open is how to make the extraction itself
affordable (fewer scenes, coarser resolution, or a different
environment). See
[Foundation Model Use](research_questions.md#foundation-model-use-adopted)
and [`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo).

**One-class method: tested, then dropped for future arms
(scope-reduction decision, 2026-11-10).** One-class SVM (chosen over
Isolation Forest by direct comparison) consistently lost to
presence-vs-background on both arms tested so far (citizen science and
expert), with the gap widening under a harder background check. Not
re-run by default on the Sentinel-2 arm or further curve extensions —
kept only as an already-tested, documented result. See
[`notebooks/07_foundation_models/one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb)
and
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
for the comparison and full reasoning.

Feature set, for whenever this arm resumes (my proposal,
agreed in conversation, not yet supervisor-confirmed): Ball et al.
(2026) annual composite (median of all 12 bands, 2023, + NDVI/NDWI/NBR),
with Domingo et al. (2023) flowering-phenology features added later as
an ablation, not built
together upfront — see
[`thesis/notes.md`](../thesis/notes.md#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al).
Background design: uniform random points, 50 m buffer, kept (not
switched to COS-stratified) — see
[`docs/research_questions.md`](research_questions.md#reference-data-pipeline-proposed)
and [`thesis/notes.md`](../thesis/notes.md#rq1-fundo-uniforme-nao-cos)
for the reasoning; still not supervisor-confirmed as final. Shared
across both label sources and every point of the effort-reduction
curve — see
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Grounded in:** Sentinel-2 at 10 m for *Acacia* — Mouta et al. (2021);
Domingo et al. (2023). Flowering-season features — Domingo et al.
(2023); Martins et al. (2016). Random Forest — Mouta et al. (2021);
Domingo et al. (2023); Eskandari et al. (2025); Ball et al. (2026).
Findings: `literature.md`.

## Foundation Models

**Model (adopted, Phase 1): TESSERA only.** AlphaEarth (access
unconfirmed) and fusion (embeddings + conventional features) are
explicitly out of scope for the January report — fusion needs the
Sentinel-2 arm, already deferred, and AlphaEarth's access was never
confirmed; neither can advance regardless. Both move to the work plan
as later, unstarted possibilities, not open decisions blocking January.

**Grounded in:** TESSERA (Feng et al., 2025) and AlphaEarth (Brown et
al., 2025) compared by Ball et al. (2026); fusion motivated by the
same paper's classifier-dependent result — see `literature.md`.

## Evaluation

**Metrics (adopted): ROC-AUC and the continuous Boyce index** (Hirzel
et al., 2006), used throughout the RQ1 notebooks so far. Precision,
recall and F1 are no longer candidates: their grounding (Ball et al.,
2026) was for a multiclass setting ("macro F1 exposes rare classes,
relevant with several plant classes"), which no longer applies now
that multiclass was abandoned and *A. dealbata* is the only target
class — see
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).
Never report a metric without stating what was evaluated, on which
data, and under which split.

**Grounded in:** Hirzel et al. (2006) (continuous Boyce index,
presence-only evaluation without confirmed absences — see
`literature.md`); Gillespie et al. (2024) reported AUC.

## Error Analysis

Go beyond aggregate metrics: where and why do models fail? Candidate
dimensions: region, land-cover context (COS), observation density,
observer, quality of the citizen-science record. Not attempted before
the January report — deferred to the work plan: the region dimension
needs RQ3 (deferred), the land-cover dimension needs the segmentation
mask comparison (deferred), so a systematic pass isn't possible yet
with only one region and one arm run. The habitat-concentration finding
already written up for RQ1 (see
[`research_questions.md`](research_questions.md#rq1--foundation-models-vs-conventional-approaches))
stands in as an informal error explanation for the January report.

## Final Map

Document the area mapped, how pixel probabilities become a map, any
threshold used, and uncertainty where available. Interpret the map in
light of the validation results and known data limitations.

**Grounded in:** mapping uncertainty alongside predictions was done by
the Michigan Deepbiosphere preprint (2026).
