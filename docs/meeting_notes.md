# Next Supervisor Meeting — Agenda

> Prepared 2026-10-17. Goal: get decisions, not just discussion. Each
> item comes with a recommendation; the supervisor approves, adjusts
> or rejects it. Items are ordered by how much of the pipeline they
> condition. Points marked [added] came from checking the agenda
> against the pilot data and docs.

## 0. Key finding to open with [added]

The pilot is dominated by a single observer:

| Records | Share from top observer |
|---|---|
| All | 83.2% |
| 2021 (3,405 records) | 98.1% |
| 2019–2022 | 91–98% per year |
| 2023 / 2025 | 35% / 31% |
| Inside 2021–2025 window | 85.5% |

The 2021 peak is one observer, not an iNaturalist-adoption effect or a
bioblitz. This affects items 1, 3 and 4 below.

## 1. Absence generation (most consequential decision)

**Context.** iNaturalist is presence-only. How pseudo-absences are
generated conditions dataset construction, evaluation, and the
interpretation of RQ3.

**Proposal: target-group background** — use iNaturalist observations
of other plant species as pseudo-absences. Standard technique in
species distribution modelling (Phillips et al. 2009, see
`literature.md`). [added]

**Arguments to present.**
- Same observers, same platform, same accessible places as the
  *Acacia* presences → shares their spatial bias, so the model learns
  *Acacia* vs. other vegetation rather than "visited vs. unvisited
  places".
- Random background lets the model learn accessibility (roads, urban
  edges) instead of the species.
- Caveat to raise openly: because it corrects part of the spatial
  bias, the absence strategy interacts with RQ3.
- Caveat [added]: the method assumes presences and background come
  from the same sampling process. Here 85% of presences come from one
  observer, while "other plants" come from the whole community — the
  footprints may not match. Check what this observer recorded besides
  *Acacia*.
- Caveat [added]: pseudo-absences are not true absences, so metrics
  against them measure separation from background, not real accuracy
  (see item 2).

**Questions.**
- [ ] Approve target-group background?
- [ ] Which plants form the target group: all vascular plants, or a
  restricted group (e.g. woody species)?
- [ ] Restrict the background to the dominant observer's own
  non-*Acacia* records, or use the whole community? [added]
- [ ] Exclusion buffer around *Acacia* observations (10 m pixels: an
  understorey plant may sit under *Acacia* canopy) — what distance?
- [ ] Presence:background ratio — 1:1, or higher with class weighting?
- [ ] Compare target-group vs. random background as part of RQ3?

## 2. Independent validation reference [added]

If training and test data both come from the same biased
citizen-science source, the bias stays hidden — exactly what RQ3 is
about.

- [ ] Which independent reference: COS 2023, OrtoSat (if access is
  possible), other?

## 3. Temporal reference design

**Context.** With temporal mismatch out of scope, time must be held
constant for RQ1–RQ3. OrtoSat is 2023 only and COS 2023 is the most
recent COS edition, which already pins part of the pipeline to that
year.

**Proposal.**
- Single reference year: **2023** for Sentinel-2, TESSERA and
  COS/OrtoSat.
- Observation window: **2023 ± 2 years (2021–2025)**, retaining
  ~80% of pilot observations. Applies to presences *and* background.

**Arguments to present.**
- ±1 year keeps only 30.7%: it drops 2021, which holds 43% of all
  records. ±2 is the first window that does not discard most of the
  data.
- Say openly [added]: 85.5% of the records kept by ±2 are from one
  observer, so the window mainly preserves that observer's data.
- *Acacia* is persistent, so presence within ±2 years is a good proxy
  for presence in 2023, unless disturbed.
- Alternative rejected: nearest-year matching per observation (mixes
  years between presences and absences/test data → possible shortcut;
  correlates year with geography → confounds RQ3).

**Questions.**
- [ ] Approve 2023 + ±2 years?
- [ ] Symmetric (2021–2025) or asymmetric (e.g. 2021–2026)?
  Argument for asymmetric: a 2025 observation is stronger evidence of
  presence in 2023 than a 2021 one.

## 4. Safeguards for the temporal window

- **Disturbance filter:** remove observations (presences and
  background) inside ICNF burned areas between observation year and
  2023.
  - Framing [added]: *Acacia* is fire-adapted — in central Portugal,
    burning promoted *A. dealbata* seed germination and stands
    persisted (Riveiro et al. 2025, see `literature.md`). The reason
    to remove burned observations is that the 2023 pixel no longer
    matches the label (burned ground, young regrowth), not that the
    species is gone.
  - [ ] Fixed pre-processing step, or part of the RQ2 filter ("which
    observations are removed and why")?
- **Window sensitivity analysis:** re-run RQ1 with ±1/±2/±3 and check
  whether the model ranking holds.
  - Design fix [added]: ±1 keeps only 31% of the data, so a ranking
    change could come from less data (RQ2), not from the window.
    Subsample ±2 and ±3 to the ±1 sample size so only the window
    changes.
  - [ ] Agree that this is a robustness check, not a study of
    temporal mismatch?

## 5. The 2021 peak

- Already checked [added]: 98.1% of 2021 records come from one
  observer (see item 0).
  - [ ] Keep as is, thin per observer, or use it explicitly as the
    bias case in RQ3?

## 6. RQ2 filter (still undefined)

- Bring 1–2 candidate filters (e.g. spatial thinning: at most one
  observation per cell / minimum distance; quality: research grade,
  coordinate uncertainty threshold).
  - [ ] Which criterion to start with?

## 7. Second region for RQ3 [added]

RQ3 compares across geographically distinct regions; the pilot is one
region dominated by one observer.

- [ ] Which second region?

## 8. Study area and species scope [added]

- The iNaturalist and TESSERA pilots use different Coimbra boundaries
  (district vs. municipality).
- [ ] Which study-area boundary?
- [ ] Genus *Acacia*, or a single species?

## 9. Prediction task (confirm)

**Adopted:** pixel-level binary classification trained on points
(10 m pixel at each observation), applied to every pixel of the study
area → complete map.

- Segmentation rejected (needs dense masks; citizen science gives
  points).
- Grid cells kept as a secondary step: aggregation of pixel
  predictions for evaluation and SDM-style comparison.

**Questions.**
- [ ] Confirm the task definition.
- [ ] Grid-cell size for the aggregation step?

## 10. Confirm what is already fixed

- RQ1–RQ3 as in `research_questions.md`; temporal mismatch out of
  scope.
- Temporal alignment is *controlled*, not *studied*, in the current
  scope — check that the supervisor agrees with this framing in the
  thesis text.

## Bring to the meeting

- Map of *Acacia* presences vs. candidate target-group background
  (shows whether the two share the same spatial footprint).
- Same map split by the dominant observer vs. everyone else. [added]
- Counts: *Acacia* observations vs. other-plant observations in the
  window (determines feasible class ratios).
- Table: share of observations per window (exact / ±1 / ±2 / ±3).
- Histogram of observations per year (shows the 2021 peak), split by
  dominant observer vs. others. [added]
- Map of 2021 observations vs. other years.
- Overlay of observations with burned areas, with the number of
  points that would be removed.
