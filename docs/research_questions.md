# Research Questions

> **Status: primary.** These research questions were adopted on
> 2026-09-11, replacing an earlier, more general framing (data
> integration / representation / model performance / generalization).
> The earlier framing is discarded, not kept as an alternative — see
> [`research_gaps.md`](research_gaps.md) for how this framing follows
> from the reviewed literature. The exact experimental design needed
> to answer these questions (models, foundation model choice,
> percentages, spatial/temporal splits) remains open — see
> [`methodology.md`](methodology.md) and
> [`research_gaps.md`](research_gaps.md#candidate-experiments).
>
> **Supervisor review (2026-10-17):** RQ1–RQ3 confirmed, with the
> wording refinements below.
>
> **RQ4 (temporal mismatch) eliminated (2026-10-17).** Not deferred —
> removed from scope entirely, along with the dedicated
> temporal-mismatch investigation (reference-year/window analysis,
> candidate mismatch experiment) that supported it. See
> [`research_gaps.md`](research_gaps.md) for what was removed.

## Main Research Question

How robust and data-efficient are Earth Observation foundation models
for invasive plant mapping when trained with citizen-science reference
data?

## Secondary Questions

### RQ1 — Foundation models vs. conventional approaches

To what extent do Earth Observation foundation-model representations
improve invasive plant mapping compared with conventional
spectral-temporal satellite features?

Related open questions: [Baseline Philosophy](methodology.md#baseline-philosophy), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy), [Evaluation Principles](methodology.md#evaluation-principles).

> *Supervisor wording (2026-10-17): "Até que ponto os foundation
> models melhoram as abordagens mais tradicionais?" — an
> extent/degree framing rather than yes/no; confirmed, no change in
> substance.*

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of available citizen-science
reference data decreases, when that reduction is induced through a
distribution-improving filter rather than uniform random sampling?

Related open questions: [Dataset Construction](methodology.md#dataset-construction), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy).

> **Supervisor refinement (2026-10-17):** apply a filter — acknowledged
> to have its own limitations — within an area with several
> observations, and examine *which* observations it removes and *why*,
> instead of discarding at random. The exact filter/criterion is not
> yet specified — see
> [`research_gaps.md`](research_gaps.md#label-efficiency-experiment-rq2).

### RQ3 — Spatial sampling bias

How does spatial sampling bias in citizen-science observations affect
invasive plant mapping performance, using conventional satellite
representations and EO foundation-model representations, when
evaluated across geographically distinct regions?

Related open questions: [Data Quality and Bias](methodology.md#data-quality-and-bias), [Validation Strategy](methodology.md#validation-strategy), [Ablation and Generalization](methodology.md#ablation-and-generalization).

> **Supervisor confirmation (2026-10-17):** the comparison should be
> made geographically, consistent with the existing
> [spatial-generalization experiment](research_gaps.md#spatial-generalization-experiment-cross-cutting-supports-evaluation-of-rq1rq4).

## Scientific Framing

This is a **hypothesis to investigate, not an assumed result** — do
not assume foundation models will outperform conventional approaches.
See [`research_gaps.md`](research_gaps.md#main-hypothesis) for the
full motivation: foundation models may reduce the need for feature
engineering while the bottleneck shifts to citizen-science
reference-data quality, quantity, and spatial distribution — i.e. the
thesis asks *under what conditions* foundation models are useful, not
only whether they are better in general.
