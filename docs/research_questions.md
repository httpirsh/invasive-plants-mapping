# Research Questions

| Item | Status |
|---|---|
| Main question | Adopted |
| RQ1–RQ3 | Proposed (to confirm with supervisor) |
| Prediction task | Adopted |
| Reference-data pipeline (proposal objective 1) | Proposed |
| Absence generation, temporal design | Proposed |
| Frozen embeddings instead of fine-tuning | Proposed (deviation from proposal) |
| Species scope | Open |
| Experiments per RQ | Candidate sketches |

How these questions follow from the literature: [`literature.md`](literature.md).
Methodological questions still open: [`methodology.md`](methodology.md).

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
| Obj. 3 — assess to what extent citizen science supports accurate, species-level mapping | RQ1 (comparison with expert reference data), [Species Scope](#species-scope-open) |
| Work plan 4 — fine-tune foundation models; analyse accuracy, limitations, transferability | [Foundation Model Use](#foundation-model-use-proposed) (frozen embeddings, a justified deviation); RQ3 (transferability) |

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
experimental controls (matched-size comparison in RQ2,
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
- **Grounded in:** Ball et al. (2026) found embeddings beat
  conventional features for tree species with curated inventory
  labels; not yet tested for invasive plants with citizen-science
  labels.

Experiment — same classifier, same test set:

```text
Baseline:          Sentinel-2 features   + citizen-science labels → classifier
Foundation model:  TESSERA embeddings    + citizen-science labels → classifier
Upper bound:       best representation   + expert reference labels → classifier
```

- Candidate classifiers: Random Forest, XGBoost, Logistic Regression.
- **Expert reference labels (open):** MAP.INVADER reference sites are
  scheduled for June 2027 and its maps cover *A. dealbata* only, for
  2026–2028 ([timeline](https://mapinvader.pt/timeline/)); nothing is
  published yet. Candidate: the reference data behind Soriano et al.
  (2026, EARSeL), who mapped *A. dealbata* in central Portugal with
  Sentinel imagery (year, coverage and access unknown — ask).
  Fallback: points sampled from the COS 2023 "Florestas de acácias"
  class. If COS is also the independent test set, training
  and test points must come from separate spatial blocks. COS has a
  1 ha minimum mapping unit, so it over-represents large, pure
  stands; this must be stated.

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of citizen-science reference
data decreases, and does it matter *which* observations are removed —
a distribution-improving filter versus random removal at the same
sample size?

**Fit with the proposal:** answers objective 2 (*use foundation models
to compensate for limited citizen-science data*).

**Why this design:** a filter reduces quantity *and* changes the
distribution at the same time, so on its own it cannot separate the
two effects. No available filter both reduces data substantially and
improves the spatial distribution. Random removal gives the learning
curve; the filter at matched size isolates the effect of *which* data
is removed. Random-removal learning curves exist in the literature;
the matched-size comparison does not.

- **Main test:** random, nested subsets (example levels: 100%, 50%,
  25%, 10%, 5%, 1%), repeated with several seeds, evaluated on
  spatially separated blocks. Fix levels after checking the real
  observation count and spread.
- **Comparison:** at each level, a filtered subset of the same size
  vs. the random subset. The filter is applied in an area with many
  observations, reporting *which* observations it removes and *why*
  Filter choice open.
- The final map always uses all data; RQ2 is a test, not a cleaning
  step.
- The disturbance filter is a fixed preprocessing step (see
  [Reference-Data Pipeline](#reference-data-pipeline-proposed)), not
  the RQ2 filter.
- **Grounded in:** Ball et al. (2026) reached near-optimal accuracy
  with ~5% of labels, with curated forest-inventory labels, not
  citizen science.

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
- The absence strategy affects the bias being measured: a
  target-group background shares the presences' bias and partly
  corrects it. Results must state which background was used;
  target-group vs. random background is a candidate experiment.
- **Real bias case — the dominant observer.** One person made 83% of
  all observations (85% in 2021–2025; 98% of the 2021 peak). Candidate
  experiment: train with all observations vs. capped vs. without that
  observer, test on other observers' records and regions.
- **Grounded in:** Dimson et al. (2023) showed iNaturalist
  invasive-plant records are biased toward roads, trails and disturbed
  areas; reviews report weaker spatial transfer for embeddings.
  Whether bias affects the two representations differently is
  untested.

Experiment — compare training sets: (1) original observations,
(2) spatially thinned, (3) dominant observer capped/removed. Build
bias axes from distance to roads/trails (e.g. OpenStreetMap) and
check they hold in the study area rather than assuming them. Do not
assume bias correction improves performance.

## Shared Design (RQ1–RQ3)

### Prediction Task (adopted)

**Pixel-level binary classification trained on points, applied
wall-to-wall.** The classifier is trained on the 10 m pixel at each
observation (Sentinel-2 features or foundation-model embedding), then
applied to every pixel of the study area to produce a full map. No
dense labels are needed.

- **Semantic segmentation — rejected:** needs dense pixel masks;
  citizen science only provides points.
- **Grid-cell presence/absence — not the training unit:** pixel
  predictions may later be aggregated to cells for evaluation and
  comparison with SDM-style outputs.

### Reference-Data Pipeline (proposed)

Answers the proposal's first objective. The steps that turn
iNaturalist points into labelled pixels are treated as a
**methodological contribution**: each step is documented, counts are
reported, and its effect is measured.

| Step | Status | Notes |
|---|---|---|
| 1. Remove obscured coordinates | Done | 43 presences, 8 242 background removed |
| 2. Positional accuracy | Open | Threshold on coordinate uncertainty relative to 10 m pixels; how to treat missing values |
| 3. Quality grade | Open | Research grade only, or all? |
| 4. Temporal window | Proposed | 2021–2025, see [Temporal Design](#temporal-design-proposed) |
| 5. Disturbance filter | Proposed (fixed) | Burned between observation year and 2023: 2 presences, 33 background |
| 6. Label purity | Open | Does the point represent an *Acacia*-dominated pixel? (e.g. isolated garden tree vs. stand). Check against COS/OrtoSat on a sample; at minimum report |
| 7. Absence generation | Proposed | See [Absence Generation](#absence-generation-proposed) |
| 8. Observer balancing | Open | Cap the dominant observer per cell? Linked to RQ3 |

**Evaluation — cumulative ablation:** run the RQ1 setup after adding
each step and report the change in performance. This shows which
steps matter, turning preprocessing into a result.

Open: whether this stays a methodological contribution (own chapter
and ablation) or becomes an explicit research question.

### Foundation Model Use (proposed)

**Frozen embeddings + light classifiers**, not fine-tuning. This is a
deliberate deviation from the proposal's "fine-tune EO foundation
models" and must be stated as such.

Reasons:

- AlphaEarth is released only as embeddings; it cannot be fine-tuned.
- TESSERA code is open, but model weights must be requested.
- With few, noisy labels, fine-tuning risks fitting the noise.
- The same classifier on every representation isolates the effect of
  the representation (RQ1).

Possible extension, if time and weights allow: fine-tune TESSERA, or
train a small MLP head on the embeddings, and compare with the frozen
setup.

### Absence Generation (proposed)

iNaturalist is presence-only, so pseudo-absences are needed. This is
the most consequential open decision: it shapes dataset construction,
evaluation, and the interpretation of RQ3.

**Proposal: target-group background** — iNaturalist observations of
*other plant species* (Phillips et al., 2009). They share the
observers, platform and places of the *Acacia* presences, so the
model learns *Acacia* vs. other vegetation, not visited vs. unvisited
places.

Checked so far (2021–2025): 6 333 presences vs. 77 301 other-plant
observations (~12:1). The dominant observer also records other plants
(33 065 records, 43%), in 97% of the 1 km cells where they recorded
*Acacia*. Other plants cover much more territory: only 26% of
other-plant cells contain *Acacia*.

**Comparison: random background** — points sampled uniformly over the
study area. Simple, but with biased presences the model may learn
accessibility (roads, urban edges) instead of the species.

Rules to confirm:

- Same observation window and disturbance filter as the presences.
- All observers' other plants, or only the dominant observer's?
- Exclusion buffer around *Acacia* observations (distance open).
- Fixed, reported presence:background ratio (open: 1:1, or higher
  with class weighting).
- Target group (open): all vascular plants, or a restricted group
  such as woody species.

### Temporal Design (proposed)

Time is **held constant, not studied**:

1. **Reference year 2023** for all imagery and auxiliary products
   (Sentinel-2 features, TESSERA embeddings, COS/OrtoSat).
2. **Observation window 2023 ± 2 years (2021–2025)**.

Data constraints:

| Source | Temporal availability |
|---|---|
| OrtoSat / COS | 2023 only |
| TESSERA | One embedding per tile per year, 2017–2025 |
| Sentinel-2 | Any date from 2015/2017 |
| Citizen science (*Acacia*, Coimbra pilot) | 1992–2026; 43% of records from 2021, 98% of those from one observer (not an adoption artifact) |

Pilot observations retained per window:

| Window | Years | Retained |
|---|---|---|
| exact | 2023 | 3.4% |
| ±1 | 2022–2024 | 30.7% |
| ±2 | 2021–2025 | 80.3% |
| ±3 | 2020–2026 | 93.3% |

Why 2023 and not a later year: 2 184 presences (34.5%) lie in areas
burned in 2025; 2023 imagery still shows the observed vegetation.

Why ±2:

- Any narrower window drops 2021, where most of the data is (mostly
  from the dominant observer).
- *Acacia* stands persist for years, so presence in 2021 or 2025 is
  strong evidence of presence in 2023 unless disturbed.
- Every model sees the same period, so differences come from
  representation, data quantity or spatial distribution — not time.

Rejected:

- **Nearest available year per observation:** the model could learn
  the year instead of *Acacia*, year would correlate with geography
  (confounding RQ3), and time becomes a hidden variable.
- **Window as an experimental variable:** temporal mismatch is out of
  scope.

Safeguards:

- **Disturbance filter:** step 5 of the
  [Reference-Data Pipeline](#reference-data-pipeline-proposed).
- **Window sensitivity check:** re-run RQ1 with ±1, ±2 and ±3 windows
  (same number of observations) and check whether the ranking of
  representations holds. Tests a design choice; an unstable ranking
  would itself be a finding.

Variant to discuss — **asymmetric window** (e.g. 2021–2026):
observations after 2023 are stronger evidence of 2023 presence than
earlier ones. Against: after the 2025 fires, a later observation may
be regrowth that does not look like the 2023 stand; 2026 is
incomplete.

### Species Scope (open)

The proposal asks for **species-level** mapping of a limited number of
representative species. Observations 2021–2025: *A. dealbata* 4 145,
*A. melanoxylon* 1 611, *A. longifolia* 417.

Proposed: genus *Acacia* as the main target (more data; three Iberian
precedents), plus *A. dealbata* alone as a species-level check, to
answer the proposal directly.

Additional data source: the University of Coimbra CFE citizen-science
platform for invasive plants in Portugal (invasoras.pt, published on
GBIF). Different platform and observer pool: candidate extra
presences, or a cross-platform test for RQ3.

## Other Open Points

Besides those marked above:

- Study area: district (observations) vs. municipality (TESSERA tiles
  downloaded so far).
- Independent validation: COS 2023 *Acacia* class and/or OrtoSat 2023
  (restricted access); must not overlap spatially with
  expert-reference training points (RQ1).
- Baseline features and metrics — see [`methodology.md`](methodology.md).