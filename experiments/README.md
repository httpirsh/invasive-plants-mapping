# Experiments

Configuration and organization for the controlled experiments that
compare modelling approaches. The exact experiments will be defined
once the baseline and foundation-model pipelines exist; see
[`docs/research_questions.md`](../docs/research_questions.md) for the
candidate experiment per research question.

| Folder | Purpose |
|---|---|
| `configs/` | Experiment configuration files |
| `baseline/` | Runs using conventional satellite-derived features |
| `foundation_model/` | Runs using Earth Observation Foundation Model embeddings |
| `fusion/` | Runs combining citizen science, conventional features and/or embeddings |
| `ablation/` | Ablation experiments isolating the contribution of each information source |
