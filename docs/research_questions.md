# Research Questions

| Item | Status |
|---|---|
| Main question | Adopted |
| RQ1, RQ3 | Proposed (to confirm with supervisor) |
| RQ2 (recency-based filter, no random removal) | Adopted 2026-10-21 |
| Prediction task | Adopted; segmentation mask open |
| Reference-data pipeline (proposal objective 1) | Proposed |
| Temporal design: all iNaturalist observations treated as 2023 | Adopted 2026-10-21 |
| Other plants as classes (multiclass) | Adopted direction 2026-10-21; details open |
| Expert reference data: *A. dealbata* polygons from the supervisor | Adopted 2026-10-20; reference year to confirm |
| Frozen embeddings instead of fine-tuning | Adopted 2026-10-21 (deviation from proposal) |
| Species scope | Proposed (2026-10-20): *A. dealbata*, other *Acacia* left out |
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

The components are not new on their own:

- **Embeddings vs. conventional features** has been tested for tree
  species (Ball et al., 2026), cropland, ecosystems and burned area
  (including Portugal: Gonçalves et al., 2026). The AlphaEarth paper
  itself evaluated on iNaturalist research-grade labels, at genus
  level (Brown et al., 2025).
- **Spatial bias in citizen science** is well documented for
  invasive plants (Dimson et al., 2023).
- **Weaker spatial transfer of embeddings** is reported in reviews
  (Zhu et al., 2026, "Earth Embeddings") and in work showing that
  buffered spatial validation narrows the embedding advantage over
  Sentinel features (old-growth forest preprint, arXiv 2609.28194).

Closest work:

- Cambridge TESSERA group: GBIF occurrences as weak labels over
  TESSERA for habitat mapping, with strong observer clustering
  reported (work in progress, not invasive plants).
- Deepbiosphere applied to invasive plants in Michigan (bioRxiv,
  2026): citizen science + imagery + climate at 256 m, without EO
  foundation models.

No work was found that combines **EO foundation models, invasive
plants and citizen-science labels with explicit evaluation of bias**.
The contribution therefore lies in the combination and in the
experimental controls (recency-based filter in RQ2,
amplify-or-mitigate framing in RQ3, expert-reference comparison in
RQ1), not in any single question.

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
much is lost compared with training on expert reference data?

**Fit with the proposal:** answers objective 3 (*to what extent
citizen science supports accurate mapping*) and part of objective 2.
Comparing representations shows how good foundation models are; the
expert-reference model is the upper bound that shows what is lost by
using citizen science instead of expert data.

- A question of degree, not yes/no.
- All representations come from the same reference year, so only the
  representation changes between compared models.
- **Grounded in:** the comparison design comes from Ball et al.
  (2026), who compared TESSERA and AlphaEarth embeddings with
  conventional Sentinel-1 + Sentinel-2 features on the same labels for
  18 tree species (embeddings won; curated inventory labels). The
  atoll ecosystem study (2026) used the same design with
  AlphaEarth 2023 embeddings vs. Sentinel-2 bands and indices. Not
  yet tested for invasive plants with citizen-science labels.
- **Upper bound grounded in:** Dimson et al. (2023) built habitat
  models separately from iNaturalist records and from professional
  surveys of invasive plants and compared them; the idea of training
  the same model on citizen-science vs. expert data comes from there.
  They also found the two sources have opposite biases, so the expert
  upper bound is biased differently, not bias-free.

Experiment — same classifier, same test set:

```text
Baseline:          Sentinel-2 features   + citizen-science labels → classifier
Foundation model:  TESSERA embeddings    + citizen-science labels → classifier
Upper bound:       best representation   + expert reference labels → classifier
```

- Candidate classifiers: Random Forest, Logistic Regression, compact
  neural network. **Grounded in:** Random Forest was used on
  embeddings by Ball et al. (2026) and Yang et al. (2026), and for
  *Acacia* with Sentinel-2 or PlanetScope by Mouta et al. (2021),
  Domingo et al. (2023) and Eskandari et al. (2025, best of the
  algorithms tested). Ball et al. (2026) also tested linear
  classifiers (weaker on embeddings) and a compact neural network
  (best on embeddings).
- **Expert reference labels (adopted):** *A. dealbata* polygons
  collected by visual interpretation and/or field work, sent by the
  supervisor (see `data/README.md`). In the Coimbra district: 1 849
  polygons with `classifica = 1` (244 ha), all in Sentinel-2 tile TNE;
  1 364 of all positives are ~5 m-radius circles (point-like), the
  rest larger patches. 59% of the district polygons touch a COS 2023
  "Florestas de acácias" polygon.
  - **Species:** *A. dealbata* only, the proposed target (see
    [Species Scope](#species-scope-proposed)).
  - **Clustered:** the district polygons fall in 15 cells of 10 km,
    so few independent spatial blocks are available to split training
    and test.
  - **Negatives:** the `classifica ≠ 1` polygons lie mostly on water
    and built-up areas and are not used. Negatives for the expert
    model come from another source (open; e.g. COS 2023 non-*Acacia*
    vegetation classes).
  - **Labels independent of citizen science:** collected by the
    experts in the field or by visual interpretation, not taken from
    iNaturalist (supervisor, to confirm in writing).
  - **Locations overlap with citizen science (design constraint):**
    all 70 iNaturalist presences inside a polygon, and 96% of the 582
    within 50 m, are the dominant observer's. Experts and that observer
    visited the same places. Consequences: tested on these polygons,
    the citizen-science model would be evaluated where it was trained
    (inflated score), so training and test must be split by spatial
    blocks (15 blocks of 10 km); as the upper bound, both models learn
    from nearly the same areas, so only the label source changes, but
    both inherit the same spatial bias.
  - **Open:** reference year (no date field); imagery used for the
    visual interpretation; how the sites were chosen.

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
  98.8% of presences, 2021 onwards 84.0%, 2023 onwards 29.1% (7 898
  dated, non-obscured presences) — so levels are set by date, not
  year. Fix levels after checking the real counts.
- **Open:** whether observations after 2023 (2024–2026: 2 040
  presences) count as "more recent", or whether recency is distance
  to 2023.
- **Limitation (to state):** without a random-removal baseline, each
  level changes quantity *and* composition (age, observers, places)
  at once; RQ2 measures their joint effect.
- The final map always uses all data; RQ2 is a test, not a cleaning
  step.
- The disturbance filter is a fixed preprocessing step (see
  [Reference-Data Pipeline](#reference-data-pipeline-proposed)), not
  the RQ2 filter.
- **Grounded in:** training with decreasing fractions of labels
  comes from Ball et al. (2026), who reached near-optimal accuracy
  with ~5% of training parcels (curated labels, random reduction).
  Removing the oldest observations first is supported by their
  cross-year result: performance dropped when imagery and labels came
  from different years (weighted F1 −9% TESSERA, −15% AlphaEarth):
  the older an observation, the larger its mismatch with the 2023
  imagery. Ball et al. (2026) reduced labels at random; filtering by
  recency is this thesis's own step, motivated by that result.

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
- The negative classes affect the bias being measured: other-plant
  classes share the presences' bias and partly correct it. Results
  must state this; other-plant classes vs. random background is a
  candidate experiment.
- **Real bias case — the dominant observer.** One person made 83% of
  all observations (85% in 2021–2025; 98% of the 2021 peak). Candidate
  experiment: train with all observations vs. capped vs. without that
  observer, test on other observers' records and regions.
- **Grounded in:** the bias axes (roads, trails, disturbed areas)
  come from Dimson et al. (2023), who found them in iNaturalist
  invasive-plant records in Hawaiʻi. The amplify/mitigate question
  comes from work reporting weaker spatial transfer of embeddings:
  Zhu et al. (2026, review), Yang et al. (2026) and the old-growth
  forest preprint (2026), where buffered spatial validation narrowed
  the embedding advantage. Strong clustering of
  citizen-science labels over TESSERA was also reported by the
  Cambridge TESSERA group (work in progress). Whether bias affects
  the two representations differently is untested.
- Spatial thinning and capping the dominant observer are motivated by
  the clustering reported by the Cambridge TESSERA group (labels
  concentrated around reserves, canals and a zoo) and by Dimson et
  al. (2023), whose biased iNaturalist records gave habitat models
  that only partly overlapped those from professional surveys.
  Phillips et al. (2009) found the largest gains from bias correction
  where presences were most biased, which applies to a single
  dominant observer.

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
applied to every pixel of the study area. Classes are *Acacia* plus
groups of other plants (see [Other Plants as
Classes](#other-plants-as-classes-adopted-direction)); the *Acacia*
map is the predicted *Acacia* probability per pixel.

**Grounded in:** training per-pixel classifiers on citizen-science
point observations over embeddings was done by Brown et al. (2025,
iNaturalist research-grade observations at genus level)
and by the Cambridge TESSERA group (GBIF occurrences as weak labels
for habitats, work in progress). The task follows them.

- **Segmentation mask (open, interpretation to confirm):** raised
  when discussing exclusion buffers. Likely meaning: replace the fixed
  buffer with a mask of the actual *Acacia* patch around each
  observation. The task stays pixel classification; the mask changes
  how labels and exclusions are built (see [Other Plants as
  Classes](#other-plants-as-classes-adopted-direction)). Grounded in
  Rivier et al. (2023/2024), who propagated sparse point labels to
  superpixels.
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
| 2. Positional accuracy | Open | Threshold on coordinate uncertainty relative to 10 m pixels; how to treat missing values | Ball et al. (2026): label impurity lowers accuracy, though embeddings tolerate moderate amounts; a point off by more than a pixel is an impure label |
| 3. Quality grade | Open | Research grade only, or all? | Research-grade only was used by Gillespie et al. (2024) and Brown et al. (2025) |
| 4. Temporal design | Adopted | All observations treated as 2023, see [Temporal Design](#temporal-design-adopted) | See that section |
| 5. Disturbance filter | Proposed (fixed) | Burned between observation and 2023 (ICNF 1975–2025; fires before 2014 have the year only): 35 presences (0.4%), 2 880 other plants (2.6%) | Riveiro et al. (2025): burned *A. dealbata* stands regrow, so the burned pixel no longer matches the label though the species remains |
| 6. Label purity | Open | Does the point represent an *Acacia*-dominated pixel? (e.g. isolated garden tree vs. stand). Check against COS/OrtoSat on a sample; at minimum report | Ball et al. (2026): embeddings robust to moderate label impurity; soft labels (species proportions) beat hard labels |
| 7. Negative classes | Adopted direction | See [Other Plants as Classes](#other-plants-as-classes-adopted-direction) | Phillips et al. (2009); see that section |
| 8. Observer balancing | Open | Cap the dominant observer per cell? Linked to RQ3 | Motivated by observer clustering (Cambridge TESSERA group) and Phillips et al. (2009), see RQ3 |

**Evaluation — cumulative ablation:** run the RQ1 setup after adding
each step and report the change in performance. This shows which
steps matter, turning preprocessing into a result. Grounded in Ball et
al. (2026), who measured how label impurity and soft vs. hard labels
change accuracy: the ablation applies the same idea to each data
preparation step.

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

**Grounded in:** frozen embeddings with light classifiers on top were
used by Ball et al. (2026, TESSERA and AlphaEarth with Random Forest,
linear models and a compact neural network), Yang et al. (2026, Random
Forest on AlphaEarth) and Brown et al. (2025, embeddings
used without re-training). The approach follows them.

Possible extension, if time and weights allow: fine-tune TESSERA, or
train a small MLP head on the embeddings, and compare with the frozen
setup.

### Other Plants as Classes (adopted direction)

iNaturalist is presence-only. Observations of *other plant species*
are used as **classes of their own**, not as absences: an observation
of eucalyptus is a presence of eucalyptus, not evidence that no
*Acacia* is there. The model becomes multiclass (*Acacia* + groups of
other plants) and learns to separate *Acacia* from the vegetation it
is confused with.

Other plants share the observers, platform and places of the
*Acacia* presences, so the model learns *Acacia* vs. other vegetation,
not visited vs. unvisited places.

**Grounded in:**

- Using other species recorded by the same observers comes from
  Phillips et al. (2009), who used them as background (*target-group
  background*); across 226 species it improved every modelling method
  tested, most where presences were most biased.
- Using them as classes rather than background follows multi-species
  models trained on citizen science: Gillespie et al. (2024) trained
  one model on 2,221 plant species from iNaturalist observations.
- Grouping species into a few classes follows Ball et al. (2026), who
  mapped 18 tree species *and groups* as classes.

Checked (all years, non-obscured): 7 898 presences vs. 110 576
other-plant observations (~14:1). The dominant observer also records
other plants (36 080 records, 33%), in 96.7% of the 1 km cells where
they recorded *Acacia*. Other plants cover much more territory: only
26.6% of other-plant cells contain *Acacia*.

**Expert model, same formulation (proposed, 2026-10-20):** in RQ1 the
expert model is also multiclass. Its negatives (random points in COS
2023 vegetated classes) are labelled by the COS class they fall in
(e.g. eucalyptus forest, pine forest, other forest, agriculture,
shrubland; rare classes merged), not as a single "not *Acacia*"
class. Reasons: RQ1 compares label sources, so the task formulation
must be the same in both arms; a COS polygon (minimum mapping unit
1 ha) says what land cover is mapped there, not that no *Acacia* is
present, the same argument as for other plants; and the confusion
matrix shows what *A. dealbata* is confused with. Both arms are
scored by P(*A. dealbata*) on the same test points, so the class sets
need not match. A binary version (*A. dealbata* vs. the rest) is run
as a sensitivity check in both arms. Grounded in Ball et al. (2026),
as above; no other source checked for this choice.

Open:

- Class groups: by genus or growth form (e.g. eucalyptus, pines,
  oaks, other trees, shrubs, herbaceous); likely 5–10 groups.
- Class imbalance (weighting or sampling).
- Mixed pixels: a 10 m pixel may contain *Acacia* and another class.
- **Patch mask instead of a fixed buffer (proposed, to confirm):**
  delimit the *Acacia* patch around each observation and use it to
  (1) exclude other-plant points inside the patch and (2) take all
  patch pixels as *Acacia* training pixels, not only the observed one.
  Candidate methods: region growing on TESSERA embedding similarity
  from the observed pixel (with a maximum radius); superpixels on
  Sentinel-2 or embeddings (as in Rivier et al., 2023/2024, who
  propagated point labels to superpixels); COS 2023 "Florestas
  de acácias" polygons where the point falls inside one (about 17% of
  2021–2025 presences). Risks: the mask may spread into similar
  non-*Acacia* vegetation (check a sample on OrtoSat), and large
  patches give many more pixels than isolated trees (may need
  balancing).
- All observers' other plants, or only the dominant observer's?
- How *Acacia* metrics are reported against several classes.

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

Why 2023 and not a later year: 2 299 presences (29.1%) lie in areas
burned in 2025; 2023 imagery still shows the observed vegetation.

Rejected: **nearest available year per observation** — the model
could learn the year instead of *Acacia*, year would correlate with
geography (confounding RQ3), and time becomes a hidden variable.

Safeguard: **disturbance filter**, step 5 of the
[Reference-Data Pipeline](#reference-data-pipeline-proposed).

**Grounded in:**

- A single reference year follows Ball et al. (2026), where
  performance dropped when imagery and labels came from different
  years (weighted F1 −9% TESSERA, −15% AlphaEarth). The atoll
  ecosystem study (2026) also used a single year of
  AlphaEarth embeddings (2023).
- Persistence: Riveiro et al. (2025) found *A. dealbata* stands in
  central Portugal persisted over three years even after slashing and
  burning.
- Treating observations from many years as one reference year
  follows from the two points above (persistence, and the cost of
  mixing years) and from Ball et al. (2026)'s conclusion that the
  bottleneck is the availability of reference data: using all
  observations keeps the most data at a fixed year. The RQ2 filter
  then tests the cost of the oldest ones.

### Species Scope (proposed)

The proposal asks for **species-level** mapping of a limited number of
representative species. Observations (all years, non-obscured):
*A. dealbata* 5 241, *A. melanoxylon* 1 884, *A. longifolia* 512.

**Proposed (2026-10-20): *A. dealbata* as the target.** Other
*Acacia* species are left out of training (not used as other-plant
classes, since they are *Acacia*). Reasons:

- The expert reference polygons cover *A. dealbata* only, so the RQ1
  comparison is only fair for that species.
- It answers the proposal's species-level objective directly.
- It is most of the data (66% of *Acacia* observations).
- The species differ from space: *A. dealbata* forms dense patches
  with winter flowering; *A. melanoxylon* is a tree mixed into
  forests; *A. longifolia* a coastal and dune shrub. One class would
  mix different signals.

Later options: *other Acacia* as a class of its own (does the model
tell them apart?), or the genus as an extension.

**Grounded in:** mapping *A. dealbata* alone follows Domingo et al.
(2023, Galicia) and Martins et al. (2016, central-eastern Portugal);
Mouta et al. (2021) mapped *A. longifolia* alone. The genus extension
would follow Eskandari et al. (2025), who mapped *Acacia* sp. in
Galicia.

Additional data source: the University of Coimbra CFE citizen-science
platform for invasive plants in Portugal (invasoras.pt, published on
GBIF). Different platform and observer pool: candidate extra
presences, or a cross-platform test for RQ3.

## Other Open Points

Besides those marked above:

- Study area: the Coimbra district for now (all data cover it);
  other regions later (needed for RQ3).
- Independent validation: COS 2023 *Acacia* class and/or a sample
  checked on OrtoSat 2023; must not overlap spatially with the expert
  reference polygons used for training (RQ1).
- Baseline features and metrics — see [`methodology.md`](methodology.md).