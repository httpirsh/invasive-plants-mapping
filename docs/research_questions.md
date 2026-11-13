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
| Main objective — reduce the dependency on costly reference data | Main question; RQ2 (citizen science against expert reference data) |
| Obj. 1 / work plan 3 — transform point observations into usable EO reference data, accounting for uncertainty and quality | [Reference-Data Pipeline](#reference-data-pipeline-proposed); RQ1 (effect of the quality filters and of extending each point to the patch around it) |
| Obj. 2 — use foundation models to compensate for limited, noisy citizen-science data | RQ3, for limited data and away from the sampled area: both representations are trained on cleaned data, so compensation for label noise is not tested |
| Obj. 3 — assess to what extent citizen science supports accurate, species-level mapping | RQ2; [Species Scope](#species-scope-proposed) |
| Work plan 4 — fine-tune foundation models; analyse accuracy, limitations, transferability | [Foundation Model Use](#foundation-model-use-adopted) (frozen embeddings, a justified deviation); RQ4 (performance away from the sampled area) |

## Main Question and Objectives

*Wording mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#reformulacao-quatro-perguntas)).*

**Main question:** To what extent can citizen-science observations,
turned into reference data and represented by Earth Observation
foundation-model embeddings, replace expert reference data for mapping
*Acacia dealbata* in the Coimbra district?

**General objective:** to assess to what extent citizen-science
observations, turned into reference data and represented by
foundation-model embeddings, can replace expert reference data for
mapping *A. dealbata* in the Coimbra district.

**Specific objectives:**

1. To build and document the process that turns citizen-science point
   observations into reference data, and to measure how its quality
   filters and the extension of each label to the surrounding
   vegetation patch change performance (RQ1).
2. To measure the performance gained by adding 10% to 90% of the
   expert polygons to a citizen-science base, to compare it with the
   expert-only case (100%), and to report the performance of the
   citizen-science-only model on expert reference data (RQ2).
3. To compare TESSERA-based and Sentinel-2-based models, with all
   observations, with few, and away from the sampled area (RQ3).
4. To measure the difference in performance between locations near
   and far from the sampled area (RQ4).
5. To produce the *A. dealbata* map of the study area, with a
   confidence map. Whether the model separates *A. dealbata* from
   other *Acacia* species is not tested and is left as future work.

**Common context:** *Acacia dealbata*, Coimbra district, 2023 imagery,
research-grade iNaturalist observations from 2021–2025, TESSERA vs.
Sentinel-2 features; performance measured with ROC-AUC and the
continuous Boyce index under 10 km spatial block holdout.

**Hypotheses** are stated under each question as a null (H₀) and an
alternative (H₁). They are working hypotheses, not formal statistical
tests: there are five spatial splits, and they reuse blocks.

**How every hypothesis is measured:** by the per-seed difference in
ROC-AUC between the two conditions (same test blocks), reported as its
mean, its standard deviation and the number of seeds in which it has
the same sign. No decision threshold is applied. The Boyce index is
reported next to it. Each question names the two conditions compared.

## Secondary Questions

The questions are numbered in the order of the proposal's objectives.

### Priority and scope

RQ2, RQ1 and RQ4 need only TESSERA; RQ3 needs the Sentinel-2 arm and
runs last. Each stage is a complete result on its own:

| Scenario | Delivers | Answers |
|---|---|---|
| RQ2 only | Reference-data pipeline + the effort-reduction curve | Main objective and objective 3 |
| RQ2 + RQ1 | The above + the effect of the quality filters and of extending point labels to patches | Objective 1 |
| RQ2 + RQ1 + RQ4 | The above + performance away from the sampled area, and a confidence map | Transferability (work plan 4) |
| All four | The above + TESSERA against Sentinel-2 | Objective 2, for limited data. Most exposed to time |

Scope is reassessed as experiments progress.

### Risks shared by the four questions

Each question also lists its own risks.

- **The metrics may not separate the models.** The Boyce index is
  near 0.99 for every model so far and, being rank-based, cannot rank
  models whose curves all rise monotonically (Hirzel et al., 2006).
  Presence-background ROC-AUC has a maximum below 1 that is not known
  here (Phillips et al., 2009). So "no difference" could come from the
  metric rather than the models. See
  [`methodology.md`](methodology.md#evaluation).
- **Spatial blocks have no buffer between them.** Training and test
  pixels on either side of a block border can be close, which can
  inflate scores (Karasiak et al., 2022; Ratsakatika et al., 2026).
  See [`methodology.md`](methodology.md#validation).
- **The Sentinel-2 arm is on hold.** RQ3 cannot be answered without
  it; RQ1, RQ2 and RQ4 do not depend on it.

### RQ1 — From point observations to reference data

*Question and design are mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#reformulacao-quatro-perguntas);
mask design:
[`thesis/notes.md`](../thesis/notes.md#rq2-proposta-mascara)). The
segmentation mask itself is his: central, try several approaches.*

**Question:** To what extent do the quality filters applied to
citizen-science observations, and the extension of each label from the
observed pixel to the vegetation patch around it, change the
performance of *A. dealbata* mapping?

**Hypotheses:**

- H₀a: performance is the same with pixel-only and patch labels. H₁a:
  it differs — more pixels per observation may help, and wrong pixels
  (the mask spreading into similar non-*Acacia* vegetation) may harm.
  *Compared:* each mask rule against pixel-only training, at each data
  level.
- H₀b: performance is the same with unfiltered and filtered
  observations. H₁b: it differs. *Compared:* training on unfiltered
  observations against training on filtered ones, with all
  observations.

**Design:**

- **Label extent, three training conditions:** the observed pixel
  only; **region growing** on TESSERA embedding similarity from the
  observed pixel, with a maximum radius; **superpixels** computed on
  TESSERA embeddings.
- **Quality filters, two training conditions:** all filters applied,
  or none of the quality filters (steps 1 to 3 of the
  [Reference-Data Pipeline](#reference-data-pipeline-proposed):
  obscured coordinates, positional accuracy, quality grade). The
  2021–2025 window, the species and one presence per pixel are the
  same in both. No step-by-step ablation.
- **Two data levels for the mask:** all 2 465 presences, and a random
  subsample of 150 (6%). The small level is where a difference can
  show, since the RQ2 curve is near its ceiling with all data. The
  filter comparison runs with all observations only.
- **Only the training labels change.** Test set (the filtered one),
  background pool, Random Forest, 10 km blocks and five seeds are
  those of RQ2. TESSERA only: the question is about the labels, not
  the representation.
- **One fixed parameter set per mask rule**, justified and stated as a
  limitation; no calibration. Values still to choose.
- **Comparison between the two mask rules is descriptive**, with the
  number of pixels each adds per observation.
- **Leakage:** mask pixels and unfiltered observations that fall in a
  test block or on a background point are removed.
- **Open:** whether the supervisor's "nearest vegetation area" means
  extending the label to the patch (the reading assumed here).

**Risks:**

- No difference between conditions, even at 150 presences.
- The mask may spread into similar non-*Acacia* vegetation and add
  wrong labels.
- The unfiltered condition needs TESSERA embeddings for the
  observations the filters remove, which are not extracted yet.

**Grounded in:** superpixel propagation of point labels follows the
idea of Rivier et al. (2024); Raine et al. (2022) compute superpixels
on learned features, with a modest gain over colour-based ones. Both
use many correctly placed points per image. Region growing to densify
point labels at Sentinel-2 scale: Zhang et al. (2021), who grow on
classifier confidence; no precedent found for growing on embedding
similarity to the seed or for a maximum radius. No paper found
combines point-to-patch propagation with sparse citizen-science points
and frozen embeddings, so that combination is a possible contribution.
The filtered-against-unfiltered comparison is adapted from the
one-factor ablations of Ball et al. (2026). Summaries:
[`literature.md`](literature.md#weak-supervision-from-point-labels).

### RQ2 — Citizen science as a substitute for expert data

*Question and wording mine, to confirm with the supervisor; the curve
design is his
([`thesis/notes.md`](../thesis/notes.md#rq2-curva-por-fonte)).*

**Question:** To what extent does a model trained only on
citizen-science observations reach the performance of models trained
with expert reference data?

**Hypotheses:** H₀: adding expert data does not change performance.
H₁: performance increases with the fraction of expert data.
*Compared:* 90% against 0% of the expert polygons. The pooled test set
(citizen-science and expert presences together) is the main one, as in
the curve design; the expert presences alone are a second analysis,
reported next to it. H₁ was written after the curve had been observed
to be flat, so this is not a pre-registered test.

**Design (supervisor):** an effort-reduction curve. Expert data are
added on top of a fixed citizen-science base, from 0% to 100% in
10-point steps; at 100% the citizen-science base is removed and
training is expert-only. The mixing unit is the polygon, sampled in a
nested order; one spatial test set per seed is reused at every level
and always contains both sources; results are averaged over five
seeds. Reasoning:
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Classifiers:** presence-vs-background. Random Forest is the main
classifier and Logistic Regression is reported as a second one. Why:
[`thesis/notes.md`](../thesis/notes.md#rq2-curva-por-fonte).

**Result (TESSERA, 2021–2025 presences; not yet confirmed by the
supervisor):** the answer depends on the classifier and on the test
presences. On the pooled test set, Random Forest gains about 0.005
ROC-AUC with the first 10% to 20% of expert polygons and no more after
(0.902 at 0%, 0.906 at 90%); Logistic Regression gains 0.031. On
expert presences alone, the citizen-science-only Random Forest reaches
0.976, against 0.994 for the expert-only model. The pooled drop at
100% (0.854) comes from the citizen-science test presences, which
likely share the sampling bias of the training data.

**Reading:** the citizen-science-only model ranks the sites mapped by
experts well. That may reflect expert presences that are easier to
separate from the background (55.0% of expert pixels fall in the COS
2023 "Florestas de acácias" class, against 17.9% of citizen-science
presences), not that the two sources are equivalent. The independent
units are polygons and 10 km blocks, and seeds reuse blocks, so
agreement between seeds is not independent evidence.

Values per level, paired differences, the Boyce index and caveats:
[`thesis/notes.md`](../thesis/notes.md#simplificacao-desenho-2026-11-13);
notebook
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb);
files in `results/rq2_per_source_check/`.

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
literature precedent checked yet. Random Forest: Domingo et al. (2023)
for *A. dealbata* presence/absence; Yang et al. (2026) on embeddings;
Ball et al. (2026) include it as a baseline, below a small neural
network and well above Logistic Regression; in Mouta et al. (2021) it
is one of eight fused classifiers.

**Expert reference labels (adopted):** *A. dealbata* polygons sent by
the supervisor; provenance and counts in
[`data/README.md`](../data/README.md#acacia-dealbata-expert-reference-polygons).

- In the Coimbra district: 1 849 polygons with `classifica = 1`
  (244 ha); 54% fall in a COS 2023 "Florestas de acácias" polygon,
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

### RQ3 — Foundation models vs. conventional features

*Question and design are mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#reformulacao-quatro-perguntas)).*

**Question:** To what extent do TESSERA embeddings improve
*A. dealbata* mapping over Sentinel-2 features when trained on cleaned
citizen-science data, with all observations and with few?

**Hypotheses:**

- H₀a: no performance difference between TESSERA and Sentinel-2
  models, at either data level. H₁a: the TESSERA model performs
  better, with a larger difference at the small data level.
  *Compared:* TESSERA against Sentinel-2 at each data level.
- H₀b: the near–far difference of
  [RQ4](#rq4--transferability-away-from-the-sampled-area) is the same
  for TESSERA and Sentinel-2. H₁b: it differs — a larger drop for
  TESSERA means it amplifies the effect of spatial sampling
  concentration, a smaller one that it mitigates it. No mechanism is
  assumed: TESSERA embeddings are computed per pixel and do not encode
  the surrounding landscape (Feng et al., 2026). *Compared:* the
  near–far difference of one representation against the other's.

**Design:**

- **Only the representation changes.** Same Random Forest, test set,
  background pool, 10 km blocks and five seeds as RQ2; all
  representations come from the same reference year.
- **Two data levels:** all 2 465 presences and the random subsample of
  150 used in RQ1.
- **Away from the sampled area:** the RQ4 experiment repeated with
  Sentinel-2 features.
- **Cleaned data only.** Whether embeddings compensate for label noise
  is not tested.
- **Status: not run.** The Sentinel-2 arm is on hold (see
  [Foundation Model Use](#foundation-model-use-adopted)); its feature
  set is decided, see [`methodology.md`](methodology.md#baseline).

**Risks:**

- The Sentinel-2 extraction may stay too costly to run.
- With all observations the models may be too close to the ceiling of
  the metrics to be separated.

**Grounded in:** the representation comparison follows Ball et al.
(2026), whose conventional arm combines Sentinel-1 and Sentinel-2; not
yet tested for invasive plants with citizen-science labels. Silva &
Gonçalves (2026) is a Portuguese case where the Sentinel-2 baseline
beat TESSERA. No source read for the choice of 150 presences as the
small level. H₀b is motivated by Yang et al. (2026), where
embedding-based models lost accuracy in another region (with no
conventional baseline in that test), and Ratsakatika et al. (2026),
where the TESSERA advantage over Sentinel features narrowed under a
10 km buffer without reversing; no work read shows embeddings
transferring worse than conventional features.

### RQ4 — Transferability away from the sampled area

*The supervisor approved a question on spatial sampling concentration;
this wording and design are mine, to confirm with him
([`thesis/notes.md`](../thesis/notes.md#simplificacao-desenho-2026-11-13)).*

**Question:** To what extent does the performance of the
citizen-science-trained model drop from locations near the sampled
area to locations far from it?

**Hypotheses:** H₀: no difference in performance between near and far
locations. H₁: performance is lower far from the sampled area.
*Compared:* far against near expert polygons. What the five seeds vary
is fixed with the design, before the experiment runs.

The experiment shows the outcome, not the mechanism.

**Design:**

- **Starting point:** one observer made 90% of the 2 465 presences,
  and their points occupy 18 of 42 blocks of 10 km. That is
  concentration; whether it harms the model is what is measured.
- **Experiment:** train on citizen science with TESSERA and evaluate
  on the expert polygons (independent reference), near vs. far from
  the nearest training point in geographic distance. 1 643 polygons
  lie within 1 km and 429 farther, in the same source file.
- **Product:** a feature-space dissimilarity map (area of
  applicability) as a confidence layer for the final map.
- **Background:** the uniform-random pool shared with RQ2.

**Risks:**

- Far polygons are 20–40 times larger than near ones, so near and far
  differ in patch size as well as distance.
- Large patches are easy to detect, so performance may be high both
  near and far and show nothing.

**Grounded in:** clustering of citizen-science records in a few
places: Cambridge TESSERA group. The dissimilarity map follows Meyer &
Pebesma (2021), tested there on regression only, so its use with a
classifier on embeddings is an extension. No precedent found for
citizen science concentrated in one observer.

## Shared Design (RQ1–RQ4)

### Prediction Task (adopted)

**Pixel-level classification trained on points, applied
wall-to-wall.** The classifier is trained on the 10 m pixel at each
observation (Sentinel-2 features or foundation-model embedding), then
applied to every pixel of the study area. The task is binary, *Acacia*
presence vs. background; the *Acacia* map is the predicted probability
per pixel.

**Grounded in:** Brown et al. (2025) — findings in `literature.md`.

**Segmentation mask:** whether the label of each observation is
extended to the patch around it is tested in
[RQ1](#rq1--from-point-observations-to-reference-data). The task stays pixel
classification; the mask changes how many pixels around each
observation count as *Acacia* training data.

Grid-cell presence/absence is not the training unit: pixel predictions
may later be aggregated to cells for evaluation.

### Reference-Data Pipeline (proposed)

Answers the proposal's first objective. The steps that turn
iNaturalist points into labelled pixels are treated as a
**methodological contribution**: each step is documented, counts are
reported, and its effect is measured.

| Step | Status | Notes | Grounded in |
|---|---|---|---|
| 1. Remove obscured coordinates | Done | 43 presences removed | iNaturalist geoprivacy randomises these coordinates (platform documentation); Brown et al. (2025) and Gillespie et al. (2024) filter on location quality explicitly |
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

**Effect of the filters:** RQ1 compares training with and without
the quality filters (steps 1 to 3), as two conditions.

**Cumulative ablation (optional):** run the RQ2 setup after adding
each step and report the change in performance (adapted from the
one-factor ablations of Ball et al., 2026). Not a committed
deliverable: the methodological contribution rests on the documented,
justified pipeline above and on RQ1 (see
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
  the representation (RQ3).

**Grounded in:** Ball et al. (2026); Yang et al. (2026); Brown et al.
(2025) — all used frozen embeddings with a light classifier on top;
Feng et al. (2026) for fine-tuning; findings in `literature.md`.

**Phasing (supervisor): TESSERA first, Sentinel-2 after.** The RQ2
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
