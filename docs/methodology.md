# Methodology

> **Status: preliminary guiding principles.** The concrete methodology
> is not fixed and is expected to be refined through literature review
> and data exploration. Where a choice below is undecided, it is
> marked as an **open question**, not a decision.

## Research Progression

The project generally follows this progression, though it is a
roadmap rather than a rigid pipeline — the methodology may change as
new evidence is found:

```
problem
→ research questions
→ literature review
→ understand citizen science data
→ understand satellite data
→ integrate datasets
→ establish baseline
→ investigate foundation models
→ design experiments
→ evaluate models
→ generate maps
→ analyse errors
→ answer research questions
→ conclusions
```

## Citizen Science vs. Satellite Data

These are treated as conceptually different sources:

- **Citizen science observations** may provide species information,
  geographic locations, observation dates, and/or labels/training
  information.
- **Satellite/Earth Observation data** may provide spectral
  information, temporal information, spatial context, derived
  features, and/or learned representations (embeddings).

**Open question:** whether citizen science observations should be
used as ordinary model features, as the source of labels only, or
both. This must be determined from the available dataset, the
literature, and the research questions — it should not be assumed.

## Baseline Philosophy

A baseline is the simplest credible approach against which more
advanced approaches are compared. An important initial baseline is
expected to be conceptually similar to:

```
citizen science observations → labels / observation locations
                                        +
satellite imagery → conventional spectral and/or temporal features
                                        ↓
                          conventional ML model
```

Candidate conventional models (not a final choice): Random Forest,
Logistic Regression, XGBoost, or other appropriate methods.

The baseline should answer: *how well can invasive plant mapping be
addressed without Earth Observation Foundation Models?* It should be
established early enough to provide a meaningful comparison, but not
over-optimized before the wider methodology (especially the
foundation-model approach) is understood.

## Foundation Model Philosophy

Foundation models are a central research component, but the following
are **open questions**, not decisions:

- Which foundation model(s) will be used
- Whether embeddings, fine-tuning, or another integration method is used
- Whether the underlying task is classification, segmentation,
  retrieval, or something else

A possible conceptual comparison:

```
Conventional:  satellite imagery → spectral/temporal features → ML → prediction
Foundation model: satellite imagery → EO foundation model → embedding → ML → prediction
Fusion: citizen science + satellite features + embeddings → ML → prediction
```

These are research hypotheses / possible experimental designs, not
assumptions about the final methodology.

## Experimental Philosophy

Experiments should be designed to answer specific research questions,
not because they are technically interesting. Whenever possible,
compare controlled alternatives.

Possible experiment families (examples, not a fixed plan):

- conventional satellite-feature baselines
- spectral + temporal feature approaches
- foundation-model representation approaches
- data fusion (citizen science + satellite + embeddings)
- feature/data ablation
- generalization experiments (spatially independent evaluation)

Every important experiment should record: purpose, hypothesis/question,
input data, methodology, evaluation procedure, result, and
interpretation. Details and the running experiment log live in
[`docs/experiments.md`](experiments.md).

## Evaluation Principles

Evaluation is a core part of the research, not an afterthought.
Candidate metrics (final choice depends on the task): Precision,
Recall, F1, ROC-AUC, PR-AUC.

Always consider:

- class imbalance, and the cost of false positives vs. false negatives
- spatial leakage and spatial autocorrelation
- geographic generalization (spatially independent validation should
  be considered carefully — a random train/test split may leak
  information when spatial proximity correlates with label similarity)
- temporal generalization, where relevant

Never report a metric without stating what was evaluated, on which
dataset, and under which split/validation strategy.
