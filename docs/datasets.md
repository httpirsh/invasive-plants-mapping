# Datasets

> **Status: to be developed.** No citizen-science or satellite data
> source has been selected yet. This document currently records the
> *candidates* under consideration and the open questions that need to
> be resolved before a source is chosen. Once a dataset is actually
> obtained, add its full provenance (source, URL, access date,
> license, spatial/temporal coverage, preprocessing) to
> [`data/README.md`](../data/README.md) and summarize the choice and
> rationale here.

High-level documentation of the datasets used in the thesis. Detailed,
per-dataset provenance is kept in [`data/README.md`](../data/README.md);
this document is for the broader narrative of what data is used and
why.

## Citizen Science Data

**Not yet decided.** No specific citizen-science platform or dataset
has been selected for this thesis. A pilot iNaturalist download (7,943
*Acacia* observations, Coimbra district) exists for access validation
only — see [`data/README.md`](../data/README.md) for full provenance;
it is not a scope decision.

Candidate sources seen in the reviewed literature (see
[`research_gaps.md`](research_gaps.md) /
[`literature_review.md`](literature_review.md)), listed here only as
examples of what other studies used, not as a decision for this
thesis:

- **iNaturalist** — used by Gillespie et al. (2024), Dimson et al.
  (2023), and (alongside social media) Cardoso et al. (2024). Leading
  candidate for this thesis (records available as CSV). **Reasonable
  proposal** (not yet a decision): a phased scope — start with
  observations in/around Coimbra as a small pilot area, then extend to
  continental Portugal once the pipeline is validated — to de-risk the
  "actual size/spread" open question below before committing to
  full-country scope.
- **GBIF** — aggregates iNaturalist and other citizen-science/
  biodiversity sources; not confirmed as used by any specific paper
  reviewed so far.

Open questions:

- Which platform(s) actually provide usable records for the target
  invasive species/region (see [Species and Region](#species-and-region-scope)
  below)?
- Does the thesis use a single platform or an aggregation (e.g. via
  GBIF)?
- What is the actual size, spatial spread, and temporal spread of the
  available records? This directly constrains the label-efficiency,
  sampling-bias, and temporal-mismatch experiments proposed in
  [`research_gaps.md`](research_gaps.md).

## Satellite / Earth Observation Data

**Not yet decided.** No specific satellite product or EO foundation
model has been selected for this thesis. Pilot downloads exist for
TESSERA (Coimbra municipality, 2024) and COS 2023 (full national
extent) to validate access — see
[`data/README.md`](../data/README.md) for full provenance; these are
not scope decisions. OrtoSat and Sentinel-1/2 are not yet obtained
(access/credentials pending, see `data/README.md#not-yet-obtained`).

Candidates under consideration, per
[`methodology.md`](methodology.md#foundation-model-philosophy) and
[`research_gaps.md`](research_gaps.md):

- **Sentinel-1 / Sentinel-2** — conventional radar/optical imagery,
  for the conventional spectral-temporal baseline. 10 m resolution,
  free/open access. Precedent: Mouta et al. (2021) used Sentinel-2 for
  *Acacia longifolia* mapping in Portugal. Currently the preferred
  candidate for the conventional baseline over OrtoSat (below), given
  open access and a directly comparable Portuguese precedent — **not
  yet a final decision**.
- **OrtoSat 30 cm** (dados.gov.pt, "Ortosat 30 cm Portugal Continental
  2023") — Pleiades-Neo satellite mosaic, 30 cm resolution, RGB + NIR
  (4 bands, 8-bit), continental Portugal, acquired Apr–Oct 2023,
  CC BY 4.0, Cloud Optimized GeoTIFF. **Open question / potential
  blocker:** the dataset page states full-resolution download is
  restricted to public-administration entities via signed terms of use
  (SharePoint, individual credentials); only WMS visualization is
  confirmed publicly accessible. Whether university/thesis access is
  possible needs confirming before relying on this source. No
  invasive-plant-mapping precedent found yet for this specific
  product.
- **TESSERA embeddings** (via [GeoTessera](https://geotessera.org),
  `pip install geotessera`) — EO foundation model, used in Ball et al.
  (2026). Concrete specs confirmed: 128-channel embeddings, 10 m
  resolution, built from Sentinel-1 + Sentinel-2, global coverage
  2017–2025, MIT license, accessible via a Zarr streaming API or
  direct tile download (Source Cooperative), no confirmed licensing
  barrier. This resolves part of the "which EO foundation model(s) are
  actually accessible" open question below in TESSERA's favor, though
  it is not yet a final choice over AlphaEarth or another model.
- **AlphaEarth embeddings** — EO foundation model, used in Ball et al.
  (2026). Access terms/licensing not yet confirmed for this thesis.
- Other EO foundation models — not ruled out; "another justified EO
  foundation model" is explicitly left open in
  [`research_gaps.md`](research_gaps.md#foundation-model-experiment-feeds-rq1).

Open questions:

- Which EO foundation model(s) are actually accessible (data
  availability, licensing, compute) for this project? TESSERA is
  confirmed freely accessible (see above); AlphaEarth's access terms
  are still unconfirmed.
- What spatial/temporal resolution and coverage do the candidate
  products offer over the target region, and is it sufficient to
  match the citizen-science observations' spatial/temporal extent?
  Note the resolution mismatch across candidates: Sentinel-2/TESSERA
  at 10 m vs. OrtoSat at 30 cm — mixing resolutions in a single
  baseline/comparison needs an explicit, justified choice, not an
  assumption.
- Whether embeddings will be used directly, fine-tuned, or combined
  with conventional features (see
  [`methodology.md`](methodology.md#foundation-model-philosophy)).
- Whether OrtoSat access (public-administration-only download terms)
  is obtainable for this thesis.

## Species and Region Scope

**Not yet decided.** Whether the thesis targets a single invasive
species, several species, or a species-agnostic invasive/non-invasive
framing is open — see the corresponding open question in
[`research_gaps.md`](research_gaps.md#open-questions). This choice
affects which citizen-science records and which regional satellite
coverage are relevant.

**Reasonable proposal, not a decision:** *Acacia* (e.g. other
broadleaf/"folhosas" species alongside *A. longifolia*) is a
strengthened candidate — it is the only genus with three prior
Iberian precedents already in [`literature_review.md`](literature_review.md#conventional-invasive-plant-mapping)
(Mouta et al. 2021, *A. longifolia*, Portugal; Domingo et al. 2023 and
Eskandari et al. 2025, *A. dealbata*/*Acacia* sp., Galicia), giving a
concrete benchmark to compare against.

## Auxiliary / External Data

**Not yet decided.** `data/external/` has placeholders for
shapefiles, land-cover products, and other auxiliary data
(e.g. administrative boundaries, existing land-cover maps) that may be
needed for sample construction or evaluation. No specific product has
been selected.

Candidate: **COS** (Carta de Uso e Ocupação do Solo), Portugal's
official national land-cover product. Not yet used in any experiment
design decision, but a natural fit for two already-open questions: the
negative/background-sample construction problem in
[`methodology.md`](methodology.md#dataset-construction), and the
land-cover-context dimension of
[error analysis](methodology.md#error-analysis-and-interpretation).

One candidate need, not yet confirmed: the RQ3 sampling-bias
experiment (see
[`research_gaps.md`](research_gaps.md#sampling-bias-experiment-rq3))
proposes grounding synthetic spatial-bias manipulation in the specific
bias axes Dimson et al. (2023) documented for citizen-science
invasive-plant data — roads/trails, general accessibility, and
disturbed vegetation — rather than arbitrary thinning. This would
require road/trail network and/or accessibility layers (e.g. from
OpenStreetMap or a national roads dataset) as auxiliary data. Whether
this is pursued depends on data availability and the feasibility check
in `research_gaps.md`.
