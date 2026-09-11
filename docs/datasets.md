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
has been selected for this thesis.

Candidate sources seen in the reviewed literature (see
[`research_gaps.md`](research_gaps.md) /
[`literature_review.md`](literature_review.md)), listed here only as
examples of what other studies used, not as a decision for this
thesis:

- **iNaturalist** — used by Gillespie et al. (2024), Dimson et al.
  (2023), and (alongside social media) Cardoso et al. (2024).
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
model has been selected for this thesis.

Candidates under consideration, per
[`methodology.md`](methodology.md#foundation-model-philosophy) and
[`research_gaps.md`](research_gaps.md):

- **Sentinel-1 / Sentinel-2** — conventional radar/optical imagery,
  for the conventional spectral-temporal baseline. Precedent:
  Mouta et al. (2021) used Sentinel-2 for *Acacia longifolia* mapping
  in Portugal.
- **TESSERA embeddings** — EO foundation model, used in Ball et al.
  (2026).
- **AlphaEarth embeddings** — EO foundation model, used in Ball et al.
  (2026).
- Other EO foundation models — not ruled out; "another justified EO
  foundation model" is explicitly left open in
  [`research_gaps.md`](research_gaps.md#foundation-model-experiment).

Open questions:

- Which EO foundation model(s) are actually accessible (data
  availability, licensing, compute) for this project?
- What spatial/temporal resolution and coverage do the candidate
  products offer over the target region, and is it sufficient to
  match the citizen-science observations' spatial/temporal extent?
- Whether embeddings will be used directly, fine-tuned, or combined
  with conventional features (see
  [`methodology.md`](methodology.md#foundation-model-philosophy)).

## Species and Region Scope

**Not yet decided.** Whether the thesis targets a single invasive
species, several species, or a species-agnostic invasive/non-invasive
framing is open — see the corresponding open question in
[`research_gaps.md`](research_gaps.md#open-questions). This choice
affects which citizen-science records and which regional satellite
coverage are relevant.

## Auxiliary / External Data

**Not yet decided.** `data/external/` has placeholders for
shapefiles, land-cover products, and other auxiliary data
(e.g. administrative boundaries, existing land-cover maps) that may be
needed for sample construction or evaluation. No specific product has
been selected.
