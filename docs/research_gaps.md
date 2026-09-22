# Research Gap

> **Status: candidate gap analysis; the research questions below are
> now PRIMARY.** Positions the thesis relative to a small set of
> directly relevant papers found so far — **not** a systematic
> literature review. Claims of the form "appears underexplored"
> reflect the current reading list only and must be revisited after a
> fuller search and supervisor discussion — see
> [Open Questions](#open-questions).
>
> Related: [`research_questions.md`](research_questions.md) (canonical
> statement of the primary RQs, adopted 2026-09-11, replacing an
> earlier, more general framing that is now discarded) and
> [`methodology.md`](methodology.md) (guiding principles). Everything
> below the research questions (gap analysis, contribution, candidate
> experiments) remains preliminary; the RQs themselves are primary.

## Existing Research

Full bibliographic notes, methods, and findings are in
[`literature_review.md`](literature_review.md). This section only
lists what each paper contributes to the gap argument below.

### EO Foundation Models and Species Mapping

- **Ball et al. (2026)** — EO foundation-model embeddings (TESSERA,
  AlphaEarth) outperform conventional Sentinel-1/-2 features for tree
  species mapping (weighted F1 0.83 vs. 0.80) and reach near-optimal
  accuracy with ~5% of training labels; but performance *degrades*
  9–15% (weighted F1) across years, hitting rare species hardest —
  empirical evidence, not just a flagged concern, that reference-data
  temporal alignment becomes the bottleneck. See
  [`literature_review.md`](literature_review.md) for the full,
  verified breakdown.

### Citizen Science + Remote Sensing + Plant Mapping

- **Gillespie et al. (2024)** — Deepbiosphere: 650,000+ iNaturalist
  observations across 2,221 species, combined with remote sensing and
  deep learning, in California (AUC 0.95 vs. 0.88 vs. conventional
  SDM baselines) — a single-region study, not a generality.

### Citizen Science + Invasive Plants + Deep Learning

- **Cardoso et al. (2024)** — citizen-science/social-media *images* +
  CNNs detect *Cortaderia selloana* in Portugal (>77% success) —
  image-based computer vision, not satellite EO representation
  learning.

### Citizen Science Sampling Bias

- **Dimson et al. (2023)** — iNaturalist invasive-plant records
  (Hawaiʻi, 4 species) are spatially biased toward roads/trails,
  accessible locations, and disturbed vegetation; resulting
  habitat-suitability estimates differ from professional survey data.

### Conventional Invasive Plant Mapping

- **Mouta et al. (2021)** — Sentinel-2 + classifier fusion (eight
  classifiers) + ecological modelling maps *Acacia longifolia* in
  northern Portugal. Remote Sensing, 13(16), 3287.
  DOI: [10.3390/rs13163287](https://doi.org/10.3390/rs13163287)
- **Domingo et al. (2023)** — Sentinel-2 + phenological spectral
  differences maps *Acacia dealbata* in Ourense, Galicia (94% reported
  accuracy). DOI: [10.3390/rs15030722](https://doi.org/10.3390/rs15030722)
- **Eskandari, Acuña-Alonso & Álvarez (2025)** — PlanetScope + Random
  Forest maps *Acacia* sp. in the Cíes Islands, Galicia.
  DOI: [10.1016/j.foreco.2025.122696](https://doi.org/10.1016/j.foreco.2025.122696)

  Domingo et al. and Eskandari et al. replace an earlier "citation
  needed" placeholder for Galicia/Iberia *Acacia* mapping (found
  2026-09-11). Neither confirms the Sentinel-1+Sentinel-2-fusion +
  spatial-cross-validation combination that placeholder loosely
  described — that specific combination is still unverified for any
  single Galicia paper.

## What Has Already Been Done

Established facts, sourced to the citations above:

1. Citizen science → plant/invasive-species observations at scale
   (Gillespie et al. 2024; Dimson et al. 2023; Cardoso et al. 2024).
2. Remote sensing → invasive plant mapping (Mouta et al. 2021;
   Domingo et al. 2023; Eskandari et al. 2025).
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
should be presented as this thesis's novelty: using an EO foundation
model for species/vegetation mapping; combining citizen science,
remote sensing, and deep learning for plant mapping; using satellite
imagery + Random Forest (or similar) to map invasive plants;
observing that citizen-science data are spatially biased.

## Potential Gap

Each ingredient above has prior work; their intersection — EO
foundation models + invasive plant mapping + citizen-science reference
data, with explicit evaluation of sparsity, spatial bias, and temporal
mismatch — **appears underexplored** (pending a fuller search, see
[Open Questions](#open-questions)). This gap was refined into the
thesis's Main Research Question — see
[`research_questions.md`](research_questions.md#main-research-question).

We found limited evidence that this specific combination has been
studied together: Ball et al. (2026) address foundation models +
label efficiency but for tree species with more systematic reference
data; Dimson et al. (2023) address citizen-science bias for invasive
plants but not through foundation-model representations; Cardoso et
al. (2024) address citizen-science + invasive plants in Portugal but
through image-based CNNs, not satellite EO foundation models.

## Candidate Contribution

**Data-efficient and bias-aware invasive plant mapping using Earth
Observation foundation models and citizen science.**

This is **not** "apply TESSERA/AlphaEarth to invasive plants." The
candidate contribution is a controlled investigation of how EO
foundation-model representations behave under realistic
citizen-science reference-data limitations (sparsity, spatial bias,
temporal mismatch), relative to a conventional satellite-feature
baseline.

## Research Questions

> **Status: primary**, adopted 2026-09-11. Canonical statement in
> [`research_questions.md`](research_questions.md); repeated here with
> a one-line grounding in the literature above (item numbers refer to
> [What Has Already Been Done](#what-has-already-been-done)) so the
> gap → RQ logic is traceable in one place, without re-explaining each
> paper again.

### RQ1 — Foundation models vs. conventional approaches

Do Earth Observation foundation-model representations improve
invasive plant mapping compared with conventional spectral-temporal
satellite features?

**Grounds:** combines the FM-vs-conventional result for tree species
(fact 5) with the conventional invasive-plant precedents (fact 2) —
that comparison, for invasive plants with citizen-science labels, was
not found in the literature reviewed.

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of available citizen-science
reference data decreases?

**Grounds:** tests whether the label-efficiency advantage (fact 6)
transfers from systematic forestry labels to citizen-science reference
data (facts 1, 7).

### RQ3 — Spatial sampling bias

How does spatial sampling bias in citizen-science observations affect
invasive plant mapping using conventional satellite representations
and EO foundation-model representations?

**Grounds:** tests whether the documented spatial bias (fact 7)
affects conventional and foundation-model representations
differently — not tested in the literature reviewed.

### RQ4 — Temporal mismatch

How does temporal mismatch between citizen-science observations and
satellite imagery affect invasive plant mapping performance, and does
the effect differ between conventional and foundation-model
representations?

**Grounds:** tests the temporal-degradation effect Ball et al. (2026)
empirically demonstrated (9–15% weighted-F1 decline across years,
fact 6) against citizen science's inherently opportunistic timing
(fact 1), and whether it affects both representation types equally.

### Optional / secondary idea (not one of the four primary RQs)

Can model uncertainty and/or observation density identify locations
where additional citizen-science observations would provide the
greatest value? Kept as a possible extension if time allows.

## Candidate Experiments

> **Status: candidate sketches, not fixed methodology.** Exact models,
> foundation model(s), percentages, and temporal ranges are open and
> depend on literature review and data availability — see
> [`methodology.md`](methodology.md).

### Baseline (feeds RQ1)

```text
citizen science observations → labels / reference data
Sentinel-1 / Sentinel-2      → conventional spectral-temporal features
                              → conventional ML
```

Candidate models (open): Random Forest, XGBoost, Logistic Regression.

### Foundation-model experiment (feeds RQ1)

```text
citizen science observations → labels / reference data
satellite EO                 → TESSERA / AlphaEarth / another
                                justified EO foundation model
                              → embeddings
                              → ML classifier
```

The exact foundation model remains open until literature and data
availability are evaluated.

### Label-efficiency experiment (RQ2)

Train on progressively smaller subsets of citizen-science observations
(example levels, not final: 100%, 50%, 25%, 10%, 5%, 1%); compare
conventional EO features vs. EO foundation-model embeddings across
levels.

### Sampling-bias experiment (RQ3)

Compare training-data construction strategies: (1) original
citizen-science observations, (2) spatially balanced/thinned
observations, (3) observation-density-aware sampling. Measure effects
on performance, spatial generalization, and geographic transfer. Do
not assume bias correction will improve performance — this is a
question, not an expected result.

Construct strategies 2–3 using the specific bias axes Dimson et al.
(2023) documented (see [Existing Research](#citizen-science-sampling-bias))
— e.g. distance-to-road/trail, accessibility layers — rather than
arbitrary spatial thinning, so the manipulated conditions stay
traceable to a documented mechanism. Requires auxiliary covariates —
see [`datasets.md`](datasets.md#auxiliary--external-data), currently
undecided. Note: Dimson et al.'s bias axes were documented in Hawaiʻi;
whether the same axes dominate in this thesis's (not yet decided)
region should be checked against the actual data, not assumed by
default.

### Temporal-mismatch experiment (RQ4)

Compare temporal relationships between observations and satellite
imagery (example ranges, not final: same year, ±1, ±2, ±3 years),
constrained to ranges actually supported by the dataset.

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
**not** assume foundation models will perform better. It is motivated
by Ball et al. (2026) (fact 6), who empirically observe temporal
performance degradation (9–15% weighted-F1 decline across years) even
where labels are relatively systematic (curated forest inventories,
not citizen science) — suggesting reference-data quality and temporal
alignment can become the main bottleneck. This reframes the central
question from "are foundation models better?" toward:

> Under what reference-data conditions are foundation models actually
> useful for invasive plant mapping?

## Scope and Feasibility

> **Status: candidate prioritization, not a decision.** Added because
> RQ1–RQ4 were adopted before the actual datasets were explored
> (`datasets.md` still lists both citizen-science and satellite
> sources as "not yet decided").

**Blocking feasibility check (before finalizing RQ2/RQ4 experimental
design):** once real citizen-science data is obtained, compute basic
descriptive stats — observation count, spatial extent/clustering,
temporal range/spread — before committing to specific label-efficiency
percentages (RQ2) or temporal-mismatch windows (RQ4). If the dataset
is small or clustered in one or two years, the example levels/ranges
above may not be meaningful and should be revised.

**Reference-year / temporal-window discussion (2026-09-22):** a
partial answer to the blocking feasibility check above, using the
iNaturalist *Acacia*/Coimbra-district pilot (see
[`data/README.md`](../data/README.md); 7,943 observations — a pilot
for access validation, not a species/region decision).

Two candidate sources are single-year products regardless of anything
else chosen: OrtoSat and COS are both fixed at 2023. If either is
used, part of the pipeline is pinned to 2023 no matter what's decided
for the rest — making 2023 a natural (not inevitable) anchor to
propose, rather than an arbitrary pick.

On the pilot data, observation coverage around a 2023 anchor:

- exact year (2023): 3.4%
- ±1 year (2022–2024): 30.7%
- ±2 years (2021–2025): 80.3%
- ±3 years (2020–2026): 93.3%

TESSERA separately covers 2017–2025; 95.3% of pilot observations fall
within that window under nearest-available-year matching instead of a
fixed 2023 anchor. The observation-date distribution is uneven — 43%
of all pilot records are from 2021 alone, most likely an iNaturalist
adoption artifact rather than an ecological signal — so a fixed window
and nearest-year matching would not select the same, or an evenly
distributed, subset of observations.

Three candidate strategies, none yet chosen:

1. **Fixed window around 2023** (e.g. ±2 years) — one consistent
   dataset for RQ1–RQ3, simplest to report, but discards ~20% of pilot
   observations and still spans up to 4 years of mismatch within the
   window itself.
2. **Nearest-available-year matching per observation** — minimizes
   each observation's individual mismatch and retains ~95% of the
   data, at the cost of every observation being matched to a different
   reference year (less uniform to report as a single baseline).
3. **Treat the window itself as the RQ4 manipulated variable** — do
   not fix it for the mismatch experiment; construct multiple dataset
   versions at different mismatch levels and compare, per the
   [temporal-mismatch experiment](#temporal-mismatch-experiment-rq4)
   above. Applies to RQ4 only — RQ1–RQ3 still need one fixed default
   in the meantime.

**Open question, for supervisor discussion:** which of these (or
another) should be the RQ1–RQ3 default, and does the answer change
once the actual species/region — not just this Coimbra/*Acacia*
pilot — is decided?

**Candidate prioritization if the timeline is constrained:** RQ1 is
the prerequisite for the other three and the core deliverable. RQ2 and
RQ3 are next, each grounded in a specific verified paper (Ball et al.
2026; Dimson et al. 2023 respectively). RQ4 is the most exploratory —
most dependent on the dataset having usable multi-year spread — and
the first candidate to lighten or drop if time runs short. Revisit
after the feasibility check and supervisor discussion.

## Open Questions

- Literature basis is seven verified papers, not a systematic review —
  the gap claim needs revisiting after a broader search (Web of
  Science/Scopus/Google Scholar).
- **Resolved 2026-09-11:** cross-checked all seven papers' claims
  against fetched abstracts/summaries. Fixes made: added the missing
  Mouta et al. (2021) DOI; added Gillespie et al.'s study region
  (California) and Dimson et al.'s (Hawaiʻi, 4 species), both omitted
  before; strengthened Ball et al.'s bottleneck claim with the actual
  reported numbers (9–15% weighted-F1 decline across years) instead of
  paraphrasing it as a vague "flagged concern." Eskandari et al.
  (2025)'s specific figures remain unverified (publisher page blocks
  automated fetching) — see `literature_review.md`.
- **Resolved 2026-09-11:** Galicia/Iberia *Acacia* placeholder replaced
  with Domingo et al. (2023) and Eskandari et al. (2025) — see
  [Existing Research](#conventional-invasive-plant-mapping). The
  literal Sentinel-1+Sentinel-2-fusion-with-spatial-CV claim remains
  unverified for any single Galicia paper.
- **Resolved 2026-09-11:** the RQs above replaced the earlier
  data-integration/representation/performance/generalization framing
  in `research_questions.md` (discarded, not kept as an alternative).
- Whether the optional/secondary uncertainty- or
  observation-density-guided sampling idea (see
  [Research Questions](#research-questions)) is in scope given the
  timeline.
- Exact EO foundation model(s) (TESSERA, AlphaEarth, other) — depends
  on data availability, licensing, and further literature review.
- Exact conventional baseline model and feature set — depends on the
  dataset once explored (see `datasets.md`, `data/README.md`).
- Exact label-efficiency percentages, sampling-bias covariates, and
  temporal-mismatch ranges, and whether all four RQs run at full
  depth — see [Scope and Feasibility](#scope-and-feasibility).
- Whether "invasive plant(s)" means one species, several species, or a
  species-agnostic framing — affects how directly Cardoso et al.
  (2024) and Mouta et al. (2021) serve as precedents.
