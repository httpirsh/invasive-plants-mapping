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
| Obj. 1 / work plan 3 — transform point observations into usable EO reference data, accounting for uncertainty and quality | [Reference-Data Pipeline](#reference-data-pipeline-proposed): a measured methodological contribution, not just preprocessing |
| Obj. 2 — use foundation models to compensate for limited, noisy citizen-science data | RQ1, RQ2 |
| Obj. 3 — assess to what extent citizen science supports accurate, species-level mapping | RQ1 (comparison with expert reference data), [Species Scope](#species-scope-proposed) |
| Work plan 4 — fine-tune foundation models; analyse accuracy, limitations, transferability | [Foundation Model Use](#foundation-model-use-adopted) (frozen embeddings, a justified deviation); RQ3 (performance away from the sampled area) |

## Main Question and Objectives

*Wording mine, to confirm with the supervisor
([`thesis/notes.md`](../thesis/notes.md#formulacao-pergunta-objetivos-hipoteses)).*

**Main question:** To what extent do Earth Observation foundation
models, trained with citizen-science observations, allow *Acacia
dealbata* to be mapped with less dependence on expert reference data
than conventional satellite features?

**General objective:** to assess under which conditions of quantity,
source and spatial distribution of reference data foundation models
are useful for mapping *A. dealbata* from citizen science.

**Specific objectives:**

1. To build and document the process that turns citizen-science point
   observations into reference data for satellite classification.
2. To compare the performance of TESSERA-based and Sentinel-2-based
   models, and to measure the gain from adding expert data from 0% to
   100% (RQ1).
3. To measure how performance changes as observations are reduced,
   removing those most distant from 2023 first (RQ2).
4. To measure the difference in performance between locations near
   and far from the sampled area, for both representations (RQ3).
5. To produce the *A. dealbata* map of the study area, with a
   confidence map.

**Common context:** *Acacia dealbata*, Coimbra district, 2023 imagery,
research-grade iNaturalist observations, TESSERA vs. Sentinel-2
features; performance measured with ROC-AUC and the continuous Boyce
index under 10 km spatial block holdout.

**Hypotheses** are stated under each question as a null (H₀) and an
alternative (H₁). They are working hypotheses, not formal statistical
tests (five spatial splits); the decision criterion for each is
written before the experiment runs.

## Secondary Questions

RQ1 is the prerequisite and core deliverable; RQ2 and RQ3 build on it.

### Priority and scope

The questions are ordered by priority, and each stage is a complete
result on its own:

| Scenario | Delivers | Answers |
|---|---|---|
| RQ1 only | Reference-data pipeline + Sentinel-2 vs. TESSERA, along the expert effort-reduction curve | Proposal objectives 1 and 3, part of 2 — already a thesis |
| RQ1 + RQ2 | The above + behaviour under data reduction | Objective 2 in full. Low extra cost: same pipeline, model and test set |
| RQ1 + RQ2 + RQ3 | The above + performance away from the sampled area, and a confidence map | Transferability (work plan 4). Most expensive and most exposed to time |

Scope is reassessed as experiments progress.

### RQ1 — Foundation models vs. conventional approaches

**Question:** To what extent do TESSERA representations improve
*A. dealbata* mapping over Sentinel-2 features when trained on citizen
science, and how much performance is gained by progressively adding
expert data?

**Hypotheses:**

- H₀a: no performance difference between TESSERA and Sentinel-2
  models. H₁a: the TESSERA model performs better.
- H₀b: adding expert data does not change performance. H₁b:
  performance increases with the fraction of expert data. (H₁b was
  written after the TESSERA curve had already come out flat,
  compatible with H₀b.)

**Design (supervisor):** an effort-reduction curve. Expert data are
added on top of a fixed citizen-science base, from 0% to 100% in
10-point steps. The mixing unit is the polygon, sampled in a nested
order; one spatial test set per seed is reused at every level and
always contains both sources; results are averaged over five seeds.
The whole curve runs once per representation, and all representations
come from the same reference year, so only the representation changes
between compared models. Reasoning:
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Method:** presence-vs-background with Random Forest; Logistic
Regression as a cheap reported baseline. Why:
[`thesis/notes.md`](../thesis/notes.md#classificador-presença-vs-fundo-ciência-cidadã-random-forest-por-agora).

**Result so far (TESSERA; not yet confirmed by the supervisor):**
Random Forest and Logistic Regression are flat from 0% to 90% expert
data and drop only at 100%, when citizen science is fully replaced.
The result holds under a harder, forest-only background. Habitat
concentration explains it: expert polygons sit mostly inside COS's own
"acacia forest" class, while citizen science spans far more habitats.
The Sentinel-2 arm has not run yet (see
[Foundation Model Use](#foundation-model-use-adopted)). Numbers and
caveats:
[`thesis/notes.md`](../thesis/notes.md#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos);
notebooks in `notebooks/07_foundation_models/`.

**Grounded in:** the representation comparison follows Ball et al.
(2026) and the atoll ecosystem study (2026); not yet tested for
invasive plants with citizen-science labels. Training the same model
on citizen-science vs. expert data comes from Dimson et al. (2023),
including that the two sources have opposite biases, so the expert
end of the curve is biased differently, not bias-free. The curve
design itself has no literature precedent checked yet. Random Forest:
Ball et al. (2026); Yang et al. (2026); Mouta et al. (2021); Domingo
et al. (2023); Eskandari et al. (2025).

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
  Both arms share the uniform-random background pool, step 7 of the
  [Reference-Data Pipeline](#reference-data-pipeline-proposed).
- **Independent of citizen science:** iNaturalist did not influence
  the collection (supervisor).
- **Locations overlap with citizen science:** all 22 cleaned
  iNaturalist presences inside a polygon, and 93% of the 162 within
  50 m, are the dominant observer's. Experts and that observer visited
  the same places, so training and test must be split by spatial
  blocks, and both sources inherit a similar spatial coverage.
- **Open:** how the sites were chosen.

### RQ2 — Data efficiency

**Question:** What is the effect of reducing citizen-science
observations, removing those most distant from 2023 first, on the
performance of TESSERA models compared with Sentinel-2 models?

**Hypotheses:** H₀: the performance difference between TESSERA and
Sentinel-2 stays the same as observations are reduced. H₁: the TESSERA
model loses less performance than the Sentinel-2 model.

**Why this design:** all observations are treated as 2023 (see
[Temporal Design](#temporal-design-adopted)), so observations far from
2023 are the most likely to no longer match the 2023 imagery (cleared,
burned, built over, or not yet established). Removing them first
reduces quantity in a documented, realistic way.

- **Filter: recency, defined as distance to 2023** (mine, not
  confirmed by the supervisor). Observations are removed starting with
  those most distant in time from 2023, in either direction;
  2024–2026 observations (1 009 presences) count as recent as
  symmetrically close ones before 2023. It is the only RQ2-specific
  filter: quality grade, positional accuracy and the disturbance
  filter are fixed pipeline steps. Why:
  [`thesis/notes.md`](../thesis/notes.md#rq2-recência-distância-a-2023).
- **Levels:** keep the N observations closest to 2023, for decreasing
  N. By year alone the levels are coarse — 2019 onwards retains 99.4%
  of the 3 000 presences, 2021 onwards 85.5%, 2023 onwards 36.6% — so
  levels are set by date. Still to fix from the real counts.
- **Limitation:** there is no random-removal baseline, so each level
  changes quantity *and* composition (age, observers, places) at once;
  RQ2 measures their joint effect. Observer A's share stays near
  88–89% across retention levels and is reported at each level
  (`notebooks/02_citizen_science/acacia_observations.ipynb`).
- The final map always uses all data; RQ2 is a test, not a cleaning
  step.
- **Grounded in:** training with decreasing fractions of labels
  follows Ball et al. (2026, random reduction). Removing the
  observations furthest from the imagery year first is this thesis's
  own step, motivated by the same paper's cross-year result.

### RQ3 — Spatial sampling concentration

*Question approved by the supervisor; this wording and design are
mine, to confirm with him
([`thesis/notes.md`](../thesis/notes.md#rq3-proposta-redesenho-diagnostico-primeiro)).*

**Question:** Do foundation models amplify or mitigate the effect of
the spatial concentration of citizen-science observations, compared
with conventional features, when the model is evaluated away from
where sampling took place?

**Hypotheses:**

- H₀: the near–far performance difference is the same for TESSERA and
  Sentinel-2. H₁: it differs — a larger drop for TESSERA means
  amplify (embeddings carry landscape context, so the model learns the
  sampled area), a smaller one means mitigate (embeddings describe the
  plant better).
- Observer comparison — H₀: at equal sample size, no difference
  between training on the dedicated observer and on the others. H₁:
  performance differs away from the sampled area.

The experiments show the outcome, not the mechanism.

**Design:**

- **Starting point:** one observer made 88% of the 3 000 presences,
  and their points occupy 18 of 43 blocks of 10 km. That is
  concentration; whether it harms the model is what is measured.
- **Experiment 1:** train on citizen science and evaluate on the
  expert polygons (independent reference), near vs. far from the
  nearest training point in geographic distance, for both
  representations. 1 680 polygons lie within 1 km and 392 farther, in
  the same source file; 398 more elsewhere in the country are an
  optional extension.
- **Experiment 2:** one dedicated observer vs. many occasional ones at
  equal sample size (353 points each).
- **Product:** a feature-space dissimilarity map (area of
  applicability) as a confidence layer for the final map.
- **Correction:** spatial thinning runs only if experiment 1 finds
  degradation.
- **Background:** the uniform-random pool shared with RQ1.
- **Main risk:** far polygons are 20–40 times larger than near ones.

**Grounded in:** the amplify/mitigate question comes from work
reporting weaker spatial transfer of embeddings — Zhu et al. (2026),
Yang et al. (2026), Ratsakatika et al. (2026) — and the clustering
reported by the Cambridge TESSERA group. The dissimilarity map follows
Meyer & Pebesma (2021). No precedent found for citizen science
concentrated in one observer.

## Shared Design (RQ1–RQ3)

### Prediction Task (adopted)

**Pixel-level classification trained on points, applied
wall-to-wall.** The classifier is trained on the 10 m pixel at each
observation (Sentinel-2 features or foundation-model embedding), then
applied to every pixel of the study area. The task is binary, *Acacia*
presence vs. background; the *Acacia* map is the predicted probability
per pixel.

**Grounded in:** Brown et al. (2025) and the Cambridge TESSERA group —
findings in `literature.md`.

**Segmentation mask (supervisor: central, try several approaches).**
A rule to consider the nearest vegetation area to each observation;
the concrete rule is mine to define. Working reading (mine, to confirm
with him): extend the point's label to the patch around it. The task
stays pixel classification; the mask changes how many pixels around
each observation count as *Acacia* training data.

Three candidates, each with uneven literature support (summaries in
[`literature.md`](literature.md#weak-supervision-from-point-labels)):

- **Region growing** on TESSERA embedding similarity from the observed
  pixel, with a maximum radius. Thinnest anchor: no remote-sensing
  precedent found for growing on embedding similarity; Zhang et al.
  (2025) grounds seeded region growing on a satellite product in
  general.
- **Superpixels** on TESSERA embeddings, following the idea of Rivier
  et al. (2024). Raine et al. (2022) supports computing superpixels on
  learned features rather than raw pixels.
- **COS 2023 "Florestas de acácias" polygons** where the point falls
  inside one (about 17% of 2021–2025 presences). No direct precedent
  found for extending a label through an existing auxiliary map.

Risks: the mask may spread into similar non-*Acacia* vegetation, and
large patches give many more pixels than isolated trees. No paper
found combines point-to-patch propagation with sparse citizen-science
points and frozen embeddings, so that combination is a possible
contribution, not an applied practice.

Choosing a rule and comparing with and without the mask are still to
do. Tests so far and reasoning:
[`thesis/notes.md`](../thesis/notes.md#máscara-de-segmentação-testar-várias-abordagens).

Grid-cell presence/absence is not the training unit: pixel predictions
may later be aggregated to cells for evaluation.

### Reference-Data Pipeline (proposed)

Answers the proposal's first objective. The steps that turn
iNaturalist points into labelled pixels are treated as a
**methodological contribution**: each step is documented, counts are
reported, and its effect is measured.

| Step | Status | Notes | Grounded in |
|---|---|---|---|
| 1. Remove obscured coordinates | Done | 43 presences removed | iNaturalist geoprivacy randomises these coordinates (platform documentation); research-grade-only data in Gillespie et al. (2024) and Brown et al. (2025) also implies location-quality filtering |
| 2. Positional accuracy | Adopted | Drop known accuracy > 30 m; keep missing values, marked `accuracy_missing`. Presences 3 441 → 3 276. Why 30 m (the COS test): [`thesis/notes.md`](../thesis/notes.md#precisão-da-localização-tirar-acima-de-30-m-manter-as-sem-valor) | Ball et al. (2026) |
| 3. Quality grade | Adopted | Research grade only. Presences 5 242 → 3 441. Why: [`thesis/notes.md`](../thesis/notes.md#só-observações-research-nos-dois-lados) | Gillespie et al. (2024); Brown et al. (2025) |
| 4. Temporal design | Adopted | All observations treated as 2023, see [Temporal Design](#temporal-design-adopted) | See that section |
| 5. Disturbance filter | Proposed (fixed) | Burned between observation and 2023 (ICNF 1975–2025): 6 *A. dealbata* presences (0.2%) | Riveiro et al. (2025): burned stands regrow, pixel no longer matches the label |
| 6. Label purity | Checked, no large-scale problem found | Expert-polygon agreement (limited power) and embedding-outlier detection found no evidence that presences are frequently off-target. See [`thesis/notes.md`](../thesis/notes.md#diagnosticos-curva-plana) | Ball et al. (2026) |
| 7. Negative/background | Adopted | Uniform-random points, 50 m buffer around known presences; not yet confirmed by the supervisor. Why: [`thesis/notes.md`](../thesis/notes.md#rq1-fundo-uniforme-nao-cos) | Empirical (forest-only robustness check). Phillips et al. (2009) supports the opposite choice, a target-group background |
| 8. Same pixel | Adopted | Pixel = 10 m cell in EPSG:32629. One presence per pixel, closest to 2023 (3 276 → 3 000). Why: [`thesis/notes.md`](../thesis/notes.md#uma-observação-por-píxel-nos-conflitos-fica-a-presença) | Karasiak et al. (2022) |
| 9. Observer balancing | Adopted | The main model uses all of Observer A's observations (88% of the 3 000 presences). Why: [`thesis/notes.md`](../thesis/notes.md#observer-a-todas-as-observações-no-modelo-principal) | Observer clustering (Cambridge TESSERA group); Phillips et al. (2009) |

**Cumulative ablation (optional):** run the RQ1 setup after adding
each step and report the change in performance, so that preprocessing
becomes a result (idea from Ball et al., 2026). Not a committed
deliverable: the methodological contribution rests on the documented,
justified pipeline above (see
[`literature.md`](literature.md#contribution)).

### Foundation Model Use (adopted)

**Frozen embeddings + light classifiers**, not fine-tuning. This is a
deliberate deviation from the proposal's "fine-tune EO foundation
models" and must be stated as such.

Reasons:

- AlphaEarth is released only as embeddings; it cannot be fine-tuned.
- TESSERA code is open, but model weights must be requested.
- With few, noisy labels, fine-tuning risks fitting the noise.
- The same classifier on every representation isolates the effect of
  the representation (RQ1).

**Grounded in:** Ball et al. (2026); Yang et al. (2026); Brown et al.
(2025) — all used frozen embeddings with a light classifier on top;
findings in `literature.md`.

**Phasing (supervisor): TESSERA first, Sentinel-2 after.** The RQ1
curve ran first with TESSERA embeddings. The Sentinel-2 arm is on
hold: extracting it at the labelled points turned out to cost about as
much as the full raster (see
[`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)).
Its feature set is already decided, see
[`methodology.md`](methodology.md#baseline).

### Temporal Design (adopted)

Time is **held constant, not studied**:

1. **Reference year 2023** for all imagery and auxiliary products
   (Sentinel-2 features, TESSERA embeddings, COS/OrtoSat).
2. **All iNaturalist observations (1992–2026) treated as 2023.**

Data constraints:

| Source | Temporal availability |
|---|---|
| OrtoSat / COS | 2023 only |
| TESSERA | One embedding per tile per year, 2017–2025 |
| Sentinel-2 | Any date from 2015/2017 |
| Citizen science (*Acacia*, Coimbra pilot) | 1992–2026; 98.8% from 2019 onwards; 43% from 2021, 98% of those from one observer |

Assumption: *Acacia* stands persist for years, so an observation is
evidence of presence in 2023 unless the site was disturbed. The risk
grows with the distance in time from 2023; the RQ2 filter removes
the most distant observations first.

Why 2023 and not a later year: 728 *A. dealbata* presences (24.3%) lie in areas
burned in 2025; 2023 imagery still shows the observed vegetation.

Safeguard: **disturbance filter**, step 5 of the
[Reference-Data Pipeline](#reference-data-pipeline-proposed).

**Grounded in:** a single reference year follows Ball et al. (2026,
cross-year degradation — see [RQ2](#rq2--data-efficiency)) and the
atoll ecosystem study (2026, single year of AlphaEarth). Persistence
follows Riveiro et al. (2025). Treating many years as one reference
year follows from both plus Ball et al. (2026)'s conclusion that the
bottleneck is reference-data availability: using all observations
keeps the most data at a fixed year; the RQ2 filter then tests the
cost of those furthest from it. Findings: `literature.md`.

### Species Scope (proposed)

The proposal asks for **species-level** mapping of a limited number of
representative species. Observations (all years, non-obscured):
*A. dealbata* 5 241, *A. melanoxylon* 1 884, *A. longifolia* 512.

**Proposed: *A. dealbata* as the target.** Other *Acacia* species are
left out of training. Why: [`thesis/notes.md`](../thesis/notes.md#só-acacia-dealbata).

**Grounded in:** mapping *A. dealbata* alone follows Domingo et al.
(2023, Galicia) and Martins et al. (2016, central-eastern Portugal);
Mouta et al. (2021) mapped *A. longifolia* alone.
