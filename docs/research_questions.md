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

## Main Research Question

How robust and data-efficient are Earth Observation foundation models
for invasive plant mapping when trained with citizen-science reference
data?

## Secondary Questions

### RQ1 — Foundation models vs. conventional approaches

Do Earth Observation foundation-model representations improve
invasive plant mapping compared with conventional spectral-temporal
satellite features?

Related open questions: [Baseline Philosophy](methodology.md#baseline-philosophy), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy), [Evaluation Principles](methodology.md#evaluation-principles).

### RQ2 — Data efficiency

How does the performance of EO foundation models compare with
conventional approaches as the amount of available citizen-science
reference data decreases?

Related open questions: [Dataset Construction](methodology.md#dataset-construction), [Foundation Model Philosophy](methodology.md#foundation-model-philosophy).

### RQ3 — Spatial sampling bias

How does spatial sampling bias in citizen-science observations affect
invasive plant mapping using conventional satellite representations
and EO foundation-model representations?

Related open questions: [Data Quality and Bias](methodology.md#data-quality-and-bias), [Validation Strategy](methodology.md#validation-strategy), [Ablation and Generalization](methodology.md#ablation-and-generalization).

### RQ4 — Temporal mismatch

How does temporal mismatch between citizen-science observations and
satellite imagery affect invasive plant mapping performance, and does
the effect differ between conventional and foundation-model
representations?

Related open questions: [Data Quality and Bias](methodology.md#data-quality-and-bias), [Dataset Construction](methodology.md#dataset-construction), [Validation Strategy](methodology.md#validation-strategy).

## Scientific Framing

This is a **hypothesis to investigate, not an assumed result**: do not
assume foundation models will outperform conventional approaches.

The possible scientific insight is that foundation models may reduce
the need for sophisticated satellite feature engineering, while the
main bottleneck shifts to the quantity, quality, spatial distribution,
and temporal alignment of citizen-science reference data — i.e. the
thesis investigates *under what reference-data conditions* EO
foundation models are actually useful for invasive plant mapping, not
only whether they are better in general. See
[`research_gaps.md`](research_gaps.md#main-hypothesis) for the full
motivation.
