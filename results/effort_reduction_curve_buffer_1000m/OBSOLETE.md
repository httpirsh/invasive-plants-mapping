# OBSOLETE (2026-11-17)

Run under the superseded RQ1 protocol: presence-vs-background Random
Forest (background as pseudo-absence), ROC-AUC / Boyce, five random
20%-of-block holdouts. The RQ1 classifier is now the presence-only
logistic regression evaluated by sensitivity at a fixed area fraction
under leave-one-block-out; these numbers are not reported anywhere.
Reasoning: `thesis/notes.md#rq1-presence-only`. Kept for the record.
