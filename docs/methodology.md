# Methodology

> **Status: preliminary guiding principles.** The concrete methodology
> is not fixed and is expected to be refined through literature review
> and data exploration. Where a choice below is undecided, it is
> marked as an **open question**, not a decision.

## Research Progression

The project generally follows this progression, though it is a
roadmap rather than a rigid pipeline — the methodology may change as
new evidence is found:

```text
problem
→ literature review
→ research gap
→ research questions
→ understand citizen science data
→ understand satellite data
→ define prediction task
→ construct modelling dataset
→ define validation strategy
→ conventional EO baseline
→ EO foundation-model approach
→ RQ1: compare representations
→ RQ2: reduce amount of citizen-science reference data
→ RQ3: investigate spatial sampling bias
→ RQ4: investigate temporal mismatch
→ spatial/generalization evaluation
→ error analysis
→ final mapping
→ conclusions
```

See [`research_gaps.md`](research_gaps.md) for the research gap
analysis and [`research_questions.md`](research_questions.md) for the
current research questions (RQ1–RQ4).

## Problem and Task Definition

The exact machine learning task is an **open question** and must be
defined based on the research questions, literature, and available
data.

"Mapping invasive alien plants" may involve different formulations,
such as classification, presence/absence prediction, probability
mapping, or segmentation. The chosen formulation should be explicitly
defined before the final experimental design.

The task definition should specify:

- what constitutes a prediction unit (e.g. point, pixel, patch, or
  spatial cell)
- what the target/label represents
- the spatial and temporal scope of the prediction
- what constitutes a positive and negative example

The final task formulation should be justified rather than assumed.

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

## Data Quality and Bias

Data quality should be assessed before modelling.

For citizen science data, consider:

- missing or inconsistent values
- duplicate observations
- coordinate accuracy
- taxonomic consistency
- temporal coverage
- uneven spatial sampling
- observer or accessibility bias

For satellite data, consider:

- cloud contamination
- missing observations
- spatial resolution
- temporal coverage
- sensor limitations
- alignment between satellite observations and citizen science
  observations

Potential sources of bias and their implications for model training
and evaluation should be documented.

## Dataset Construction

The construction of the modelling dataset is a distinct methodological
step between data exploration and model training.

Conceptually:

```text
citizen science observations
            +
satellite / Earth Observation data
            ↓
      sample construction
            ↓
      labels + features
            ↓
      modelling dataset
```

Important open questions include:

- how citizen science observations are converted into labels
- how satellite observations are associated with citizen science
  locations and dates
- the spatial unit used to extract satellite information
- the temporal window used around observations
- how duplicate or uncertain observations are handled
- how negative/background samples are constructed
- how sampling bias in citizen science data is accounted for

A missing citizen science observation must not automatically be
interpreted as evidence of species absence. The strategy for creating
negative/background samples must therefore be justified using the
literature and characteristics of the available data.

## Validation Strategy

The validation strategy should be considered before the main
experiments are designed.

Potential considerations include:

- train/validation/test splits
- spatially independent validation
- temporal validation, where relevant
- spatial leakage
- spatial autocorrelation
- class imbalance
- geographic generalization

A random train/test split should not be used automatically when
spatial proximity may cause observations in the training and test sets
to be highly similar.

The final validation strategy is an **open question** and should be
justified based on the task, dataset structure, and literature.

## Baseline Philosophy

A baseline is the simplest credible approach against which more
advanced approaches are compared. An important initial baseline is
expected to be conceptually similar to:

```text
citizen science observations → labels / observation locations
                                        +
satellite imagery → conventional spectral and/or temporal features
                                        ↓
                          conventional ML model
```

Candidate conventional models (not a final choice): Random Forest,
Logistic Regression, XGBoost, or other appropriate methods.

The baseline should answer: *how well can invasive plant mapping be
addressed without Earth Observation Foundation Models?*

It should be established early enough to provide a meaningful
comparison, but not over-optimized before the wider methodology
(especially the foundation-model approach) is understood.

## Foundation Model Philosophy

Foundation models are a central research component, but the following
are **open questions**, not decisions:

- Which foundation model(s) will be used
- Whether embeddings, fine-tuning, or another integration method is used
- Whether the underlying task is classification, segmentation,
  retrieval, or something else
- Which spatial and/or temporal representation is most appropriate

A possible conceptual comparison:

```text
Conventional:
satellite imagery → spectral/temporal features → ML → prediction

Foundation model:
satellite imagery → EO foundation model → embedding → ML → prediction

Fusion:
citizen science + satellite features + embeddings → ML → prediction
```

These are research hypotheses / possible experimental designs, not
assumptions about the final methodology.

## Experimental Philosophy

Experiments should be designed to answer specific research questions,
not because they are technically interesting. Whenever possible,
compare controlled alternatives and change one important factor at a
time.

Possible experiment families include:

- conventional satellite-feature baselines
- spectral + temporal feature approaches
- foundation-model representation approaches
- data fusion
- ablation studies
- spatial or temporal generalization

Every important experiment should record:

- purpose
- hypothesis/question
- input data
- methodology
- evaluation procedure
- result
- interpretation

Details and the running experiment log live in
[`docs/experiments.md`](experiments.md).

## Ablation and Generalization

Ablation experiments may be used to understand the contribution of
individual components by systematically removing or changing them.

For example, a final approach may be compared with versions where
specific feature groups, data sources, or model components are removed.

Generalization experiments may evaluate whether the model performs
reliably on spatially or temporally independent areas.

The exact ablation and generalization strategies are open questions
and should be introduced when they help answer a specific research
question.

## Evaluation Principles

Evaluation is a core part of the research, not an afterthought.

Candidate metrics (final choice depends on the task):

- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC

Always consider:

- class imbalance, and the cost of false positives vs. false negatives
- spatial leakage and spatial autocorrelation
- geographic generalization
- temporal generalization, where relevant

Never report a metric without stating what was evaluated, on which
dataset, and under which split/validation strategy.

## Error Analysis and Interpretation

Model evaluation should not rely exclusively on aggregate metrics.

After the main experiments, analyse where and under which conditions
the models succeed or fail.

Possible dimensions include:

- species
- geographic region
- temporal period
- environmental or land-cover context
- observation density
- quality of citizen science observations

The purpose is to understand model behaviour, limitations, and
possible sources of error, not only to identify the model with the
highest metric.

## Final Mapping

The final stage may produce spatial predictions or maps over the study
area.

The final mapping procedure should document:

- the spatial prediction unit
- the area being mapped
- how predictions are converted into a map
- any thresholds applied
- uncertainty or confidence information, where available

The final maps should be interpreted in the context of the validation
results and known limitations of the data and methodology.

## Reproducibility

Experiments should be reproducible whenever reasonably possible.

Record:

- dataset and version
- preprocessing choices
- model configuration
- hyperparameters
- random seeds where relevant
- train/validation/test strategy
- evaluation metrics
- important assumptions

Important methodological decisions should be documented rather than
left only inside notebooks.

Use:

- `docs/` for methodological decisions and project knowledge
- `experiments/` for experiment organization and configuration
- `results/` for generated outputs
- `notebooks/` for exploration, prototyping, and analysis

## Methodology Evolution

This document describes the **current methodological thinking**, not
the final thesis methodology.

As the project develops:

- update open questions when they become decisions
- document important changes and their rationale
- avoid silently replacing previous methodological assumptions
- keep the final methodology consistent with the research questions
  and experimental evidence

The final thesis methodology should be based on the evidence gathered
through literature review, data exploration, experiments, and
validation.
