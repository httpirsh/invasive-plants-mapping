# Research Questions

How the research questions and the shared design work now. Reasoning
behind each decision: [`thesis/notes.md`](../thesis/notes.md#decisões).
How the questions follow from the literature:
[`literature.md`](literature.md). Methodological questions not tied to
one question: [`methodology.md`](methodology.md).

Each decision has a **Grounded in** note naming the work that already
used it or that motivates it. Items marked *to confirm* are mine and
the supervisor has not answered yet.

## Fit with the Thesis Proposal

The thesis is part of MAP.INVADER. The proposal's main objective is to
**reduce dependency on costly reference data by turning citizen-science
point observations into training data for satellite classifiers of
invasive alien plants**. Each part of the proposal maps to a part of
this document:

| Proposal | Addressed by |
|---|---|
| Main objective — reduce the dependency on costly reference data | Main question; RQ1 (citizen science against expert reference data) |
| Obj. 1 / work plan 3 — transform point observations into usable EO reference data, accounting for uncertainty and quality | [Reference-Data Pipeline](#reference-data-pipeline-proposed); RQ2 (effect of the grade and accuracy filters and of extending each point to the patch around it). Uncertainty is covered only through the positional-accuracy filter and the mask: the uncertainty of each observation does not enter the model |
| Obj. 2 — use foundation models to compensate for limited, noisy citizen-science data | RQ4, for limited data: both representations are trained on cleaned data, so compensation for label noise is not tested |
| Obj. 3 — assess to what extent citizen science supports accurate, species-level mapping | RQ1; [Species Scope](#species-scope-proposed) |
| Work plan 4 — fine-tune foundation models; analyse accuracy, limitations, transferability | [Foundation Model Use](#foundation-model-use-adopted) (frozen embeddings, a justified deviation); RQ3 (performance away from the sampled area, within the district) |

## Main Question and Objectives

*Wording and numbering mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#renumeracao-perguntas-2026-11-13);
main question:
[`thesis/notes.md`](../thesis/notes.md#pergunta-principal-dados-de-treino)).*

**Main question:** To what extent can citizen-science observations,
turned into reference data and represented by Earth Observation
foundation-model embeddings, replace expert reference data as training
data for mapping *Acacia dealbata* in the Coimbra district?

**General objective:** to assess to what extent citizen-science
observations, turned into reference data and represented by
foundation-model embeddings, can replace expert reference data as
training data for mapping *A. dealbata* in the Coimbra district.

**Specific objectives:**

1. To measure the performance gained by adding 10% to 100% of the
   expert polygons to a citizen-science base, to compare it with the
   expert-only model, and to report the performance of the
   citizen-science-only model on expert reference data (RQ1).
2. To build and document the process that turns citizen-science point
   observations into reference data, and to measure how its grade and
   accuracy filters and the extension of each label to the surrounding
   vegetation patch change performance (RQ2).
3. To measure the difference in performance between locations near
   and far from the sampled area (RQ3).
4. To compare TESSERA-based and Sentinel-2-based models, with all
   observations and with few (RQ4).
5. To produce the *A. dealbata* map of the study area, with a
   confidence map. Whether the model separates *A. dealbata* from
   other *Acacia* species is not tested and is left as future work.

**Common context:** *Acacia dealbata*, Coimbra district, 2023 imagery,
research-grade iNaturalist observations from 2021–2025, 90% of them
from one observer, TESSERA vs. Sentinel-2 features; a presence-only
classifier; performance measured as sensitivity at a fixed fraction of
predicted area under leave-one-block-out over 10 km blocks, with
ROC-AUC and the continuous Boyce index as secondary metrics (to
confirm with the supervisor; the area fraction, 10%, is my choice:
[`thesis/notes.md`](../thesis/notes.md#rq1-presence-only)).

**What "replace" means here:** the difference in performance between
models trained on citizen-science observations and models trained
with expert reference data. Expert data remain the test reference.

**Hypotheses** are stated under each question as a null (H₀) and an
alternative (H₁), each marked as written before or after its result
was seen. They are working hypotheses, not formal statistical tests.

**What is reported for every hypothesis:** the per-fold difference in
sensitivity at the fixed area fraction between the two conditions
(same test block): its mean, its standard deviation and the number of
folds in which it has the same sign, with the sensitivity-by-area
curve (5% to 30%) and the secondary metrics next to it. The
difference is reported and no decision threshold is applied, because
the folds are few and unequal in size. Each question names the two
conditions compared.

## Secondary Questions

Each question uses only what the questions before it define; the one
that depends on Sentinel-2 comes last.

### Scope

Each question is a complete result on its own:

| Question | Delivers | Answers, in the thesis proposal | Depends on |
|---|---|---|---|
| RQ1 | The effort-reduction curve | Main objective and obj. 3 | TESSERA only; measured |
| RQ2 | The reference-data pipeline, and the effect of its grade and accuracy filters and of extending point labels to patches | Obj. 1 | TESSERA only; the mask needs an extraction of TESSERA windows, to approve before running |
| RQ3 | Performance away from the sampled area, and a confidence map | Work plan 4 (transferability) | TESSERA only |
| RQ4 | TESSERA against Sentinel-2 | Obj. 2, for limited data | The Sentinel-2 arm, on hold |

Scope is reassessed as experiments progress.

### Risks shared by the four questions

Each question also lists its own risks.

- **The secondary metrics may not separate the models.** The Boyce
  index is near 0.99 for every model so far and, being rank-based,
  cannot rank models whose curves all rise monotonically (Hirzel et
  al., 2006). ROC-AUC against background counts an unrecorded acacia
  in the background as an error, so its maximum is below 1 and not
  known here (Phillips et al., 2009). The primary metric avoids both
  by never labelling background as absence; its literature is not yet
  read. See [`methodology.md`](methodology.md#evaluation).
- **Spatial blocks have no buffer between them.** Training and test
  pixels on either side of a block border can be close, which can
  inflate scores (Karasiak et al., 2022; Ratsakatika et al., 2026).
  Measured for the RQ1 curve with buffers of 300 m and 1 km, as a
  sensitivity analysis: see
  [`methodology.md`](methodology.md#validation).
- **The Sentinel-2 arm is on hold.** RQ4 cannot be answered without
  it; RQ1, RQ2 and RQ3 do not depend on it.

### RQ1 — Citizen science as a substitute for expert data

*Question and wording mine, to confirm with the supervisor. The idea
of the curve is his
([meeting of 2026-11-05](meetings/2026-11-05.md)); its details are
mine, to confirm with him
([`thesis/notes.md`](../thesis/notes.md#rq2-curva-por-fonte)).*

**Question:** To what extent does a model trained only on
citizen-science observations reach the performance of models trained
with expert reference data?

**Hypotheses:** H₀: adding expert data does not change performance.
H₁: performance increases with the fraction of expert data. H₁ was
written after the curve had been observed, so this is not a
pre-registered test.

**Reported:** 90% against 0% of the expert polygons. The pooled test
set (citizen-science and expert presences together) is the main one,
as in the curve design; the expert presences alone are a second
analysis, reported next to it.

**Design (curve idea: supervisor; details: mine, to confirm with
him):** an effort-reduction curve. Expert data are
added on top of a fixed citizen-science base, from 0% to 100% in
10-point steps, so the citizen-science base is in training at every
level. The **expert-only** model (no citizen science) is a separate
reference point, not a level of the curve (to confirm with the
supervisor:
[`thesis/notes.md`](../thesis/notes.md#curva-100-mais-ciencia-cidada)).
The mixing unit is the polygon, sampled in a
nested order; the percentages are of the 1 457 polygons that hold at
least one pixel with a stored embedding, of the 1 849 in the district;
one spatial test set per seed is reused at every level
and always contains both sources; results are averaged over five
seeds. Reasoning:
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Classifier:** presence-only, chosen by a method-selection step that
compares true one-class models (Isolation Forest, One-Class SVM; no
background in training) with presence-background models that use the
background as an unlabelled sample of the landscape (L2 logistic
regression, MaxEnt), each with a small hyperparameter sweep under the
shared protocol. **Measured (to confirm with the supervisor):** the
best configurations of the presence-background models beat the best
one-class configurations at every area fraction; pooled sensitivity at
10% of area is 0.410 for the logistic regression (`C=10`), 0.334 for
MaxEnt (linear + quadratic features), 0.258 for the One-Class SVM and
0.188 for the Isolation Forest (chance 0.10). PCA reconstruction, a
small autoencoder and their ensembles with the Isolation Forest were
tested and stay near chance. The logistic regression with `C=10` is
the classifier of the curve. Why, criterion, caveats and what is to
confirm:
[`thesis/notes.md`](../thesis/notes.md#rq1-presence-only);
notebook
[`presence_only_method_selection.ipynb`](../notebooks/07_foundation_models/presence_only_method_selection.ipynb).

**Measured:** the curve is not run yet under this classifier and
metric (task in [`docs/todo.md`](todo.md)). The script
[`experiments/effort_reduction_curve/run.py`](../experiments/effort_reduction_curve/run.py)
is rewritten for it.

**Known from the data, before running:** expert presences may be
easier to separate from the background than citizen-science ones:
55.0% of expert pixels fall in the COS 2023 "Florestas de acácias"
class, against 17.9% of citizen-science presences
([`thesis/notes.md`](../thesis/notes.md#diagnosticos-curva-plana)).
The independent units are polygons and 10 km blocks.
Sensitivity of the curve to a buffer between training and test:
[`methodology.md`](methodology.md#validation).

**Not measured:** the curve with Sentinel-2 features (not planned: see RQ4);
the curve diagnostics (forest-only background, redundancy, label
purity) split by source of the test presences.

**Risks:**

- The result may be specific to this pilot (one region, TESSERA only)
  or to the metrics, not a finding about expert data in general.
- Expert polygons fall in only 18 blocks of 10 km, so there are few
  independent spatial splits.

**Grounded in:** training the same model on citizen-science vs. expert
data comes from Dimson et al. (2023), who report that the two sources
often have inverse biases; an analogy only, since here experts and the
dominant observer visited the same places. That the expert end of the
curve is biased differently, not bias-free, rests on this project's
own habitat-composition result. The curve design itself has no
literature precedent checked yet. Presence-only classifier: Rapinel &
Hubert-Moy (2021) on background vs. pseudo-absences; Phillips et al.
(2009) on background as an unlabelled sample; Deng et al. (2018),
Mack & Waske (2017), Li & Guo (2010) on presence-background methods
against true one-class ones.

**Expert reference labels (adopted):** *A. dealbata* polygons sent by
the supervisor; provenance and counts in
[`data/README.md`](../data/README.md#acacia-dealbata-expert-reference-polygons).

- In the Coimbra district: 1 849 polygons with `classifica = 1`
  (244 ha); 56% fall in a COS 2023 "Florestas de acácias" polygon,
  most of the rest in pine, eucalyptus and other forest.
- **Clustered:** they fall in only 18 blocks of 10 km, so few
  independent spatial blocks are available to split training and test.
- **Background:** `classifica = 0` polygons are not used as negatives
  (supervisor — why:
  [`thesis/notes.md`](../thesis/notes.md#usar-os-dados-de-especialistas-com-limpeza)).
  Both sources share the uniform-random background pool, step 7 of the
  [Reference-Data Pipeline](#reference-data-pipeline-proposed).
- **Independent of citizen science:** iNaturalist did not influence
  the collection (supervisor).
- **Locations overlap with citizen science:** all 22 cleaned
  iNaturalist presences inside a polygon, and 97% of the 143 within
  50 m, are the dominant observer's. Experts and that observer visited
  the same places, so training and test must be split by spatial
  blocks, and both sources inherit a similar spatial coverage.
- **Open:** how the sites were chosen.

### RQ2 — From point observations to reference data

*Question and design are mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#renumeracao-perguntas-2026-11-13);
mask design:
[`thesis/notes.md`](../thesis/notes.md#rq2-proposta-mascara)). The
segmentation mask itself is his: central, try several approaches.*

**Question:** To what extent do the grade and accuracy filters applied
to citizen-science observations, and the extension of each label from
the observed pixel to the vegetation patch around it, change the
performance of *A. dealbata* mapping?

**Hypotheses (written before running; no performance result exists
for either):**

- H₀a: performance is the same with pixel-only and patch labels. H₁a:
  it differs — more pixels per observation may help, and wrong pixels
  (the mask spreading into similar non-*Acacia* vegetation) may harm.
- H₀b: performance is the same with and without the grade and accuracy
  filters. H₁b: it differs.

**Reported:** for H₀a, each mask rule against pixel-only training, at
each data level; for H₀b, training without the two filters against
training with them, with all observations.

**Design:**

- **Label extent, three training conditions:** the observed pixel
  only; **region growing** on TESSERA embedding similarity from the
  observed pixel; **superpixels** computed on TESSERA embeddings. The
  supervisor's "nearest vegetation area" is read as extending the
  label to the vegetation patch (to confirm with the supervisor).
- **One configuration per mask rule, fixed before running and not
  tuned on the results:**

  | Rule | Configuration |
  |---|---|
  | Region growing | Cosine similarity to the observed pixel ≥ 0.90; 4-connected growth; at most 5 pixels (50 m) from the observed pixel along each axis, so at most 121 pixels |
  | Superpixels | SLIC on a 41 × 41 pixel window of embeddings; mean size 25 pixels (0.25 ha), so 67 segments per window; compactness 0.1; the label goes to the superpixel that holds the observed pixel |

- **Grade and accuracy filters, two training conditions:** both
  applied (the 2 465 presence pixels), or neither (steps 2 and 3 of
  the [Reference-Data Pipeline](#reference-data-pipeline-proposed):
  positional accuracy and quality grade). In the 2021–2025 window the
  two filters remove 1 553 observations, which add 1 122 pixels; 1 120
  of these have a stored TESSERA embedding and form the unfiltered
  condition, and the 2 observations without one are left out of it
  (counts from [`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb)).
  Observations with obscured coordinates (step 1; 12 in the window)
  are excluded from both conditions, so step 1 is not measured. The
  2021–2025 window, the species and one presence per pixel are the
  same in both. No step-by-step ablation.
- **Two data levels for the mask:** all 2 465 presences, and a random
  subsample of 150 (6%). The small level is where a difference can
  show, since the RQ1 curve is near its ceiling with all data. The
  filter comparison runs with all observations only.
- **Only the training labels change.** Test set (the filtered one),
  background pool, classifier, folds and metric are those of RQ1.
  TESSERA only: the question is about the labels, not the
  representation.
- **Comparison between the two mask rules is descriptive**, with the
  number of pixels each adds per observation.
- **Leakage:** mask pixels and unfiltered observations that fall in a
  test block or on a background point are removed.
- **Status:** not run. The filter comparison needs no new embeddings.
  The mask comparison needs the TESSERA windows around the
  observations, which are not stored: that extraction is to approve
  before running. Measured so far: the counts of each pipeline step,
  and the patch sizes of both rules on a sample of 30 observations
  with other parameter values (pixel counts only).

**Risks:**

- No difference between conditions, even at 150 presences.
- The mask may spread into similar non-*Acacia* vegetation and add
  wrong labels.
- The mask configuration is not calibrated; a different one could give
  a different answer.
- The background pool was drawn with a 50 m exclusion zone around the
  filtered presences only. In the unfiltered condition a background
  point can lie within 50 m of an added presence; only a point on the
  same pixel is removed.

**Grounded in:** superpixel propagation of point labels follows the
idea of Rivier et al. (2024); Raine et al. (2022) compute superpixels
on learned features, with a modest gain over colour-based ones. Both
use many correctly placed points per image. Region growing to densify
point labels at Sentinel-2 scale: Zhang et al. (2021), who grow on
classifier confidence. Raine et al. (2026) propagate point labels by
similarity on frozen foundation-model features, in underwater images
with several points of several classes; no precedent found for a
similarity threshold, a connectivity rule or a maximum radius. No
paper found combines point-to-patch propagation with sparse
presence-only citizen-science points and frozen satellite embeddings,
so that combination is a possible contribution.
The mask configuration is my own reasoning, with no source found: no
paper read gives a value usable here. The 50 m limit is the exclusion
distance of the background pool around presences (step 7 of the
pipeline), and 25 pixels is the same 50 m scale. The limit holds along
each axis: the corners of the 11 × 11 window lie 71 m from the
observed pixel. One of the 2 000 background points lies inside the
window of a presence ([`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb));
a background point that a mask labels as *Acacia* is taken out of the
background of that condition (my rule, to apply when the mask runs). The
filtered-against-unfiltered comparison is adapted from the one-factor
ablations of Ball et al. (2026); Fonte et al. (2020) measure the
effect of filtering volunteered training data on a land-cover map.
Research grade is an agreement indicator, which measures reliability
and not accuracy unless compared with reference data (Fonte et al.,
2017).
Summaries:
[`literature.md`](literature.md#weak-supervision-from-point-labels);
reasoning and counts:
[`thesis/notes.md`](../thesis/notes.md#renumeracao-perguntas-2026-11-13).

### RQ3 — Transferability away from the sampled area

*The supervisor approved a question on spatial sampling concentration;
this wording and design are mine, to confirm with him
([`thesis/notes.md`](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).*

**Question:** To what extent does the performance of the
citizen-science-trained model drop from locations near the sampled
area to locations far from it?

**Hypotheses (written before running):** H₀: no difference in
performance between near and far locations. H₁: performance is lower
far from the sampled area. The RQ1 value of the citizen-science-only
model on expert presences, the starting point of this question, is not
measured yet under the current classifier and metric.

**Reported:** far against near expert polygons. The difference is
reported without attributing its cause to distance (see Risks).

**Design:**

- **Starting point:** one observer made 90% of the 2 465 presences,
  and their points occupy 15 of the 39 blocks of 10 km that hold
  presences (EPSG:32629 grid, as in the experiments). That is
  concentration; whether it harms the model is what is measured.
- **Model:** in each fold, the citizen-science-only (0%) model of RQ1:
  the same test block, trained on the citizen-science presences
  outside it (and, for a presence-background classifier, the
  background points outside it), with TESSERA.
- **Folds:** the leave-one-block-out folds of RQ1 vary the test block,
  and with it the training set and the test background.
- **Test set:** the expert pixels, against the background points of
  the seed's test blocks. The 21 expert pixels that are also the pixel
  of a citizen-science presence are left out, so no test pixel trains
  this model.
- **Near and far:** distance from each expert polygon to the nearest
  citizen-science training presence; near is up to 1 km, far is beyond
  1 km, inside the district only.
- **Counts:** measured to the 2 465 presences, 1 645 polygons are near
  (1 643 of them in the district) and 206 polygons in the district
  are far, between 1.0 and 8.2 km.
  With a stored embedding, and without the 21 shared pixels (all
  near), the test set holds 1 251 near polygons (1 961 pixels) and 205
  far ones (789 pixels). Counts from
  [`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb);
  the counts per seed are not made yet.
- **Product:** a feature-space dissimilarity map (area of
  applicability) as a confidence layer for the final map.
- **Status:** not run. No part of this question uses Sentinel-2:
  whether foundation models amplify or mitigate the effect, against
  conventional features, is not tested.

**Risks:**

- Near and far polygons differ in more than distance. In the district
  the median far polygon is about 36 times larger than the median near
  one (2 788 m² against 77 m²), and the land cover differs somewhat
  (pine forest holds 23.7% of near polygons and 10.2% of far ones;
  COS 2023 "Florestas de acácias" 55.6% and 59.2%).
- Large patches are easy to detect, so performance may be high both
  near and far and show nothing.
- "Far" is at most 8.2 km from a citizen-science presence, so the
  result does not speak for other regions.

**Grounded in:** clustering of citizen-science records in a few
places: Cambridge TESSERA group. Embedding-based models lost accuracy
in another region in Yang et al. (2026) and, against conventional
features, in Ma et al. (2026; AlphaEarth, crop yield). Models
trained on volunteered data lost accuracy between two Portuguese
regions in Duarte et al. (2022; OpenStreetMap, land cover). The
dissimilarity map follows Meyer & Pebesma (2021), tested there on
regression only, so its use with a classifier on embeddings is an
extension. No precedent found for citizen science concentrated in one
observer: Milanesi et al. (2020) model observers' effort without
examining concentration. The 1 km cut and the
use of the expert pixels as test data are my own reasoning, with no
source found.

### RQ4 — Foundation models vs. conventional features

*Question and design are mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).*

**Question:** To what extent do TESSERA embeddings improve
*A. dealbata* mapping over Sentinel-2 features when trained on cleaned
citizen-science data, with all observations and with few?

**Hypotheses (written before running):** H₀: no performance
difference between TESSERA and Sentinel-2 models, at either data
level. H₁: the TESSERA model performs better, with a larger difference
at the small data level.

**Reported:** TESSERA against Sentinel-2 at each data level.

**Design:**

- **Only the representation changes.** Same classifier, test set,
  background pool, folds and metric as RQ1; all representations come
  from the same reference year.
- **Two data levels:** all 2 465 presences and the random subsample of
  150 used in RQ2.
- **Citizen-science training data only.** The effort-reduction curve
  of RQ1 and the near–far comparison of RQ3 are not repeated with
  Sentinel-2.
- **Cleaned data only.** Whether embeddings compensate for label noise
  is not tested.
- **Status: not run, nothing measured.** The whole question depends on
  the Sentinel-2 arm, which is on hold (see
  [Foundation Model Use](#foundation-model-use-adopted)); its feature
  set is decided, see [`methodology.md`](methodology.md#baseline).

**Risks:**

- The Sentinel-2 extraction may stay too costly to run.
- With all observations the models may be too close to the ceiling of
  the metrics to be separated.
- A light classifier may understate the embeddings: in Koukos et al.
  (2026) the distance between engineered features and TESSERA is 8.4
  points of macro F1 with Random Forest and 1.1 with a neural network.
  Whether this holds for the presence-only classifier chosen in RQ1 is
  not known.

**Grounded in:** the representation comparison follows Ball et al.
(2026), whose conventional arm combines Sentinel-1 and Sentinel-2; not
yet tested for invasive plants with citizen-science labels. Silva &
Gonçalves (2026) is a Portuguese case where the Sentinel-2 baseline
beat TESSERA. The two data levels have a precedent in Koukos et al.
(2026): engineered features ahead with all the data, TESSERA ahead
below about 25% of the training plots. No source read for the choice of 150 presences as the
small level.

## Shared Design (RQ1–RQ4)

### Prediction Task (adopted)

**Pixel-level classification trained on points, applied
wall-to-wall.** The classifier is trained on the 10 m pixel at each
observation (Sentinel-2 features or foundation-model embedding), then
applied to every pixel of the study area. The task is presence-only:
the classifier learns from *Acacia* presences, with the background at
most as an unlabelled sample of the landscape, never as absence; the
*Acacia* map is the per-pixel score (relative suitability, not a
probability of presence against absence).

**Grounded in:** Brown et al. (2025) — findings in `literature.md`.

**Segmentation mask:** whether the label of each observation is
extended to the patch around it is tested in
[RQ2](#rq2--from-point-observations-to-reference-data). The task stays pixel
classification; the mask changes how many pixels around each
observation count as *Acacia* training data.

Grid-cell presence/absence is not the training unit: pixel predictions
may later be aggregated to cells for evaluation.

### Reference-Data Pipeline (proposed)

Answers the proposal's first objective. The steps that turn
iNaturalist points into labelled pixels are treated as a
**methodological contribution**: each step is documented and its
counts are reported. The effect of the grade and accuracy filters
(steps 2 and 3) is measured in
[RQ2](#rq2--from-point-observations-to-reference-data).

| Step | Status | Notes | Grounded in |
|---|---|---|---|
| 1. Remove obscured coordinates | Done | 43 *Acacia* observations removed (all species) | iNaturalist geoprivacy randomises these coordinates (platform documentation); Brown et al. (2025) and Gillespie et al. (2024) filter on location quality explicitly |
| 2. Positional accuracy | Adopted | Drop known accuracy > 30 m; keep missing values, marked `accuracy_missing`. Presences 3 441 → 3 276. Why 30 m (the COS test): [`thesis/notes.md`](../thesis/notes.md#precisão-da-localização-tirar-acima-de-30-m-manter-as-sem-valor) | Filtering on positional uncertainty: Brown et al. (2025), ≤10 m; Gillespie et al. (2024), ≤120 m. The 30 m value is from my own test |
| 3. Quality grade | Adopted | Research grade only. Presences 5 242 → 3 441. Why: [`thesis/notes.md`](../thesis/notes.md#só-observações-research-nos-dois-lados) | Gillespie et al. (2024); Brown et al. (2025) |
| 4. Observation years | Adopted | Keep observations from 2021–2025; every presence kept is treated as 2023. Presences 3 276 → 2 580. See [Temporal Design](#temporal-design-adopted) | See that section |
| 5. Disturbance filter | Proposed (fixed) | Burned between observation and 2023 (ICNF 1975–2025): no *A. dealbata* presence is flagged within 2021–2025 | Riveiro et al. (2025): fire does not remove the species, it regrows from seed and resprouts. That the 2023 pixel no longer matches the label is my reasoning; Silva & Gonçalves (2026) show fire changes a TESSERA annual embedding |
| 6. Label purity | Checked, no large-scale problem found | Expert-polygon agreement (limited power) and embedding-outlier detection found no evidence that presences are frequently off-target. See [`thesis/notes.md`](../thesis/notes.md#diagnosticos-curva-plana) | Ball et al. (2026) report tolerance to moderate label impurity, of a different kind (mixed-species parcels) |
| 7. Negative/background | Adopted | Uniform-random points, 50 m buffer around known presences; not yet confirmed by the supervisor. Why: [`thesis/notes.md`](../thesis/notes.md#rq1-fundo-uniforme-nao-cos) | My own choice. Rapinel & Hubert-Moy (2021) recommend background over the whole landscape, without excluding the surroundings of presences. Phillips et al. (2009) argue for the opposite, a target-group background, and show that a check scored against background points, such as the forest-only one, cannot rule out background bias |
| 8. Same pixel | Adopted | Pixel = 10 m cell in EPSG:32629. One presence per pixel, closest to 2023 (2 580 → 2 465). Why: [`thesis/notes.md`](../thesis/notes.md#uma-observação-por-píxel-nos-conflitos-fica-a-presença) | My own reasoning (observations in one pixel share one embedding); no source found |
| 9. Observer balancing | Adopted | The main model uses all of Observer A's observations (90% of the 2 465 presences). Why: [`thesis/notes.md`](../thesis/notes.md#observer-a-todas-as-observações-no-modelo-principal) | Dimson et al. (2023) recommend keeping all available data; Phillips et al. (2009) call discarding records unpalatable when records are few. Neither addresses one dominant observer |

The table is grouped by topic. In the cleaning, the steps on single
observations run first (1, species, 3, 2, 4), then step 8, then step
5; counts at every step:
[`data/README.md`](../data/README.md#inaturalist-observations-cleaned-derived).

**Effect of the filters:** RQ2 compares training with and without
the grade and accuracy filters (steps 2 and 3), as two conditions.

**Cumulative ablation (optional):** run the RQ1 setup after adding
each step and report the change in performance (adapted from the
one-factor ablations of Ball et al., 2026). Not a committed
deliverable: the methodological contribution rests on the documented,
justified pipeline above and on RQ2 (see
[`literature.md`](literature.md#contribution)).

### Foundation Model Use (adopted)

**Frozen embeddings + light classifiers**, not fine-tuning. This is a
deliberate deviation from the proposal's "fine-tune EO foundation
models" and must be stated as such.

Reasons:

- AlphaEarth is released only as embeddings; it cannot be fine-tuned.
- TESSERA code is open and the paper describes the weights as open,
  but the repository restricts the checkpoint (checked 2026-11-11).
- Fine-tuning the TESSERA encoder gave no benefit over frozen
  embeddings in its own paper (Feng et al., 2026).
- With few, noisy labels, fine-tuning risks fitting the noise.
- The same classifier on every representation isolates the effect of
  the representation (RQ4).

**Grounded in:** Ball et al. (2026); Yang et al. (2026); Brown et al.
(2025) — all used frozen embeddings with a light classifier on top;
Feng et al. (2026) for fine-tuning; findings in `literature.md`.

**Phasing (supervisor): TESSERA first, Sentinel-2 after.** The RQ1
curve ran first with TESSERA embeddings. The Sentinel-2 arm is on
hold: extracting it at the labelled points turned out to cost about as
much as the full raster (see
[`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)).
Its feature set is already decided, see
[`methodology.md`](methodology.md#baseline).

### Temporal Design (adopted)

*The observation window is my decision; the supervisor has not been
told yet
([`thesis/notes.md`](../thesis/notes.md#janela-temporal-2021-2025)).*

Time is **held constant, not studied**:

1. **Reference year 2023** for all imagery and auxiliary products
   (Sentinel-2 features, TESSERA embeddings, COS/OrtoSat).
2. **Every iNaturalist presence is treated as representative of the
   stand in 2023**, the year of the predictor variables.
3. **Only observations from 2021–2025 are kept** (2023 ± 2 years), to
   support that assumption. It is step 4 of the
   [Reference-Data Pipeline](#reference-data-pipeline-proposed): after
   the checks on each observation, before the one-per-pixel step and
   the burned-area flag.

Data constraints:

| Source | Temporal availability |
|---|---|
| OrtoSat / COS | 2023 only |
| TESSERA | One embedding per tile per year; 2017–2024 in Feng et al. (2026) |
| Sentinel-2 | Any date from 2015/2017 |
| Citizen science (*Acacia*, Coimbra pilot) | Raw download 1992–2026; 43% of records from 2021, 98% of those from one observer. 2021–2025 holds 2 580 of the 3 276 presences that pass the checks on each observation (79%) |

Assumption (mine, no source read for it): *Acacia* stands persist for
years, so an observation within two years of 2023 is evidence of
presence in 2023 unless the site was disturbed. The effect of the
distance in time is not tested.

Why the window ends in 2025: the 2026 download is an incomplete year
(accessed 2026-09-22), and an observation made after the 2025 fires
may be regrowth.

Why 2023 and not a later year: 704 *A. dealbata* presences (28.6%) lie
in areas burned in 2025; 2023 imagery still shows the observed
vegetation.

Safeguard: **disturbance filter**, step 5 of the
[Reference-Data Pipeline](#reference-data-pipeline-proposed).

**Grounded in:** a single reference year follows Ball et al. (2026),
who found cross-year degradation in one year-pair and warn against
generalising it. Treating observations from several years as one
reference year has precedent in Ball et al. (2026; inventory labels
from 2010–2021 with 2018 imagery) and Gillespie et al. (2024;
observations from 2015–2022 with 2012 imagery). The width of the
window (± 2 years) is my own choice; no source read for it. Riveiro
et al. (2025) supports only that fire does not remove the species.
Findings: `literature.md`.

### Species Scope (proposed)

The proposal asks for **species-level** mapping of a limited number of
representative species. Observations (all years, non-obscured):
*A. dealbata* 5 241, *A. melanoxylon* 1 884, *A. longifolia* 512.

**Proposed: *A. dealbata* as the target.** Other *Acacia* species are
left out of training. Why: [`thesis/notes.md`](../thesis/notes.md#só-acacia-dealbata).

**Not tested:** whether the model separates *A. dealbata* from the
other *Acacia* species. The task is *A. dealbata* against background,
so "species-level" is a stated limitation and the check is left as
future work.

**Grounded in:** mapping *A. dealbata* alone follows Domingo et al.
(2023, Galicia) and Martins et al. (2016, central-eastern Portugal);
Mouta et al. (2021) mapped *A. longifolia* alone.
