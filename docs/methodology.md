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
- Candidates: spatial blocking, grouped K-fold, geographically
  separated test regions (needed for RQ3), with attention to spatial
  leakage and autocorrelation.
- **Expert-polygon side needs a buffer, not just block holdout
  (supervisor, recalled — see
  [`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)):**
  expert polygons are contiguous patches, so a validation pixel can
  sit right next to a training pixel even within a kept 10 km block.
  Buffer size given as "20/30"; **assumed to be 20–30 m (my
  decision, not confirmed by the supervisor)** — the empirical
  variogram and Karasiak's own software both point to pixels
  (200–300 m) instead, but this was not pursued further. Not yet
  implemented in the actual train/test split.
- Open: an independent validation reference not drawn from the same
  citizen-science source (candidates: COS 2023, OrtoSat). Without it,
  biased training data evaluated on equally biased test data hides
  the bias.

**Grounded in:** Karasiak et al. (2021/2022) and Le Rest et al. (2014)
(buffer/spatial-leakage requirement, buffer = autocorrelation range,
not fixed); Mahoney, Johnson & Silge (2023) (block/cluster holdout at
least as robust as buffered leave-one-out); the old-growth forest
preprint (2026) (validation choice can change the RQ1 result); Domingo
et al. (2023) is a counter-example with no spatial cross-validation
confirmed — see `literature.md`.

## Baseline

The simplest credible approach: Sentinel-2 spectral-temporal features
→ conventional classifier, not multiclass — run as both true one-class
and presence-vs-background in parallel (see
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

**One-class method: one-class SVM (my decision, by direct
comparison, not Isolation Forest)** — see
[`notebooks/07_foundation_models/one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb)
and [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
for the comparison and its caveats (citizen-science arm only so far,
background not yet supervisor-confirmed).

Feature set, for whenever this arm resumes (my proposal,
agreed in conversation, not yet supervisor-confirmed): Ball et al.
(2026) annual composite (median of all 12 bands, 2023, + NDVI/NDWI/NBR),
with Domingo et al. (2023) flowering-phenology features added later as
an ablation, not built
together upfront — see
[`thesis/notes.md`](../thesis/notes.md#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al).
Also open: exact background design
confirmation (a first version — uniform random points, 50 m buffer —
was built to run the comparison above, not yet supervisor-confirmed as
final), and whether it is shared across both label sources and every
point of the effort-reduction curve — see
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Grounded in:** Sentinel-2 at 10 m for *Acacia* — Mouta et al. (2021);
Domingo et al. (2023). Flowering-season features — Domingo et al.
(2023); Martins et al. (2016). Random Forest — Mouta et al. (2021);
Domingo et al. (2023); Eskandari et al. (2025); Ball et al. (2026).
Findings: `literature.md`.

## Foundation Models

Open:

- Which model(s): TESSERA (accessible, MIT), AlphaEarth (access
  unconfirmed), other.
- Whether to also test fusion (embeddings + conventional features).

**Grounded in:** TESSERA (Feng et al., 2025) and AlphaEarth (Brown et
al., 2025) compared by Ball et al. (2026); fusion motivated by the
same paper's classifier-dependent result — see `literature.md`.

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
