# Research Questions

| Item | Status |
|---|---|
| Main question | Adopted |
| RQ1 | Adopted (approved by the supervisor, as the thesis's core); redesigned (supervisor, in person) as an effort-reduction curve — see [RQ1](#rq1--foundation-models-vs-conventional-approaches) |
| RQ3 | Adopted (approved by the supervisor) |
| RQ2 (recency-based filter, no random removal) | Adopted |
| Prediction task | Adopted; segmentation mask: direction set (supervisor), rule to define |
| Reference-data pipeline (proposal objective 1) | Proposed |
| Temporal design: all iNaturalist observations treated as 2023 | Adopted |
| Other plants as classes (multiclass) | **Superseded** (supervisor, in person): multiclass dropped for both models; RQ1's background is a uniform-random point pool, not other-plant data — see [RQ1](#rq1--foundation-models-vs-conventional-approaches) and [Other Plants as Classes](#other-plants-as-classes-adopted-direction) |
| Expert reference data: *A. dealbata* polygons from the supervisor | Adopted; year 2023 (confirmed) |
| Frozen embeddings instead of fine-tuning | Adopted (deviation from proposal); phase 1 (TESSERA only, supervisor) done, phase 2 (Sentinel-2) deferred again (extraction cost higher than expected) |
| Species scope | Proposed: *A. dealbata*, other *Acacia* left out |
| Experiments per RQ | Candidate sketches |

How these questions follow from the literature: [`literature.md`](literature.md).
Methodological questions still open: [`methodology.md`](methodology.md).

Each decision has a **Grounded in** note naming the work that already
used it and from which the idea comes. Where no paper used it directly,
the note names the work that motivates it.

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
| Work plan 4 — fine-tune foundation models; analyse accuracy, limitations, transferability | [Foundation Model Use](#foundation-model-use-adopted) (frozen embeddings, a justified deviation); RQ3 (transferability) |

## Position in the Literature

What has already been done, the gap, and the contribution this thesis
makes: [`literature.md`](literature.md#what-has-already-been-done).

## Main Question

How robust and data-efficient are Earth Observation foundation models
for invasive plant mapping when trained with citizen-science reference
data?

**Hypothesis** (to test, not assume): EO foundation models may give
more data-efficient representations, but their advantage may be
limited by the quality, quantity and spatial distribution of
citizen-science data. The thesis asks *under what conditions* they are
useful, not only whether they are better.

## Secondary Questions

RQ1 is the prerequisite and core deliverable; RQ2 and RQ3 build on it.

### Priority and scope

The questions are deliberately ambitious; reaching RQ3 assumes ideal
conditions. They are ordered by priority, and each stage is a complete
result on its own:

| Scenario | Delivers | Answers |
|---|---|---|
| RQ1 only | Reference-data pipeline + Sentinel-2 vs. TESSERA vs. expert upper bound | Proposal objectives 1 and 3, part of 2 — already a thesis |
| RQ1 + RQ2 | The above + behaviour under data reduction | Objective 2 in full. Low extra cost: same pipeline, model and test set |
| RQ1 + RQ2 + RQ3 | The above + amplify/mitigate under spatial bias | Transferability (work plan 4). Most expensive: needs distinct regions, road/trail layers and the observer experiments; most exposed to time |

Scope is reassessed as experiments progress.

### RQ1 — Foundation models vs. conventional approaches

To what extent do Earth Observation foundation-model representations
improve invasive plant mapping over conventional spectral-temporal
satellite features when trained on citizen-science labels, and how
much performance is gained by progressively adding costlier expert
reference data on top of it?

**Fit with the proposal:** answers objective 3 (*to what extent
citizen science supports accurate mapping*) and objective 1 (*reduce
dependency on costly reference data*). Comparing representations shows
how good foundation models are; the effort-reduction curve shows how
much expert data is actually needed, and where the balance between
performance and field-collection effort lies.

- A question of degree, not yes/no.
- All representations come from the same reference year, so only the
  representation changes between compared models.
- **Grounded in:** the representation comparison follows Ball et al.
  (2026) and the atoll ecosystem study (2026); not yet tested for
  invasive plants with citizen-science labels. Findings:
  `literature.md`.
- **Effort-reduction curve grounded in:** Dimson et al. (2023) — the
  idea of training the same model on citizen-science vs. expert data
  comes from there, including that the two sources have opposite
  biases, so the expert end of the curve is biased differently, not
  bias-free. Finding: `literature.md`. The curve design itself has no
  literature precedent checked yet. Full decision and open points:
  [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Redesigned (supervisor, in person):** replaces the
earlier fixed "upper bound" design with an effort-reduction curve
(0–100% expert data mixed into the citizen-science base, 10-point
steps, polygon-level nested mixing, one fixed spatial test set per
seed reused at every level). Multiclass dropped for both models (see
[Other Plants as Classes](#other-plants-as-classes-adopted-direction)).

**Method:** true one-class/novelty detection and
presence-vs-background classification run in parallel, not staged —
no presence-only evaluation method found avoids needing background
data anyway. **One-class SVM** chosen over Isolation Forest, **Random
Forest** chosen over Logistic Regression, both by direct comparison on
the citizen-science arm; both rankings confirmed on the expert arm
Full comparison and numbers:
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo),
[`one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb),
[`presence_background_citizen_science.ipynb`](../notebooks/07_foundation_models/presence_background_citizen_science.ipynb),
[`expert_arm_classifiers.ipynb`](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb).

**Status (not yet confirmed by the supervisor):** full
curve run on both arms. Random Forest and Logistic Regression are
essentially flat across the whole curve, dropping only at 100% expert
(no citizen science); One-Class SVM is the only one that improves as
expert data is added, but stays below the other two throughout. Holds
under a harder (forest-only) background. Two follow-up checks ruled
out pixel redundancy and citizen-science label/GPS noise as
explanations — habitat concentration (expert polygons sit mostly
inside COS's own "acacia forest" class; citizen science spreads across
far more habitats) explains it instead. Full numbers, caveats (ceiling
effects, single background design) and the diagnostic notebooks:
[`thesis/notes.md`](../thesis/notes.md#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos),
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb),
[`forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb),
[`expert_polygon_redundancy_check.ipynb`](../notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb),
[`expert_polygon_geographic_diversity.ipynb`](../notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb),
[`label_purity_check.ipynb`](../notebooks/07_foundation_models/label_purity_check.ipynb).

Run once per representation (TESSERA done; Sentinel-2 deferred, see
[Foundation Model Use](#foundation-model-use-adopted)), same
classifiers, same held-out spatial test set, at every curve level.

- Candidate classifiers: Random Forest, Logistic Regression, compact
  neural network. **Grounded in:** Random Forest — Ball et al. (2026);
  Yang et al. (2026); Mouta et al. (2021); Domingo et al. (2023);
  Eskandari et al. (2025). Compact neural network — Ball et al.
  (2026). Findings: `literature.md`.
- **Expert reference labels (adopted):** *A. dealbata* polygons
  sent by the supervisor. Provenance, attributes and counts:
  [`data/README.md`](../data/README.md#acacia-dealbata-expert-reference-polygons).
  In the Coimbra district: 1 849 polygons with `classifica = 1`
  (244 ha), all in Sentinel-2 tile TNE; 54% fall in a COS 2023
  "Florestas de acácias" polygon, most of the rest in pine, eucalyptus
  and other forest.
  - **Species:** *A. dealbata* only, the proposed target (see
    [Species Scope](#species-scope-proposed)).
  - **Clustered:** the district polygons fall in only **18** cells of
    10 km (reconciled), so few independent spatial blocks
    are available to split training and test. An earlier "15" figure
    for the same polygons was a coordinate-system artefact, not a
    smaller polygon set or a split bug — see
    [`notebooks/07_foundation_models/expert_arm_classifiers.ipynb`](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb)
    and `thesis/notes.md`.
  - **Background:** `classifica = 0` polygons not used as negatives
    (supervisor — why:
    [`thesis/notes.md`](../thesis/notes.md#usar-os-dados-de-especialistas-com-limpeza)).
    Shares the uniform-random background pool with the citizen-science
    arm — see step 7 of the [Reference-Data
    Pipeline](#reference-data-pipeline-proposed).
  - **Cleaning and year/method:** see the `data/README.md` entry
    linked above.
  - **Labels independent of citizen science:** iNaturalist did not
    influence the collection (supervisor).
  - **Locations overlap with citizen science (design constraint):**
    all 22 cleaned iNaturalist *A. dealbata* presences inside a
    polygon, and 93% of the 162 within 50 m, are the dominant
    observer's. Experts and that observer
    visited the same places. Consequences: tested on these polygons,
    the citizen-science model would be evaluated where it was trained
    (inflated score), so training and test must be split by spatial
    blocks (18 blocks of 10 km); as the upper bound, both models learn
    from nearly the same areas, so only the label source changes, but
    both inherit the same spatial bias.
  - **Open:** how the sites were chosen.

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as citizen-science reference data are reduced
by a filter that keeps the most recent and most reliable observations?

**Fit with the proposal:** answers objective 2 (*use foundation models
to compensate for limited citizen-science data*).

**Why this design:** all observations are treated as 2023 (see
[Temporal Design](#temporal-design-adopted)), so older observations
are the most likely to no longer match the 2023 imagery (cleared,
burned, built over). Removing them first reduces quantity in a
documented, realistic way, and reports *which* observations are
removed and *why*.

- **Filter:** observations ordered by date, oldest removed first,
  combined with the other candidate criteria (quality grade,
  positional accuracy). Exact combination open.
- **Levels:** keep the most recent N observations, for decreasing N.
  By year alone the levels are coarse — keeping 2019 onwards retains
  99.4% of presences, 2021 onwards 85.5%, 2023 onwards 36.6% (3 000
  cleaned *A. dealbata* presences) — so levels are set by date, not
  year. Fix levels after checking the real counts.
- **Open:** whether observations after 2023 (2024–2026: 1 009
  presences) count as "more recent", or whether recency is distance
  to 2023. **Not just wording (checked):** the two readings
  give different observer compositions at the same retention level —
  see the limitation below.
- **Limitation (checked, see
  `notebooks/02_citizen_science/acacia_observations.ipynb`):** without
  a random-removal baseline, each level changes quantity *and*
  composition (age, observers, places) at once; RQ2 measures their
  joint effect. Checked against Observer A (88.2% of presences, 98% of
  the RQ3 bias case): oldest-removed-first keeps Observer A's share
  near 88% at coarse cuts but drops it to 73.7% at the most aggressive
  one (keep ≥2023, 36.6% kept), because the oldest removed
  observations are themselves 93–97% Observer A's; distance-to-2023
  stays flatter (~88–89% at the same retention fractions). The
  confound is real but not one-directional, and the two "recent"
  readings disagree with each other on it. Whichever is chosen,
  report Observer A's share at each kept level alongside the RQ2
  result. My own check, not grounded in literature.
- The final map always uses all data; RQ2 is a test, not a cleaning
  step.
- The disturbance filter is a fixed preprocessing step (see
  [Reference-Data Pipeline](#reference-data-pipeline-proposed)), not
  the RQ2 filter.
- **Grounded in:** training with decreasing fractions of labels
  follows Ball et al. (2026, random reduction; finding in
  `literature.md`). Removing the oldest observations first instead is
  this thesis's own step, motivated by the same paper's cross-year
  result (see [Temporal Design](#temporal-design-adopted)): the older
  an observation, the larger its mismatch with the 2023 imagery.

### RQ3 — Spatial sampling bias

Do EO foundation-model representations amplify or mitigate the effect
of spatial sampling bias in citizen-science observations, compared
with conventional satellite features, when evaluated across
geographically distinct regions?

**Fit with the proposal:** answers objective 2 (*noisy*, biased
citizen-science data) and the transferability analysis in work
plan 4.

**Why this question:** the effect of spatial bias on species
distribution models is already documented; whether foundation models
react to it *differently* is untested. Two competing hypotheses:

- **Amplify:** embeddings encode context (roads, settlements,
  disturbance), so a model can learn observer accessibility more
  easily than from spectral bands.
- **Mitigate:** richer representations separate *Acacia* from its
  surroundings better, so the model relies less on where observers
  went.

Design notes:

- Evaluated with geographically separated test regions (see
  [Validation](methodology.md#validation)).
- A single reference year keeps observation year from correlating
  with geography.
- The background affects the bias being measured: the other-plant
  background pool shares the presences' observers and places (same
  citizen-science pipeline), so it partly absorbs their spatial bias
  rather than exposing it; a uniform-random background does not share
  that bias, so it should expose more of it. Results must state which
  background was used.
- **Reviewed (mine; reasonable proposal, not yet confirmed
  by the supervisor):** the candidate experiment — other-plant
  background pool vs. random background — does not actually depend on
  the dropped multiclass design; it only needs the other-plant pool to
  exist as *a* background source, which it still does (group pipeline,
  kept for this purpose — see [Other Plants as
  Background](#other-plants-as-classes-adopted-direction)). What
  changed is which background RQ1 adopted as its main, shared one:
  the background actually built and used so far for the
  presence-vs-background classifier and the one-class evaluation is
  **uniform-random points** (not yet confirmed by the supervisor as
  final — see [RQ1](#rq1--foundation-models-vs-conventional-approaches)
  and [`data/README.md`](../data/README.md)), not the other-plant
  pool. So the two candidate backgrounds map onto the amplify/mitigate
  question directly: random background is the "bias-exposed" condition
  (closer to what RQ3 wants to measure), the other-plant/target-group
  pool is the "bias-corrected" condition (per Phillips et al., 2009).
  Running RQ3 under both and comparing the amplify/mitigate reading is
  still a candidate experiment, now stated independently of multiclass;
  not yet run, and not scheduled ahead of the RQ1 curve.
- **Real bias case — the dominant observer.** One person made 83% of
  all observations (85% in 2021–2025; 98% of the 2021 peak). Candidate
  experiment: train with all observations vs. capped vs. without that
  observer, test on other observers' records and regions.
- **Grounded in:** the bias axes (roads, trails, disturbed areas) come
  from Dimson et al. (2023). The amplify/mitigate question comes from
  work reporting weaker spatial transfer of embeddings: Zhu et al.
  (2026), Yang et al. (2026), the old-growth forest preprint (2026),
  and the clustering reported by the Cambridge TESSERA group. Whether
  bias affects the two representations differently is untested.
  Findings: `literature.md`.
- Spatial thinning and capping the dominant observer are motivated by
  the same Cambridge TESSERA group and Dimson et al. (2023) findings
  above, and by Phillips et al. (2009) — largest bias-correction gains
  where presences are most biased, which applies to a single dominant
  observer.

Experiment — compare training sets: (1) original observations,
(2) spatially thinned, (3) dominant observer capped/removed. Build
bias axes from distance to roads/trails (e.g. OpenStreetMap) and
check they hold in the study area rather than assuming them. Do not
assume bias correction improves performance.

## Shared Design (RQ1–RQ3)

### Prediction Task (adopted)

**Pixel-level classification trained on points, applied
wall-to-wall.** The classifier is trained on the 10 m pixel at each
observation (Sentinel-2 features or foundation-model embedding), then
applied to every pixel of the study area. The task is binary —
*Acacia* presence vs. background — run both as true one-class/novelty
detection and as a presence-vs-background classifier in parallel (see
[RQ1](#rq1--foundation-models-vs-conventional-approaches)); the
*Acacia* map is the predicted probability (or novelty score) per
pixel.

**Grounded in:** Brown et al. (2025) and the Cambridge TESSERA group —
findings in `literature.md`.

- **Segmentation mask (supervisor: central, try several
  approaches; rule to define):** raised when discussing exclusion
  buffers. Decided (supervisor): a rule to consider the nearest
  vegetation area to each observation; the concrete rule is mine to
  define. Read as two things to
  test: (1) move the point to the nearest vegetation when the
  coordinate (where the phone was) falls on a road or building;
  (2) extend the point label to the patch around it, as in the paper
  he recommended. Working on (2) for now (adopted, mine, still to
  confirm explicitly with him — see
  [`thesis/notes.md`](../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens)).
  The supervisor sees this as a central point of the thesis and suggests
  trying several approaches; comparing them can be a result. The task
  stays pixel classification; the mask changes how many pixels around
  each observation count as *Acacia* training data. Using the camera
  direction or close-up vs. landscape photos was dropped (not worth
  it, supervisor). Recommended reading: Rivier et al. (2024, ICIP),
  who propagated sparse point labels to superpixels, "and similar
  works" (supervisor; not read yet beyond the abstract).
  **Candidate methods (to compare):** region growing on TESSERA
  embedding similarity from the observed pixel, with a maximum radius;
  superpixels on Sentinel-2 or embeddings (as in Rivier et al., 2024 —
  see [`literature.md`](literature.md#weak-supervision-from-point-labels)
  for how their propagation rule works and how it differs from our
  setting); COS 2023 "Florestas de acácias" polygons where the point
  falls inside one (about 17% of 2021–2025 presences). Risks: the mask
  may spread into similar non-*Acacia* vegetation (check a sample on
  OrtoSat), and large patches give many more pixels than isolated
  trees (may need balancing). Literature search found
  this is an active technique in weakly-supervised remote-sensing
  segmentation generally, but no paper combines it with sparse
  citizen-science points and frozen foundation-model embeddings as
  proposed here, so that specific combination stays a possible
  contribution, not an applied practice. Gillespie et al. (2024) is
  **not** a precedent for this rule — why, in
  [`literature.md`](literature.md#citizen-science--remote-sensing--plant-mapping).
- **Grid-cell presence/absence — not the training unit:** pixel
  predictions may later be aggregated to cells for evaluation and
  comparison with SDM-style outputs.

### Reference-Data Pipeline (proposed)

Answers the proposal's first objective. The steps that turn
iNaturalist points into labelled pixels are treated as a
**methodological contribution**: each step is documented, counts are
reported, and its effect is measured.

| Step | Status | Notes | Grounded in |
|---|---|---|---|
| 1. Remove obscured coordinates | Done | 43 presences, 9 903 other plants | iNaturalist geoprivacy randomises these coordinates (platform documentation); research-grade-only data in Gillespie et al. (2024) and Brown et al. (2025) also implies location-quality filtering |
| 2. Positional accuracy | Adopted | Drop known accuracy > 30 m; keep missing values, marked `accuracy_missing`. Presences 3 441 → 3 276, other plants 60 630 → 48 125. Why 30 m (the COS test): [`thesis/notes.md`](../thesis/notes.md#precisão-da-localização-tirar-acima-de-30-m-manter-as-sem-valor) | Ball et al. (2026) |
| 3. Quality grade | Adopted | Research grade only, on both sides. Presences 5 242 → 3 441, other plants 110 576 → 60 630. Why: [`thesis/notes.md`](../thesis/notes.md#só-observações-research-nos-dois-lados) | Gillespie et al. (2024); Brown et al. (2025) |
| 4. Temporal design | Adopted | All observations treated as 2023, see [Temporal Design](#temporal-design-adopted) | See that section |
| 5. Disturbance filter | Proposed (fixed) | Burned between observation and 2023 (ICNF 1975–2025): 6 *A. dealbata* presences (0.2%), 125 other plants (0.9%) | Riveiro et al. (2025): burned stands regrow, pixel no longer matches the label |
| 6. Label purity | Checked, no large-scale problem found | Expert-polygon agreement (limited power) and embedding-outlier detection found no evidence citizen-science presences are frequently off-target; see [RQ1](#rq1--foundation-models-vs-conventional-approaches) and `thesis/notes.md` | Ball et al. (2026) |
| 7. Negative/background | Adopted | Uniform-random points, 50 m buffer around known presences, not COS-stratified — not yet confirmed by the supervisor as final. See [RQ1](#rq1--foundation-models-vs-conventional-approaches) and [`data/README.md`](../data/README.md) | Phillips et al. (2009) |
| 8. Same pixel | Adopted | Pixel = 10 m cell in EPSG:32629. One presence per pixel, closest to 2023 (3 276 → 3 000). Conflicts: co-located other plants dropped, presence kept. Other plants: one per pixel, tallest group first, then closest to 2023 (16 720 → 13 554). Why: [`thesis/notes.md`](../thesis/notes.md#uma-observação-por-píxel-nos-conflitos-fica-a-presença) | Karasiak et al. (2022) |
| 9. Other-plant classes | **Superseded** | Multiclass dropped; the cleaned, grouped other-plant dataset is kept only as a candidate background source for the RQ3 amplify/mitigate experiment (not yet run) — see [RQ3](#rq3--spatial-sampling-bias) and [Other Plants as Classes](#other-plants-as-classes-adopted-direction) | FAO LCCS (Di Gregorio & Jansen, 2000); GIFT (Weigelt et al., 2020; Denelle et al., 2023); Decreto-Lei 92/2019, Annex II; EPPO (2024); Ball et al. (2026) |
| 10. Observer balancing | Adopted | Main model: all of Observer A's observations (88% of the 3 000 presences); capping/removing is the RQ3 experiment, not preprocessing. Why: [`thesis/notes.md`](../thesis/notes.md#observer-a-todas-as-observações-no-modelo-principal) | Observer clustering (Cambridge TESSERA group); Phillips et al. (2009) |

**Evaluation — cumulative ablation:** run the RQ1 setup after adding
each step and report the change in performance. This shows which
steps matter, turning preprocessing into a result. Grounded in Ball et
al. (2026) — applies the same idea to each data preparation step.

Open: whether this stays a methodological contribution (own chapter
and ablation) or becomes an explicit research question.

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

Possible extension, if time and weights allow: fine-tune TESSERA, or
train a small MLP head on the embeddings, and compare with the frozen
setup.

**Phase 1: TESSERA only (decision, supervisor, in
person).** The RQ1 effort-reduction curve (see
[RQ1](#rq1--foundation-models-vs-conventional-approaches)) ran first
with TESSERA embeddings. No literature grounding checked for the
phasing itself — it was a scheduling decision, not a methodological
one. **Phase 2 deferred again (my decision):** a same-day
attempt to start the Sentinel-2 arm found its point-level extraction
is not actually cheap here — see
[`thesis/notes.md`](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo).
The original supervisor sequencing stands; other RQ1 items take
priority for now. Feature set is decided for whenever it resumes
(bands, indices, seasonal composites) — see
[`methodology.md`](methodology.md#baseline).

### Other Plants as Classes (adopted direction)

**Superseded (supervisor, in person):** multiclass is
dropped for both models — other-plant observations are not separate
classifier classes. RQ1's background in force is a uniform-random
point pool, unrelated to other-plant data; see
[RQ1](#rq1--foundation-models-vs-conventional-approaches) and
[`data/README.md`](../data/README.md). Full decision and reasoning:
[`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).

**Why the other-plant data is still kept:** it remains a candidate
background source for the RQ3 amplify/mitigate experiment (not yet
run, not scheduled ahead of the RQ1 curve) — see
[RQ3](#rq3--spatial-sampling-bias). The cleaned, grouped dataset (3 000
*A. dealbata* vs. 13 554 other-plant observations after cleaning, in 8
groups from GIFT growth forms, the national invasive list and the
iNaturalist taxonomy) is documented in
[`data/README.md`](../data/README.md); group rules and grounding:
[`thesis/notes.md`](../thesis/notes.md#outras-plantas-em-8-grupos-herbáceas-só-onde-são-a-camada-de-cima).
Grounded in Phillips et al. (2009) for other-species-as-background;
Ball et al. (2026) for grouping into a few classes.

Open:

- Mixed pixels: a 10 m pixel may contain *Acacia* and another class.
- All observers' other plants, or only the dominant observer's, if the
  RQ3 candidate experiment above is run.

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
grows with the age of the observation; the RQ2 filter removes the
oldest first.

Why 2023 and not a later year: 728 *A. dealbata* presences (24.3%) lie in areas
burned in 2025; 2023 imagery still shows the observed vegetation.

Rejected: **nearest available year per observation** — the model
could learn the year instead of *Acacia*, year would correlate with
geography (confounding RQ3), and time becomes a hidden variable.

Safeguard: **disturbance filter**, step 5 of the
[Reference-Data Pipeline](#reference-data-pipeline-proposed).

**Grounded in:** a single reference year follows Ball et al. (2026,
cross-year degradation — see [RQ2](#rq2--data-efficiency)) and the
atoll ecosystem study (2026, single year of AlphaEarth). Persistence
follows Riveiro et al. (2025). Treating many years as one reference
year follows from both plus Ball et al. (2026)'s conclusion that the
bottleneck is reference-data availability: using all observations
keeps the most data at a fixed year; the RQ2 filter then tests the
cost of the oldest ones. Findings: `literature.md`.

### Species Scope (proposed)

The proposal asks for **species-level** mapping of a limited number of
representative species. Observations (all years, non-obscured):
*A. dealbata* 5 241, *A. melanoxylon* 1 884, *A. longifolia* 512.

**Proposed: *A. dealbata* as the target.** Other
*Acacia* species are left out of training (not used as other-plant
classes, since they are *Acacia*). Why: [`thesis/notes.md`](../thesis/notes.md#só-acacia-dealbata).

Later options: *other Acacia* as a class of its own (does the model
tell them apart?), or the genus as an extension.

**Grounded in:** mapping *A. dealbata* alone follows Domingo et al.
(2023, Galicia) and Martins et al. (2016, central-eastern Portugal);
Mouta et al. (2021) mapped *A. longifolia* alone. The genus extension
would follow Eskandari et al. (2025), who mapped *Acacia* sp. in
Galicia.

Additional candidate data source: [`literature.md`](literature.md#data-sources-found-in-the-literature-search).

## Other Open Points

Besides those marked above:

- Study area: the Coimbra district for now (all data cover it);
  other regions later (needed for RQ3).
- Independent validation: COS 2023 *Acacia* class and/or a sample
  checked on OrtoSat 2023; must not overlap spatially with the expert
  reference polygons used for training (RQ1).
- Baseline features and metrics — see [`methodology.md`](methodology.md).