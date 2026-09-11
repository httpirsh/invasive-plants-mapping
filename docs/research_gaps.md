# Research Gap

> **Status: candidate gap analysis; the research questions below are
> now PRIMARY.** This document positions the thesis relative to a
> small set of directly relevant papers found so far. It is **not** a
> systematic literature review. Claims of the form "this appears
> underexplored" reflect the current reading list only and must be
> revisited once a fuller literature review and supervisor discussion
> have taken place — see [Open Questions](#open-questions).
>
> Related: [`research_questions.md`](research_questions.md) (canonical
> statement of the thesis's primary research questions, adopted
> 2026-09-11, replacing an earlier, more general data/representation/
> performance/generalization framing that is now discarded — not kept
> as an alternative) and [`methodology.md`](methodology.md) (guiding
> methodological principles). The gap analysis, candidate
> contribution, and candidate experiments below remain preliminary;
> the research questions themselves are primary, not candidates.

## Existing Research

Full bibliographic notes for each paper live in
[`literature_review.md`](literature_review.md). This section only
summarizes what each paper establishes and why it matters for scoping
this thesis's contribution.

### EO Foundation Models and Species Mapping

- **Ball et al. (2026)** — *Geospatial foundation models enable
  data-efficient tree species mapping in temperate mountain forests.*
  Science of Remote Sensing, 14, 100466.
  DOI: [10.1016/j.srs.2026.100466](https://doi.org/10.1016/j.srs.2026.100466)

  Compares TESSERA embeddings, AlphaEarth embeddings, and conventional
  Sentinel-1/Sentinel-2 features for mapping 18 tree species/species
  groups in Trentino, Italy, across classification performance, label
  efficiency, classifier complexity, label impurity, and temporal
  transferability. Foundation-model embeddings outperform conventional
  baselines and approach saturation with a small fraction of training
  labels. The paper argues that foundation models may shift the
  bottleneck away from feature engineering and toward the
  availability, quality, and temporal alignment of ecological
  reference data.

### Citizen Science + Remote Sensing + Plant Mapping

- **Gillespie et al. (2024)** — *Deep learning models map rapid plant
  species changes from citizen science and remote sensing data.*
  PNAS, 121(37), e2318296121.
  DOI: [10.1073/pnas.2318296121](https://doi.org/10.1073/pnas.2318296121)

  Introduces Deepbiosphere, trained on more than 650,000 iNaturalist
  observations across 2,221 plant species paired with remote-sensing
  imagery, for species distribution mapping and temporal monitoring of
  plant-community change at large scale.

### Citizen Science + Invasive Plants + Deep Learning

- **Cardoso et al. (2024)** — *Can citizen science and social media
  images support the detection of new invasion sites? A deep learning
  test case with Cortaderia selloana.* Ecological Informatics, 81,
  102602.
  DOI: [10.1016/j.ecoinf.2024.102602](https://doi.org/10.1016/j.ecoinf.2024.102602)

  Uses citizen-science and social-media **images** with CNN
  classification/object detection to identify and map new *Cortaderia
  selloana* occurrences in Portugal, with reported identification
  success above 77%. This is image-based computer vision on
  ground-level/social-media photos, not satellite EO representation
  learning.

### Citizen Science Sampling Bias

- **Dimson et al. (2023)** — *Citizen science can complement
  professional invasive plant surveys and improve estimates of
  suitable habitat.* Diversity and Distributions.
  DOI: [10.1111/ddi.13749](https://doi.org/10.1111/ddi.13749)

  Quantifies spatial sampling bias in iNaturalist invasive-plant
  observations (biased toward roads/trails, accessible locations, and
  disturbed vegetation) and shows that habitat-suitability estimates
  can differ between citizen-science and professional survey data.

### Conventional Invasive Plant Mapping

- **Mouta et al. (2021)** — *The Best of Two Worlds—Combining
  Classifier Fusion and Ecological Models to Map and Explain Landscape
  Invasion by an Alien Shrub.* (*Acacia longifolia*, Portugal.)

  Maps *Acacia longifolia* using Sentinel-2, machine-learning/
  statistical classifiers, classifier fusion, and ecological modelling.
  Provides a Portuguese precedent for conventional EO + ML invasive
  mapping.

- **Recent Sentinel-1/Sentinel-2 + ML invasive-plant studies**
  (**citation needed**) — referenced qualitatively as recent work
  combining optical/radar fusion, Random Forest, and spatial
  cross-validation for invasive plant mapping, reportedly including
  *Acacia* mapping in Galicia/Northern Iberia. No specific paper has
  been identified and added to `literature_review.md` yet — this entry
  is a placeholder flagging an area to search, not a citation. Do not
  cite this line as if it referred to a specific verified paper until
  the actual source is located and added.

## What Has Already Been Done

Based on the papers above (**established facts**, sourced to the
citations listed):

1. Citizen science → plant/invasive-species observations at scale
   (Gillespie et al. 2024; Dimson et al. 2023; Cardoso et al. 2024).
2. Remote sensing → invasive plant mapping (Mouta et al. 2021; the
   unverified Galicia/Iberia *Acacia* line above).
3. Deep learning → plant species mapping (Gillespie et al. 2024;
   Cardoso et al. 2024).
4. Citizen science + remote sensing → plant mapping (Gillespie et al.
   2024).
5. EO foundation models → species mapping (Ball et al. 2026, tree
   species).
6. EO foundation models → improved label efficiency (Ball et al.
   2026).
7. Citizen-science observations → spatial sampling bias, specifically
   for invasive plants (Dimson et al. 2023).

**Implication for this thesis:** none of the following, individually,
should be presented as this thesis's novelty:

- using an EO foundation model for species/vegetation mapping,
- combining citizen science, remote sensing, and deep learning for
  plant mapping,
- using satellite imagery + Random Forest (or similar conventional
  ML) to map invasive plants,
- observing that citizen-science data are spatially biased.

## Potential Gap

Each of the individual ingredients above — invasive plants, citizen
science, EO foundation models, sparse/biased reference data — has
prior work. What **appears underexplored** (pending a fuller
literature search, see [Open Questions](#open-questions)) is their
intersection:

**EO foundation models + invasive alien plant mapping + citizen-science
reference data + explicit evaluation of reference-data sparsity,
spatial sampling bias, and temporal mismatch.**

A more precise candidate framing:

> How robust are EO foundation-model representations for invasive
> plant mapping when the available citizen-science reference data are
> sparse, spatially biased, and temporally misaligned?

This framing was subsequently adopted, in a more compact form, as the
thesis's Main Research Question — see
[`research_questions.md`](research_questions.md#main-research-question).

We found limited evidence, in the papers reviewed so far, that this
specific combination has been studied together and evaluated in a
controlled way. This is a **potential research gap**, not a confirmed
one — Ball et al. (2026) study foundation models + label efficiency
but for tree species with (presumably) more systematic reference data,
not citizen-science invasive-plant records; Dimson et al. (2023)
study citizen-science bias for invasive plants but not through EO
foundation-model representations; Cardoso et al. (2024) study
citizen-science + invasive plants in Portugal but through image-based
CNNs, not satellite EO foundation models.

## Candidate Contribution

**Data-efficient and bias-aware invasive plant mapping using Earth
Observation foundation models and citizen science.**

This is **not** "apply TESSERA/AlphaEarth to invasive plants." The
candidate scientific contribution is a controlled investigation of how
EO foundation-model representations behave under realistic
citizen-science reference-data limitations (sparsity, spatial bias,
temporal mismatch), relative to a conventional satellite-feature
baseline.

## Research Questions

> **Status: primary**, adopted 2026-09-11. The canonical statement
> lives in [`research_questions.md`](research_questions.md); they are
> repeated here together with an explicit derivation from the
> literature above, so the gap → RQ logic is traceable in one place.

### RQ1 — Foundation models vs. conventional approaches

Do Earth Observation foundation-model representations improve
invasive plant mapping compared with conventional spectral-temporal
satellite features?

**Why this follows from the literature:** Ball et al. (2026) show
foundation-model embeddings outperforming conventional Sentinel-1/-2
features for tree species mapping; Mouta et al. (2021) (and the
unverified Galicia/Iberia line) establish a credible conventional
satellite + ML precedent specifically for invasive plants. RQ1 asks
whether the foundation-model advantage seen for tree species also
holds for invasive plants evaluated against a comparably strong
conventional baseline, using citizen-science reference data — a
comparison we found no evidence of in the papers reviewed so far.

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of available citizen-science
reference data decreases?

**Why this follows from the literature:** Ball et al. (2026)
demonstrate label efficiency for foundation-model embeddings, but
with reference data that is presumably more systematic than
citizen-science records. Gillespie et al. (2024) and Dimson et al.
(2023) show citizen-science plant/invasive-species data exists at
scale but with different sparsity and quality characteristics than
curated forestry labels. RQ2 tests whether the label-efficiency
advantage transfers to citizen-science reference data specifically.

### RQ3 — Spatial sampling bias

How does spatial sampling bias in citizen-science observations affect
invasive plant mapping using conventional satellite representations
and EO foundation-model representations?

**Why this follows from the literature:** Dimson et al. (2023)
establish that citizen-science invasive-plant observations are
spatially biased (toward roads/trails, accessible locations, and
disturbed vegetation). No paper reviewed so far tests whether this
bias affects conventional and foundation-model representations
differently — RQ3 targets that specific comparison.

### RQ4 — Temporal mismatch

How does temporal mismatch between citizen-science observations and
satellite imagery affect invasive plant mapping performance, and does
the effect differ between conventional and foundation-model
representations?

**Why this follows from the literature:** Ball et al. (2026)
specifically flag temporal alignment between reference data and
imagery as a potential bottleneck for foundation-model performance.
Citizen-science observations (Gillespie et al. 2024; Dimson et al.
2023) are opportunistic and not temporally coordinated with satellite
acquisitions, unlike more controlled reference datasets. RQ4 tests
this bottleneck directly and asks whether conventional and
foundation-model representations are affected equally.

### Optional / secondary idea (not one of the four primary RQs)

Can model uncertainty and/or observation density identify locations
where additional citizen-science observations would provide the
greatest value? Kept as a possible extension if time allows; not part
of the primary research questions above.

## Candidate Experiments

> **Status: candidate experimental sketches, not fixed methodology.**
> Exact models, foundation model(s), percentages, and temporal ranges
> are open and depend on literature review and data availability (see
> [`methodology.md`](methodology.md)).

### Baseline (feeds RQ1)

```text
citizen science observations → labels / reference data
Sentinel-1 / Sentinel-2      → conventional spectral-temporal features
                              → conventional ML
```

Candidate models (exact choice open): Random Forest, XGBoost, Logistic
Regression.

### Foundation-model experiment (feeds RQ1)

```text
citizen science observations → labels / reference data
satellite EO                 → TESSERA / AlphaEarth / another
                                justified EO foundation model
                              → embeddings
                              → ML classifier
```

The exact foundation model must remain open until literature and data
availability are evaluated.

### Label-efficiency experiment (RQ2)

Train models on progressively smaller subsets of citizen-science
observations (example levels, not final: 100%, 50%, 25%, 10%, 5%, 1%)
and compare conventional EO features vs. EO foundation-model
embeddings across these levels.

### Sampling-bias experiment (RQ3)

Compare training-data construction strategies, e.g.:

1. original citizen-science observations,
2. spatially balanced/thinned observations,
3. observation-density-aware sampling.

Measure effects on performance, spatial generalization, and geographic
transfer. Do not assume bias correction will improve performance —
this is a question, not an expected result.

**Grounding the bias, not just thinning at random:** Dimson et al.
(2023) document *specific* bias axes for citizen-science invasive-plant
observations — proximity to roads/trails, general accessibility, and
disturbed vegetation. Where possible, strategies 2–3 above (and any
additional "biased vs. corrected" comparison) should be constructed
using those same axes (e.g. distance-to-road/trail, accessibility
layers) rather than arbitrary spatial thinning or density-only
resampling — this keeps the manipulated conditions ecologically
realistic and traceable to a documented bias mechanism instead of an
artificial one. This requires auxiliary covariates (e.g. road/trail
or accessibility layers) — see
[`datasets.md`](datasets.md#auxiliary--external-data), currently
undecided.

### Temporal-mismatch experiment (RQ4)

Compare temporal relationships between observations and satellite
imagery (example ranges, not final: same year, ±1, ±2, ±3 years),
constrained to ranges actually supported by the dataset and ecological
context.

### Spatial-generalization experiment (cross-cutting, supports evaluation of RQ1–RQ4)

Avoid relying exclusively on random train/test splits. Investigate
spatial blocking, Group K-Fold, and geographically separated test
regions, with explicit attention to spatial leakage, spatial
autocorrelation, and geographic generalization.

## Main Hypothesis

**EO foundation models may provide more data-efficient representations
for invasive plant mapping, but their advantage may become limited by
the quality, quantity, spatial distribution, and temporal alignment of
citizen-science reference data.**

This is a **hypothesis**, not an expected or claimed result — do
**not** assume that foundation models will perform better. It is
motivated by Ball et al. (2026), who suggest that reference-data
quality and temporal alignment can become the main bottleneck for
foundation-model-based species mapping even where labels are
relatively systematic. This reframes the central question from "are
foundation models better?" toward:

> Under what reference-data conditions are foundation models actually
> useful for invasive plant mapping?

## Scope and Feasibility

> **Status: candidate prioritization, not a decision.** Added because
> RQ1–RQ4 were adopted before the actual citizen-science and satellite
> datasets were explored (`docs/datasets.md` still lists both sources
> as "not yet decided"). This section exists so feasibility is checked
> deliberately rather than discovered mid-experiment.

**Blocking feasibility check (do before finalizing RQ2/RQ4
experimental design):** once real citizen-science data is obtained,
compute basic descriptive stats — total observation count, spatial
extent/clustering, and temporal range/spread — before committing to
specific label-efficiency percentages (RQ2) or temporal-mismatch
windows (RQ4). If the dataset is small or clustered in one or two
years, the example levels/ranges in the experiments above (e.g. 1%
subsets, ±3-year windows) may not be meaningful and should be revised
to what the data actually supports, rather than kept as originally
sketched.

**Candidate prioritization if the thesis timeline is constrained:**
RQ1 (baseline vs. foundation model) is the prerequisite for the other
three and should be treated as the core deliverable. RQ2 and RQ3 are
next in priority since they are directly grounded in a specific,
verified literature gap (Ball et al. 2026 for label efficiency;
Dimson et al. 2023 for spatial bias). RQ4 (temporal mismatch) is the
most exploratory of the four — it depends most heavily on the
citizen-science dataset actually having usable multi-year spread — and
is the first candidate to reduce to a lighter secondary analysis, or
drop, if time runs short. This ordering is a suggestion to revisit
after the feasibility check above and after supervisor discussion, not
a fixed decision.

## Open Questions

- This document is based on five verified papers found so far (plus
  one unverified placeholder — the Galicia/Iberia line above), not a
  systematic literature review. The "potential gap" claim needs
  revisiting once a broader search is done (e.g. across Web of Science/Scopus/Google
  Scholar for combinations of "foundation model" + "citizen science" +
  "invasive species"/"biological invasion").
- The "recent Sentinel-1/Sentinel-2 + Galicia/Northern Iberia Acacia"
  reference has no identified citation yet — find and add the actual
  paper(s) to `literature_review.md`, or remove the claim if none is
  found.
- **Resolved 2026-09-11:** the RQs above are now the thesis's primary
  research questions, replacing the earlier data-integration/
  representation/performance/generalization framing in
  `research_questions.md`. That earlier framing is discarded, not
  kept as an alternative.
- Whether the optional/secondary uncertainty- or
  observation-density-guided sampling idea (see
  [Research Questions](#research-questions)) is in scope at all for
  the thesis timeline, given it adds an active-learning-like
  component beyond the four primary RQs.
- Exact EO foundation model(s) to use (TESSERA, AlphaEarth, or other)
  — depends on data availability, licensing, and further literature
  review.
- Exact conventional baseline model and feature set — depends on the
  dataset once explored (see `datasets.md` and `data/README.md`).
- Exact label-efficiency percentages, sampling-bias covariates, and
  temporal-mismatch ranges, and whether all four RQs can be run at
  full depth or some must be scoped down — see
  [Scope and Feasibility](#scope-and-feasibility) for the blocking
  feasibility check and candidate prioritization.
- Whether "invasive plant(s)" in scope means one species, several
  species, or a species-agnostic invasive/non-invasive framing —
  affects how directly Cardoso et al. (2024) and Mouta et al. (2021)
  serve as precedents.
