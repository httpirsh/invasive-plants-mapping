# Research Questions

| Item | Status |
|---|---|
| Main question, RQ1–RQ3 | Adopted |
| Prediction task | Adopted |
| Absence generation, temporal design | Proposed |

Models, foundation-model choice, data percentages and spatial splits
are still open — see [`methodology.md`](methodology.md) and
[`research_gaps.md`](research_gaps.md#candidate-experiments).

## Main Question

How robust and data-efficient are Earth Observation foundation models
for invasive plant mapping when trained with citizen-science reference
data?

## Secondary Questions

### RQ1 — Foundation models vs. conventional approaches

To what extent do Earth Observation foundation-model representations
improve invasive plant mapping compared with conventional
spectral-temporal satellite features?

- A question of degree, not yes/no.
- All representations come from the same reference year, so only the
  representation changes between compared models.

Related: [Baseline Philosophy](methodology.md#baseline-philosophy), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy), [Evaluation Principles](methodology.md#evaluation-principles).

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of available citizen-science
reference data decreases, when that reduction is induced through a
distribution-improving filter rather than uniform random sampling?

- The filter is applied in an area with many observations, reporting
  *which* observations it removes and *why*. The filter itself is not yet
  specified — see
  [`research_gaps.md`](research_gaps.md#label-efficiency-experiment-rq2).
- Reduction is applied within the fixed observation window.
- The disturbance filter (see [Temporal Design](#temporal-design-proposed))
  is a candidate component, since it removes observations for a
  documented reason.

Related: [Dataset Construction](methodology.md#dataset-construction), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy).

### RQ3 — Spatial sampling bias

How does spatial sampling bias in citizen-science observations affect
invasive plant mapping performance, using conventional satellite
representations and EO foundation-model representations, when
evaluated across geographically distinct regions?

- The comparison is geographic, as in the
  [spatial-generalization experiment](research_gaps.md#spatial-generalization-experiment-cross-cutting-supports-evaluation-of-rq1rq3).
- A single reference year keeps observation year from correlating
  with geography, so spatial effects are not confounded with time.
- The absence strategy affects the bias being measured: a
  target-group background shares the presences' bias and partly
  corrects it. Results must state which background was used;
  target-group vs. random background is a candidate experiment.
- The 2021 peak must be checked spatially: a local campaign or a few
  very active observers would itself be an instance of sampling bias.

Related: [Data Quality and Bias](methodology.md#data-quality-and-bias), [Validation Strategy](methodology.md#validation-strategy), [Ablation and Generalization](methodology.md#ablation-and-generalization).

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

### Absence Generation (proposed)

iNaturalist is presence-only, so pseudo-absences are needed. This is
the most consequential open decision: it shapes dataset construction,
evaluation, and the interpretation of RQ3.

**Proposal: target-group background** — iNaturalist observations of
*other plant species*. They share the observers, platform and places
of the *Acacia* presences, so the model learns *Acacia* vs. other
vegetation, not visited vs. unvisited places.

**Comparison: random background** — points sampled uniformly over the
study area. Simple, but with biased presences the model may learn
accessibility (roads, urban edges) instead of the species.

Rules to confirm:

- Same observation window and disturbance filter as the presences.
- Exclusion buffer around *Acacia* observations, since another
  plant's point may fall in an *Acacia*-dominated pixel (distance
  open).
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
| Citizen science (*Acacia*, Coimbra pilot) | 1992–2026; 43% of records from 2021 (likely an iNaturalist-adoption artifact) |

Pilot observations retained per window:

| Window | Years | Retained |
|---|---|---|
| exact | 2023 | 3.4% |
| ±1 | 2022–2024 | 30.7% |
| ±2 | 2021–2025 | 80.3% |
| ±3 | 2020–2026 | 93.3% |

Why ±2:

- Any narrower window drops 2021, where most of the data is.
- *Acacia* stands persist for years, so presence in 2021 or 2025 is
  strong evidence of presence in 2023 unless disturbed.
- Every model sees the same period, so differences come from
  representation, data quantity or spatial distribution — not time.

Rejected:

- **Nearest available year per observation:** mixes years in the
  presences while absences and test data stay at 2023 (the model
  could learn the year instead of *Acacia*), correlates year with
  geography (confounding RQ3), and makes time a hidden variable.
- **Window as an experimental variable:** temporal mismatch is out of
  scope.

Safeguards:

- **Disturbance filter:** remove (and count) observations inside ICNF
  burned areas between their observation year and 2023.
- **Window sensitivity check:** re-run RQ1 with ±1, ±2 and ±3 windows
  and check whether the ranking of representations holds. This tests
  a design choice; an unstable ranking would itself be a finding.

Variant to discuss — **asymmetric window** (e.g. 2021–2026):
observations after 2023 are stronger evidence of 2023 presence than
earlier ones, which may since have been burned or cleared. Note that
2026 is incomplete.

## Open Points

- Target-group background as the absence strategy, and its rules
  (target group, buffer, class ratio).
- 2023 as reference year and ±2 years as the default window.
- Symmetric (2021–2025) vs. asymmetric (e.g. 2021–2026) window.
- Disturbance filter: fixed pre-processing step or part of the RQ2
  filter?
- How to handle the 2021 peak if it is spatially concentrated.

## Scientific Framing

A **hypothesis to investigate, not an assumed result** — foundation
models are not assumed to outperform conventional approaches. They
may reduce feature engineering while the bottleneck shifts to the
quality, quantity and spatial distribution of citizen-science data;
the thesis asks *under what conditions* they are useful. Temporal
alignment is controlled rather than studied. See
[`research_gaps.md`](research_gaps.md#main-hypothesis).
