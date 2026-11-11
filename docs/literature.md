# Literature

A small set of directly relevant papers, **not** a systematic review.
"Appears underexplored" claims reflect this reading list only and
must be revisited after a broader search (protocol in
[`thesis/notes.md`](../thesis/notes.md#protocolo-de-pesquisa-da-literatura)).

Several papers are now read in full (marked "Read" below); the rest
still have summaries written with help from abstracts, publisher
pages and quick skims only, and must be checked against the paper
before citing details in the thesis. Each paper has a status:

- **Read** — full text read, summary confirmed against it.
- **To read** — summary not yet confirmed by reading the paper.
- **To find** — only seen in a reference list; the paper itself has
  not been located.
- **Not read** — full text located but inaccessible (e.g. paywalled or
  blocked); summary is from a secondary source only, not to be cited.

Suggested reading order (papers that support the most decisions in
[`research_questions.md`](research_questions.md) and
[`methodology.md`](methodology.md) first): Ball 2026, Phillips 2009,
Dimson 2023, Riveiro 2025, Gillespie 2024, Karasiak 2022; then
Domingo 2023, Mouta 2021, Eskandari 2025, Martins 2016; then Brown
2025, Feng 2025; then Zhu 2026, Yang 2026, Ratsakatika 2026, Meyer &
Pebesma 2021; then Rivier 2023/2024, Raine et al. 2022, Liu et al. 2026, Zhang et
al. 2025 (timberline) (segmentation-mask candidates); Zhang et al.
2021 (WTS) and Wölk et al. 2026 lowest priority (unread/inaccessible,
low confirmed relevance so far, not pursued further for now).

## Papers

### EO foundation models

**Brown et al. (2025).** AlphaEarth Foundations: An embedding field
model for accurate and efficient global mapping from sparse label
data. arXiv:2507.22291. — *To read*

The AlphaEarth paper. Annual 64-dimensional embeddings at 10 m, used
without re-training; reported to outperform other featurization
approaches across mapping evaluations. **Directly relevant:** its
biodiversity evaluation already uses GBIF research-grade iNaturalist
observations, at genus level (including tree genera). So "embeddings +
iNaturalist labels" is not new on its own; what is new is invasive
plants, explicit bias evaluation and a conventional baseline under
the same labels.

**Feng et al. (2025).** TESSERA: Temporal Embeddings of Surface
Spectra for Earth Representation and Analysis.
[PDF](https://anil.recoil.org/papers/2025-tessera.pdf) — *To read*

The TESSERA paper. Pixel-wise model on annual Sentinel-1 + Sentinel-2
time series, 128-dimensional embeddings at 10 m. Evaluated on tree
species (Germany), crops (Austria) and biomass. Code open (MIT);
model weights on request; embeddings via GeoTessera. Needed as the
primary reference for the chosen foundation model.

**Ball et al. (2026).** Geospatial foundation models enable
data-efficient tree species mapping in temperate mountain forests.
*Science of Remote Sensing*, 14, 100466.
DOI: [10.1016/j.srs.2026.100466](https://doi.org/10.1016/j.srs.2026.100466)
— paywalled; methods confirmed from the authors' own code
([`PatBall1/trentino-trees`](https://github.com/PatBall1/trentino-trees),
`src/data_acquisition/s1s2annual.js` and `s1s2seasonal.js`), not the
paper's prose, which I haven't read in full.

Compares TESSERA embeddings, AlphaEarth embeddings and conventional
Sentinel-1 + Sentinel-2 features for 18 tree species/groups
(parcel-level forest inventories) in Trentino, Italy.

**Conventional Sentinel-2 baseline, confirmed from source
code:** Sentinel-2 SR (`COPERNICUS/S2_SR_HARMONIZED`),
cloud/shadow-masked per scene (SCL classes 4/5/6/7 kept, 0/1/3/8/9/10/11
dropped, plus QA60 opaque-cloud/cirrus bits), scenes with
`CLOUDY_PIXEL_PERCENTAGE < 60` only. Two composite variants, both
tested: **(a) annual** — single per-pixel median of all 12 bands
(B01–B12, B8A) over the calendar year, plus NDVI, NDWI (McFeeters) and
NBR computed on that median; **(b) seasonal** — the same but three
separate medians (spring Mar–May, summer Jun–Aug, autumn Sep–Nov), each
with its own NDVI/NDWI/NBR, i.e. 45 Sentinel-2 features. Sentinel-1
VV/VH (dB, plus VV−VH and VV/VH) added the same way, annual or
seasonal, as an optional second sensor. All exported on a fixed 10 m
UTM grid. Which variant (annual vs. seasonal) is the one reported as
"the" conventional baseline in the paper's headline numbers below is
**not confirmed** — the repository exposes both as working scripts
without saying which is primary.

- Embeddings beat conventional composites (weighted F1 0.83 vs. 0.80;
  macro F1 0.55 vs. 0.50).
- Near-optimal accuracy with ~5% of training parcels.
- A compact neural network was the best classifier, beating Random
  Forest; linear classifiers on embeddings underperformed neural
  networks on conventional composites.
- Robust to moderate label impurity; soft labels (species
  proportions) beat hard labels (macro F1 0.586–0.589).
- Performance degraded across years (weighted F1 −9% TESSERA, −15%
  AlphaEarth), hitting rare species hardest.

Conclusion: foundation models shift the bottleneck from feature
engineering to the availability, quality and temporal alignment of
reference data. Reference labels here are curated, not citizen
science.

Relevance beyond RQ1/RQ2: the cross-year degradation supports holding
time constant ([Temporal Design](research_questions.md#temporal-design-adopted));
the label-impurity result is relevant to the label-purity step of the
[Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed).

### Spatial transfer of embeddings

Evidence that embedding advantages shrink outside the training
region — the basis for RQ3's amplify-or-mitigate question.

**Zhu et al. (2026).** Earth Embeddings. arXiv:2608.03410. — *To read*

Review of geospatial embeddings in applications. Reports that
embeddings are competitive when trained and evaluated locally but
less robust under spatial transfer, and argues they work "in a
narrower and more practical sense" than foundation-model narratives
suggest. Useful framing for the thesis hypothesis.

**Yang et al. (2026).** Evaluating the Performance of AlphaEarth
Foundation Embeddings for Irrigated Cropland Mapping Across Regions
and Years. *Remote Sensing*, 18(7), 1065.
DOI: [10.3390/rs18071065](https://doi.org/10.3390/rs18071065)
— *To read*

Random forests on AlphaEarth embeddings for irrigated cropland (China,
USA). Reported (by a citing paper) as high accuracy with stable
transfer between years but weaker generalisation across regions.

**Ratsakatika, Zotta, Keshav & Lines (2026).** Geospatial embeddings
detect old-growth forests but buffered spatial validation narrows
their advantage over Sentinel features. arXiv:2609.28194 (preprint,
v1, 23 Sep 2026). — *Abstract and the area-of-applicability sections
(2.9, 3.5, 4.6) read; the rest not yet*

Old-growth forest mapping over 211 893 ha of Romania's Southern
Carpathians, expert-informed labels, AlphaEarth, TESSERA v2 and
Sentinel-1/2 features added to a topographic/access baseline,
spatially blocked validation with and without 10 km train–test
buffers. Unbuffered, TESSERA reaches PR-AUC 0.84 and beats
Sentinel-1/2 by +0.08 [+0.05, +0.11]; with a 10 km buffer the
advantage narrows to +0.04 [−0.01, +0.11], consistent with no
difference. The closest existing result to the question of whether
foundation-model gains survive spatial separation.

Also computes the area of applicability (Meyer & Pebesma, 2021 — see
[Spatial validation](#spatial-validation)) for its deployed model:
98.4% of forest inside the study area is within it, 65.0% across the
whole Carpathians, and the area outside is read as where new labels
would contribute most. Done for one model only, not compared between
feature sets, and the authors state that applicability "refers to
feature-space support rather than model accuracy, which was not
tested outside the AOI or verified in the field" — the part a test
against independent reference data would add.

### EO foundation models in related applications

Listed to show RQ1 alone is not novel; skim only.

- **Atoll ecosystem mapping** (*Remote Sensing* 18(17), 2964, 2026;
  DOI: [10.3390/rs18172964](https://doi.org/10.3390/rs18172964)):
  AlphaEarth 2023 embeddings vs. Sentinel-2 bands and indices,
  Maldives; embeddings better for most classes. Same 2023 reference
  year and same comparison design as RQ1. — *To read*
- **Gonçalves et al. (2026).** Evaluating AlphaEarth and TESSERA
  Geospatial Embeddings for Machine Learning-Based Burned Area
  Mapping in Portugal. Found only in a reference list; venue to
  check. Portuguese precedent for both embeddings — check whether
  the authors are from Coimbra/INESC. — *To find*

### Citizen science + remote sensing + plant mapping

**Gillespie et al. (2024).** Deep learning models map rapid plant
species changes from citizen science and remote sensing data.
*PNAS*, 121(37), e2318296121.
DOI: [10.1073/pnas.2318296121](https://doi.org/10.1073/pnas.2318296121)
— *Read (full text)*

Deepbiosphere: 650,000+ research-grade (mostly iNaturalist)
observations of 2,221 plant species, paired with remote sensing and
deep learning, in California only. Beats conventional SDM baselines
(AUC 0.95 vs. 0.88). No EO foundation models, no focus on invasive
species or data sparsity/bias.

Each point is paired with one 256×256 m, 1 m/pixel NAIP image
**centred on the point**, and the model predicts per-image species
presence — not a per-pixel mask grown from the point. CALVEG
vegetation-class maps appear only in a post-hoc case study, to
validate predictions against an independent map (per-pixel label =
the alliance with the largest area overlap), not to generate training
labels from points. GPS handling: keep only points with coordinate
uncertainty ≤120 m, drop near-duplicates within 150 m; no snapping or
correction of the coordinate itself. **Not a precedent for the
"nearest vegetation area" rule** (see
[`research_questions.md`](research_questions.md#prediction-task-adopted)):
the point→pixel-neighbourhood link here is a fixed 256 m window
around the point, not a rule that moves or expands the label based on
what is actually at that location.

**Deepbiosphere for invasive plants, Michigan (2026).** Mapping
distribution of invasive plant species and uncertainty using citizen
science, remote sensing, and deep learning. bioRxiv,
DOI: [10.64898/2026.06.10.731341](https://doi.org/10.64898/2026.06.10.731341)
— *To read*

Applies Deepbiosphere to invasive plants in Michigan: citizen science
+ high-resolution imagery + climate, statewide predictions at 256 m,
plus climate-scenario uncertainty. Acknowledges citizen-science
sampling bias as a limitation. **Closest work on invasive plants +
citizen science + remote sensing**; differs from this thesis in
resolution (256 m vs. 10 m), the absence of EO foundation models,
and no explicit bias experiment.

**Cambridge TESSERA group (2026, work in progress).** Global habitat
maps from Tessera embeddings.
[Project page](https://anil.recoil.org/ideas/tessera-habitat-maps)
— *To read / follow*

GBIF occurrences, filtered against IUCN ranges, used as weak, noisy
labels over TESSERA embeddings for habitat classification. Reports
heavy clustering around nature reserves, canals and a zoo.
**Closest work on foundation models + citizen-science labels**;
habitats, not invasive plants; no published results yet. Monitor:
the group could publish in the same space.

**Radová (2026, unpublished).** Can citizen science data improve
*Acacia dealbata* maps from supervised satellite image classification?
A post-classification approach. Internal presentation, Department of
Mathematics, University of Coimbra, 2026-10-30 (CFE, advised by
Cidália Fonte and Diogo Duarte). — *Unpublished; I only attended the
talk, this is not a paper or preprint, and the summary below may not
match whatever the final thesis says*

Post-classification recalibration of an existing Sentinel-2 Random
Forest *A. dealbata* probability map, using iNaturalist research-grade
observations (Sentinel-2 tile 29TNE, Aveiro–Coimbra–Leiria — contains
this thesis's Coimbra study area) as a correction signal, not as
training data; retraining the classifier with citizen-science labels
is listed as future work, not done. Points worth noting, with the
unpublished caveat above:

- Most apparent disagreement between points and map is attributed to
  GPS/pixel misalignment rather than model error (median point
  probability 18% → 51% once a 30–50 m neighbourhood is allowed
  instead of the exact pixel) — consistent with this thesis's choice
  to drop positional accuracy > 30 m (step 2 of the
  [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed))
  and with the segmentation-mask question in
  [Prediction Task](research_questions.md#prediction-task-adopted).
- One observer made 85% of *A. dealbata* records — close to the
  dominant-observer bias found independently in this thesis's own
  pilot (83% overall, 85% in 2021–2025; see
  [RQ3](research_questions.md#rq3--spatial-sampling-concentration)), over a
  larger area. If it is the same observer, that is independent
  support that the bias is not an artefact of the smaller pilot.
- Points cluster along roads/trails, consistent with the bias axes
  from Dimson et al. (2023).
- Uses COS 2023 and OrtoSat 2023 as independent checks, the same
  sources used in this thesis's [Species Scope](research_questions.md#species-scope-proposed)
  work.
- **Contrast:** proposes using other-plant observations as negative
  evidence against *Acacia* (to push probabilities down). This thesis
  does not use other-plant observations at all: its negative side is a
  uniform-random background, not claimed absences.

### Citizen science + invasive plants + deep learning

**Cardoso et al. (2024).** Can citizen science and social media
images support the detection of new invasion sites? A deep learning
test case with *Cortaderia selloana*. *Ecological Informatics*, 81,
102602. DOI: [10.1016/j.ecoinf.2024.102602](https://doi.org/10.1016/j.ecoinf.2024.102602)
— *To read*

CNNs on ground-level citizen-science and social-media photos detect
*Cortaderia selloana* in Portugal (>77% identification success) and
map unreported occurrences. Image-based computer vision, not
satellite EO.

### Citizen-science sampling bias

**Dimson et al. (2023).** Citizen science can complement professional
invasive plant surveys and improve estimates of suitable habitat.
*Diversity and Distributions*.
DOI: [10.1111/ddi.13749](https://doi.org/10.1111/ddi.13749)
— *To read*

Hawaiʻi, four invasive species. iNaturalist records are biased toward
roads/trails and disturbed vegetation; professional surveys toward
less accessible, native-dominated sites. Habitat models from each
source overlap only moderately; combining both gives more complete
estimates. Whether the same bias axes hold in Portugal is untested.

Relevance to the expert-reference comparison in RQ1: citizen-science
and professional data have *inverse* biases, so the expert end of
the effort-reduction curve is not bias-free either — it is biased
differently.

### Conventional invasive plant mapping

**Martins, Alegria & Gil (2016).** Mapping invasive alien *Acacia
dealbata* Link using ASTER multispectral imagery: a case study in
central-eastern Portugal. *Forest Systems*, 25(3), e078.
DOI: [10.5424/fs/2016253-09248](https://doi.org/10.5424/fs/2016253-09248)
— *To read*

ASTER imagery, central-eastern Portugal. Best accuracy with
flowering-season imagery and Maximum Likelihood (overall accuracy
86%). Early Portuguese precedent; supports flowering phenology as the
key conventional signal, which the Sentinel-2 baseline features
should capture.

**Mouta et al. (2021).** 'The Best of Two Worlds' — Combining
Classifier Fusion and Ecological Models to Map and Explain Landscape
Invasion by an Alien Shrub. *Remote Sensing*, 13(16), 3287.
DOI: [10.3390/rs13163287](https://doi.org/10.3390/rs13163287)
— *To read*

Maps *Acacia longifolia* in a northern Portugal municipality with
Sentinel-2 (10 m), a fusion of eight classifiers, and Random Forest
to explain invasion drivers. Portuguese precedent for a credible
conventional baseline.

**Domingo et al. (2023).** Assessing the Efficacy of Phenological
Spectral Differences to Detect Invasive Alien *Acacia dealbata* Using
Sentinel-2 Data in Southern Europe. *Remote Sensing*, 15(3), 722.
DOI: [10.3390/rs15030722](https://doi.org/10.3390/rs15030722)
— read in full (open-access copy via Universidad de
Zaragoza repository, since MDPI blocks automated access).

Sentinel-2 time series and flowering-period spectral differences,
with Random Forest feature selection, map *A. dealbata* in Arnoia
(Ourense, Galicia): 94% overall accuracy with six metrics. Sentinel-2
only; no spatial cross-validation confirmed.

**Exact method, confirmed from the text:** Sentinel-2 L2A, blue
(B02)/green(B03)/red(B04)/NIR(B08) at native 10 m only; cloud/cirrus
masked via the quality bitmask (<20% scene cloudiness kept); monthly
median composites built from 208 cloud-free scenes, 2018–2021. Six
normalized-difference indices from all pairwise combinations of the
four bands (RG, GB, BR, NDVI = NIR/Red, NIRG, NIRB). The flowering
peak was found empirically from the monthly time series (blooming:
March; pre-flowering: January; post-flowering: May — chosen as the
months where the ND indices returned to baseline either side of the
peak), giving 27 candidate features (9 metrics × 3 periods: the raw
bands/indices at each period, plus the pre→bloom and bloom→post
deltas). Random Forest (GEE `smileRandomForest`, ntrees 1–3000,
mtry 1–3, 75/25 train/test, 10 repeats) with Gini importance then
narrowed this to **6 final features** for the reported 94% accuracy:
NIR in March (blooming), Δpre-NDVI, Δpre-BR, Δpre-RG, ΔBR-post,
ΔRG-post — i.e. every surviving feature is a flowering-period
difference except the raw blooming-NIR value, and the two indices
built from blue (BR, RG) carried the most importance.

**Eskandari, Acuña-Alonso & Álvarez (2025).** Identification of
Acacia invasive species in protected areas of Spain using PlanetScope
high-resolution satellite images and machine learning models in time
series. *Forest Ecology and Management*, 586, 122696.
DOI: [10.1016/j.foreco.2025.122696](https://doi.org/10.1016/j.foreco.2025.122696)
— *To read*

PlanetScope time series + Random Forest map *Acacia* sp. in the Cíes
Islands, Galicia; Random Forest beat the other algorithms. Specific
area-change figures (2016–2024) are **unverified** — the publisher
page blocks automated access.

### Presence-only modelling

**Phillips et al. (2009).** Sample selection bias and presence-only
distribution models: implications for background and pseudo-absence
data. *Ecological Applications*, 19(1), 181–197.
DOI: [10.1890/07-2153.1](https://doi.org/10.1890/07-2153.1)
— *To read*

Background data are usually drawn at random, but occurrence records
are biased toward accessible areas, which gives inaccurate models.
Proposes **target-group background**: use all occurrences of a group
of species recorded by similar methods as background, since they
share the same bias. Across 226 species, target-group background
improved average performance for every modelling method tested,
with the largest gains where the presence records were most biased.
The adopted background is uniform-random, which this paper argues against; it is
kept on empirical grounds (step 7 of the
[Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)).

### One-class / positive-unlabeled classification

> Search done for the RQ1 method choice. True one-class methods were
> then tested and dropped in favour of presence-vs-background (see
> [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)).
> **Every entry comes from search snippets, abstracts or citing-paper
> summaries; no full text was read. Verify any figure before citing.**

Terminology is inconsistent in this literature: "one-class" is used
both for methods with no background data at all (true one-class,
novelty detection) and for methods with no *labelled negatives* that
still use unlabelled or background data (presence-background,
PU-learning). Phillips et al. (2009) and MaxEnt are the second kind.

- **Deng, Li, Liu, Guo & Newsam (~2018).** One-class remote sensing
  classification: one-class vs. binary classifiers. *Int. J. Remote
  Sensing*. DOI: 10.1080/01431161.2017.1416697. The closest to this
  thesis's framing: under a limited labelling budget,
  Presence-and-Background Learning beat both plain one-class SVM and
  the binary classifiers tested. The advantage comes from using
  unlabelled data, not from avoiding it.
- **Skowronek, Asner & Feilhauer (2017).** Performance of one-class
  classifiers for invasive species mapping using airborne imaging
  spectroscopy. *Ecological Informatics*, 37, 66–76. DOI:
  10.1016/j.ecoinf.2016.11.005. Two invasives, 1 m airborne data;
  MaxEnt, biased SVM and BRT (all presence-background); overall
  accuracy 72–88%.
- **Li, Guo & Elkan (2011).** A Positive and Unlabeled Learning
  Algorithm for One-Class Classification of Remote-Sensing Data. *IEEE
  TGRS*, 49(2), 717–725. DOI: 10.1109/TGRS.2010.2058578. PU-learning
  outperformed biased SVM and one-class SVM on two aerial scenes.
- **Li & Guo (2010).** A maximum entropy approach to one-class
  classification of remote sensing imagery. *Int. J. Remote Sensing*.
  DOI: 10.1080/01431161003702245. Reports MaxEnt beating one-class
  SVM; contradicted by a 2016 comparison in *Remote Sensing Letters*
  (DOI: 10.1080/2150704X.2016.1265689), where biased SVM came first
  and "even the best overall approach still performs poorly in a
  significant number of tasks".
- **Rapinel & Hubert-Moy (2021).** Systematic review of one-class
  vegetation classification, 2013–2020, 136 articles. Content not
  retrieved.
- **Goldenrod (*Solidago*), Sentinel-2 vs. PlanetScope, Poland (2024;
  title and authorship not confirmed).** Random Forest outperformed
  one-class SVM by 1–15 percentage points on dense stands; a related
  study reportedly found a drop for patchy vegetation, relevant here
  because citizen-science presences are often isolated trees.
- **Zhu, Samat, Li, Xu, Li & Li (2025).** Adversarial
  Positive-Unlabeled Learning-Based Invasive Plant Detection in Alpine
  Wetland Using Jilin-1 and Sentinel-2 Imageries. *Remote Sensing*,
  17(6), 1041. DOI: 10.3390/rs17061041. No figures retrieved.

**Synthesis (my reading):** in every empirical comparison found, a
true zero-background one-class method was the worst or near-worst
performer, with no counter-example. None of these studies matches this
setup, but the thesis's own tests later agreed with them.

### Evaluating presence-only models without confirmed absences

**Hirzel, Le Lay, Helfer, Randin & Guisan (2006).** Evaluating the
ability of habitat suitability models to predict species presences.
*Ecological Modelling*, 199(2), 142–152.
DOI: 10.1016/j.ecolmodel.2006.05.017 — *Abstract + secondary
documentation (R package docs), full text not read*

Introduces the **continuous Boyce index**: a Spearman rank correlation
between the proportion of presence sites falling in each
prediction-value class and the proportion expected from background
sites in that class; range −1 to 1, with values above 0 meaning
predictions track true presence probability. Tested on 114 alpine
plant species (Swiss Alps) against AUC/Kappa-style metrics —
moderately-to-strongly correlated with them, fairly insensitive to
prevalence. **Still needs background points**: it avoids needing
*labelled absences*, not background data entirely. Implemented in R:
`enmSdmX::evalContBoyce`, `tidysdm::boyce_cont`.

**Li & Guo (2014).** Positive-background learning F-measures (F-pb,
F-cpb). *IEEE TGRS*, 52(8), 4621–4632. DOI: 10.1109/TGRS.2013.2283082
— *Abstract only; exact title not independently confirmed*

Replaces observed negatives with background data in a modified
confusion matrix; F-cpb calibrated for class prevalence. Tested on two
aerial-photo scenes, ranked models similarly to standard
F-measure/kappa. A 2023 follow-up (Hainan University) extended the
idea to impervious-surface mapping (WorldView-3, Landsat 8). Also
needs background data — same caveat as the Boyce index.

**No method was found that evaluates a presence-only model without
any background or unlabelled sample.** Even a zero-background training
method needs background data to be evaluated, which is why the shared
background pool exists.

### Spatial validation

**Karasiak, Dejoux, Monteil & Sheeren (2021/2022).** Spatial
dependence between training and test sets: another pitfall of
classification accuracy assessment in remote sensing. *Machine
Learning*, 111(7), 2715–2740. DOI:
[10.1007/s10994-021-05972-1](https://doi.org/10.1007/s10994-021-05972-1)
(online 2021, journal issue dated 2022) — authors/venue confirmed via
dblp/OpenAlex — *Full text not read: blocked by bot
protection on HAL and a login wall on Springer; everything below is
from its own software's documentation and from a citing review
(Mahoney et al., 2023, full text read — see below)*

Sentinel-2 forest classification: non-spatial cross-validation
overestimates accuracy; spatial leave-one-out (SLOO) gives estimates
consistent with real map quality. Released **Museo ToolBox**, whose
`SpatialLeaveOneOut` class takes its buffer/exclusion distance as
`distance_thresold`, documented **in pixels, not metres**
(museotoolbox.readthedocs.io, checked) — relevant directly
to how many pixels/metres a validation buffer should be, see
[methodology.md#validation](methodology.md#validation).

**Le Rest, Pinaud, Monestiez, Chadoeuf & Bretagnolle (2014).** Spatial
leave-one-out cross-validation for variable selection in the presence
of spatial autocorrelation. *Global Ecology and Biogeography*, 23(7),
811–820. DOI:
[10.1111/geb.12161](https://doi.org/10.1111/geb.12161) — *Full text
not read (403 on the publisher); secondary summary and the citing
review (below) only*

Introduced SLOO: the exclusion buffer/threshold distance is set equal
to the **range of residual spatial autocorrelation (RSA)** —
estimated from the data (e.g. via a variogram), not a fixed universal
value.

**Mahoney, Johnson & Silge (2023).** Assessing the performance of
spatial cross-validation approaches for models of spatially structured
data. arXiv:2303.07334. — *Full text read (open-access preprint)*

Simulation study comparing five spatial CV strategies (clustered,
blocked, LODO, buffered leave-one-observation-out, inclusion-radius
variants). Confirms the buffer/exclusion distance is "a matter of some
debate," with suggestions across the field (including Karasiak et al.,
2021) to use the **variogram range of the predictors, outcome, or
model residuals** — not a fixed constant. In their simulations, the
best-performing parameterisations separated train/test by roughly
**25–41% of the study-area extent**, close to the measured ~25%
autocorrelation range of their simulated outcome variable; spatial
blocking/clustering (closer to this thesis's existing 10 km block
holdout) was at least as robust as buffered leave-one-out, which was
comparatively sensitive to the buffer size chosen. Introduces the R
package `spatialsample`.

**Meyer & Pebesma (2021).** Predicting into unknown space? Estimating
the area of applicability of spatial prediction models. *Methods in
Ecology and Evolution*, 12(9), 1620–1633. DOI:
[10.1111/2041-210X.13650](https://doi.org/10.1111/2041-210X.13650)
(journal details from a library listing, not checked on the
publisher) — *arXiv version (2005.07939) read through an automated
text extraction, not page by page*

Defines a dissimilarity index (DI): distance in predictor space from a
location to its nearest training point, with predictors standardised
and weighted by variable importance, divided by the mean pairwise
distance among training points; for training points, the nearest
point outside their own cross-validation fold. The area of
applicability (AOA) is where DI stays below a threshold taken from
the training data's own cross-validated DI. Tested on simulated
responses over Europe (Random Forest, 19 bioclimatic predictors),
including a spatially clustered training scenario with
leave-cluster-out validation: inside the AOA, prediction error is
comparable to the cross-validation error; outside it is considerably
higher (case study RMSE 0.07 inside vs. 0.38 outside), and DI
correlates with true absolute error (r = 0.71). Stated limits:
regression only (classification not tested), Random Forest only,
simulated data, nearest-point distance only, and the threshold "comes
with reservations". Implemented in the R package `CAST`. Method in
the proposed RQ3 redesign (to confirm with the supervisor) — see
[`research_questions.md`](research_questions.md#rq3--spatial-sampling-concentration).

**Applied here:** this project's own empirical variogram
result and what it was used for (not a paper finding) is logged in
[`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km),
notebook:
[`notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb`](../notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb).

### *Acacia* fire ecology

**Riveiro et al. (2025).** Effectiveness of slash and burn treatments
in controlling *Acacia dealbata* Link invasion. *Biological
Invasions*, 27, 125.
DOI: [10.1007/s10530-025-03567-8](https://doi.org/10.1007/s10530-025-03567-8)
— *To read*

Eight experimental blocks across central Portugal, monitored for
three years. Burning promoted *A. dealbata* seed germination;
slashing stimulated resprouting. Even combined slash-and-burn left at
least 6.5 stems/m² (0 in controls). Relevance: burned *Acacia* stands
are not gone, so the disturbance filter removes observations because
the 2023 pixel no longer matches the label, not because the species
is absent. Also a caveat for post-2023 observations in burned areas:
after the 2025 fires, later observations may be regrowth.

### Weak supervision from point labels

**Rivier et al. (2023/2024).** Efficient Semantic Segmentation for
Aerial Imagery Using Query Points and Superpixel Supervision.
arXiv:2309.05490v2; published at IEEE ICIP 2024,
DOI: [10.1109/ICIP51287.2024.10647646](https://doi.org/10.1109/ICIP51287.2024.10647646).
PDF: [`literature/rivier_2024_superpixel_query_points.pdf`](literature/rivier_2024_superpixel_query_points.pdf).
Recommended by the supervisor for the segmentation mask:
a rule linking each citizen-science point to the nearest vegetation
area, with several approaches to compare (see
[`research_questions.md`](research_questions.md#prediction-task-adopted)).
— *Read (full text)*

Trains a full segmentation network (DeepLabV3/U-Net/FCN, not a
classifier on frozen embeddings) from sparse point labels (10-50 per
512×512 image) via superpixel propagation: superpixels are generated
with DAL-HERS (learned pixel affinities + hierarchical entropy-rate
merging), each superpixel gets the majority class among the points
that fall inside it, and superpixels with no point are left unlabelled
(masked out of the loss). mIoU 75.64% on LandCoverAI (25-50 cm RGB
aerial imagery, 4 classes), close to full supervision (83.99%).
Ablation: more points per image always helps; more superpixels (i.e.
smaller regions) hurts once past ~100-200 (best at 80-100, worse at
200-300) — relevant here because our citizen-science points are a few
per tile, not tens to fifty as in their setup, so coarser regions may
suit us better. Differences from our setting to keep in mind: dense,
evenly distributed point grids (not sparse opportunistic citizen
science), RGB-only sub-metre imagery (not Sentinel-2/TESSERA), and an
end-to-end trained segmentation backbone (not the frozen-embedding +
light-classifier approach adopted here, see
[Foundation Model Use](research_questions.md#foundation-model-use-adopted)).

**Zhang, Tang, Corpetti & Zhao (2021).** WTS: A Weakly towards
Strongly Supervised Learning Framework for Remote Sensing Land Cover
Classification Using Segmentation Models. *Remote Sensing*, 13(3),
394. DOI: [10.3390/rs13030394](https://doi.org/10.3390/rs13030394)
— *Not read (full text blocked on MDPI, HAL — hal-03717196, behind a
bot-protection wall — and ResearchGate mirrors, confirmed still
blocked on a second attempt; characterisation below is from a
search-engine summary only, not verified first-hand — do not cite its
numbers)*

Reportedly uses SVM-labelled high-confidence pixels as seeds, then
seeded region growing plus a fully-connected CRF to iteratively grow
the labelled set, validated on Sentinel-2 imagery. Potentially another
candidate for the patch-mask rule (region growing from a point,
analogous to growing from a TESSERA-embedding seed), but needs the
actual text read before it can ground anything.

**Zhang, Kumar, Hoffman, Ivanov, Wang, Sheshukov, Zhou, Montesano &
Liu (2025).** A Region-Growing Segmentation Approach to Delineating
Timberline from Satellite-Derived Tree Fractional Cover Products.
*Remote Sensing*, 17(12), 2002.
DOI: [10.3390/rs17122002](https://doi.org/10.3390/rs17122002) —
*Read (full text, open access)*

Found while checking a candidate title; no relation to Zhang, Tang,
Corpetti & Zhao (2021) above beyond a shared surname. Seeded region
growing over a single satellite-derived raster band (tree fractional
cover, CGLS, 100 m): seeds are pixels representative of each
continuous forest patch (densest cover or patch boundary), the region
grows by a fixed global threshold (fCover > 0.3), and the output
boundary is the timberline. **The strongest accessible precedent found
so far for candidate 1 (region growing)** — a real, read, open-access
case of seeded region growing delineating vegetation extent from a
satellite product, replacing Zhang et al. (2021) above as the live
anchor for this candidate, which stays unread/blocked. Not a perfect
fit: grows over one interpretable scalar band with a fixed threshold,
not high-dimensional embeddings with a similarity-to-seed criterion,
and has no sparse point-label or citizen-science-noise angle at all —
so it supports the general technique (region growing to delineate
vegetation extent from satellite data), not our specific point-label
setting.

**Raine, Marchant, Kusy, Maire & Fischer (2022).** Point Label Aware
Superpixels for Multi-species Segmentation of Underwater Imagery.
*IEEE Robotics and Automation Letters*, 7(3), 8291–8298.
DOI: [10.1109/LRA.2022.3187836](https://doi.org/10.1109/LRA.2022.3187836),
arXiv:2202.13487. — *Read (full text, HTML)*

Found searching for papers citing Rivier et al. (2024) /
addressing the same problem, in response to the supervisor's "and
similar works" pointer (no second direct remote-sensing precedent for
superpixel label propagation turned up this way — see Wölk et al.
below). **Not remote sensing** — underwater photo-quadrats of coral,
not satellite imagery — but a closer analogue than Rivier on one axis:
it is **species-level**, propagating sparse ecologist point labels to
multi-species segmentation, the same structure as our *A. dealbata*
point-to-patch problem. Superpixels are computed on features from a
Superpixel Sampling Network encoder, not raw pixels; their own ablation
shows feature-based superpixels clearly beat raw-LAB ones (89.6–92.6 vs.
64.1 pixel accuracy) — direct support for building superpixels on
TESSERA embeddings rather than raw Sentinel-2 bands, our candidate 2.
Unlabeled superpixels take the class of the **most feature-similar
labeled superpixel**, not masked out of the loss as in Rivier — a
different, explicit design choice to consider instead of just
inheriting Rivier's rule. Point density tested (200–300/image) is still
far above our few citizen-science points per tile, same gap as Rivier.
Explicitly notes prior point-supervision work "assumes points lie
centrally within objects" — a caveat directly relevant to citizen-science
points, which are often off-target (phone GPS near a road or trail, not
the plant itself).

**Liu, Wang, Xu, Shi & Xing (2026).** Tighnari v2: Mitigating Label
Noise and Distribution Shift in Multimodal Plant Distribution
Prediction via Mixture of Experts and Weakly Supervised Learning.
arXiv:[2602.08282](https://arxiv.org/abs/2602.08282). Experiments on
GeoLifeCLEF 2025 (11 255 species). — *Read (full text, HTML)*

Found searching for a precedent for candidate 3 (COS-polygon label
extension). Pools *multiple* presence-only point records that fall
inside the same fixed 640 m × 640 m Sentinel patch as joint labels for
that patch — the mirror operation of our rule (we extend *one* point's
label outward to an existing polygon; they pool *many* points' labels
inward onto a fixed grid cell). Confirms area-based aggregation of
sparse presence-only points against satellite imagery is an active,
current technique (2026) in this general problem family, but is **not
a direct precedent** for extending a label via an independent,
pre-existing auxiliary land-cover polygon (as opposed to a fixed grid
or a model-derived region) — reinforces, rather than changes, what
`research_questions.md` already says about candidate 3 being a
possible contribution, not an applied practice.

**Wölk, Degenhardt, Hellmundt & Fu (2026).** Uncertainty-Aware
Annotation for Reliable Tree Cover Monitoring from Satellite Imagery.
ACM GoodIT 2026 (Best Paper Award), Madagascar tree-cover case study.
— *To find (only a university press release found; no PDF or DOI
landing page with full text located)*

The one paper citing Rivier et al. (2024) found to be topically
close, while searching for the supervisor's unnamed "similar works."
From the press release only: lets annotators flag ambiguous objects as
"uncertain" and uses auxiliary models to estimate class probabilities
for those — **a different problem** (annotation uncertainty, not
point→patch label propagation) from our three mask candidates. **Low
relevance**; do not use beyond this one-line characterisation unless
the full text is found later.

## Data Sources Found in the Literature Search

Not papers, but relevant:

- **Sightings Map of Invasive Plants in Portugal** — citizen-science
  dataset by the Centre for Functional Ecology, University of
  Coimbra (invasoras.pt), published on GBIF. Different platform and
  observer pool from iNaturalist: candidate extra presences or a
  cross-platform test for RQ3. See
  [Species Scope](research_questions.md#species-scope-proposed).

## What Has Already Been Done

1. Citizen science → plant/invasive-species observations at scale
   (Gillespie 2024; Dimson 2023; Cardoso 2024).
2. Remote sensing → invasive plant mapping, including *Acacia* in
   Iberia (Martins 2016; Mouta 2021; Domingo 2023; Eskandari 2025).
3. Deep learning → plant species mapping (Gillespie 2024; Cardoso
   2024).
4. Citizen science + remote sensing → plant mapping (Gillespie 2024),
   including invasive plants at 256 m (Michigan preprint, 2026).
5. EO foundation models vs. conventional features → many tasks:
   trees (Ball 2026), crops (Yang 2026), ecosystems (atolls 2026),
   burned area in Portugal (Gonçalves 2026).
6. EO foundation models + iNaturalist labels → genus-level evaluation
   (Brown 2025); habitat mapping with GBIF labels in progress
   (Cambridge).
7. EO foundation models → label efficiency (Ball 2026).
8. Embeddings transfer worse across regions than within (Zhu 2026;
   Yang 2026; old-growth preprint 2026).
9. Citizen-science invasive-plant data are spatially biased (Dimson
   2023); target-group background mitigates bias in presence-only
   models (Phillips 2009).

None of these, on its own, is this thesis's novelty.

## Gap

Each ingredient has prior work; their intersection — **EO foundation
models + invasive plant mapping + citizen-science reference data,
with explicit evaluation of sparsity and spatial bias** — appears
underexplored:

- Ball et al. (2026): foundation models + label efficiency, but tree
  species with curated labels, and random label reduction only.
- Brown et al. (2025): foundation models + iNaturalist labels, but as
  a generic benchmark, with no bias analysis.
- Cambridge TESSERA group: foundation models + GBIF labels with
  observed bias, but habitats, and not yet published.
- Michigan preprint (2026): invasive plants + citizen science +
  remote sensing, but 256 m and no foundation models.
- Dimson et al. (2023): citizen-science bias for invasive plants, but
  no foundation models.
- Zhu et al. (2026) and related: embeddings transfer worse across
  regions, but not tested with biased citizen-science labels.
- Cardoso et al. (2024): citizen science + invasive plants in
  Portugal, but ground-level images, not satellite EO.

Three specific questions not answered by any of the above:

1. **Do foundation models amplify or mitigate citizen-science spatial
   bias** compared with conventional features? (RQ3)
2. **How do foundation models behave when citizen-science data are
   reduced by a documented filter** (observations furthest from the
   imagery year first) rather
   than at random? Existing label-efficiency work uses random
   reduction only (Ball 2026). (RQ2)
3. **How much is lost by training on citizen science instead of
   expert reference data**, with the same representation and test
   set? (RQ1)

## Contribution

**Data-efficient and bias-aware invasive plant mapping using EO
foundation models and citizen science.** Not "apply TESSERA to
invasive plants", but a controlled study of how foundation-model
representations behave under realistic citizen-science limitations
(sparsity, spatial bias), against a conventional satellite baseline
and increasing amounts of expert reference data.

Two parts:

1. **Methodological:** a documented, justified pipeline that turns
   citizen-science points into satellite reference data (the
   proposal's first objective; see
   [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)) —
   each step documented and justified from literature or data. A
   cumulative ablation measuring each step's effect is an optional
   stretch goal. Candidate step with no precedent found: the
   segmentation mask, which extends a citizen-science point to the
   patch around it using frozen embeddings (see
   [Prediction Task](research_questions.md#prediction-task-adopted)).
2. **Empirical:** RQ1–RQ3 in
   [`research_questions.md`](research_questions.md).
