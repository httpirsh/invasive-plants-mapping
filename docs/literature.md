# Literature

A small set of directly relevant papers, **not** a systematic review.
"Appears underexplored" claims reflect this reading list only and
must be revisited after a broader search (protocol in
[`thesis/notes.md`](../thesis/notes.md#protocolo-de-pesquisa-da-literatura)).

Every entry was re-read on 2026-11-11 from the full text where it
could be obtained. Each paper has a status:

- **Read** — full text read end to end; the summary is checked against
  it. Figures were read from captions and text, not viewed, and
  supplements were not read unless stated.
- **Read (other version)** — a preprint or author version was read,
  not the published article; numbers must not be cited as the
  published paper's.
- **Abstract only** — the full text is paywalled or blocked; the
  summary is from the abstract and must not be cited for details.
- **Unpublished** — a talk or a project page, not a paper.

## Papers

### EO foundation models

**Brown et al. (2025).** AlphaEarth Foundations: An embedding field
model for accurate and efficient global mapping from sparse label
data. arXiv:2507.22291 (v2). — *Read (main text and supplement)*

The AlphaEarth paper. Annual 64-dimensional embeddings at 10 m
(2017–2024), used without re-training; about 24% mean error reduction
over other featurization approaches, with unreliable gains in the
1-shot and 10-shot settings (S6.1). Transfer is by k-nearest
neighbours or a linear probe (S4.1), not Random Forest.

- **Biodiversity evaluation:** one evaluation, "US trees", 39 tree
  genera from GBIF research-grade iNaturalist observations (S3.3.7).
  So "embeddings + iNaturalist labels" is not new on its own.
- **Location filter, stated explicitly:** spatial uncertainty of at
  most 10 m, coordinates with at least four decimals, at least 1.28 km
  between points (S3.1–S3.2) — stricter than this thesis's 30 m.
- **AlphaEarth was trained with GBIF text labels** (research-grade
  observations 2017–2023, S1.12), a circularity caveat if it is ever
  used with iNaturalist labels. TESSERA is not affected.
- **Location alone predicts the labels well:** on US trees the
  next-best method uses coordinates only (S6.2).
- Embeddings are not pixel-independent: inference uses 1.28 km tiles
  with spatial self-attention (S8.2). Only embeddings are released,
  not weights.

**Feng et al. (2026).** TESSERA: Temporal Embeddings of Surface
Spectra for Earth Representation and Analysis. CVPR 2026,
pp. 34818–34831; arXiv:2506.20380 (v7).
[PDF](https://anil.recoil.org/papers/2025-tessera.pdf) — *Read (main
text and supplement)*

The TESSERA paper. Pixel-wise model on annual Sentinel-1 + Sentinel-2
time series, 128-dimensional embeddings at 10 m, distributed through
GeoTessera. Evaluated on tree species (Germany), crops (Austria,
France), biomass and canopy height, with MLP, U-Net and k-nearest
neighbour heads; no species-occurrence or citizen-science task.

- **Fine-tuning gives no benefit** over the frozen encoder (§5,
  Fig. 6b) — the strongest support found for frozen embeddings.
- **No spatial context:** pretraining is pixel-wise, with global
  shuffling to break spatial autocorrelation (§3.3, A.9). The
  embeddings do not encode the landscape around a pixel.
- **Coverage stated in the paper:** 2017–2024 (A.4).
- **Weights:** the paper says "open-source model weights"; the
  repository README (checked 2026-11-11) says the checkpoint is
  restricted to Cambridge members. Code licence (MIT) is from the
  repository, not the paper.
- Embeddings are built from a random sample of 40 valid dates per
  year; accuracy drops where valid Sentinel-2 observations are few.

**Ball et al. (2026).** Geospatial foundation models enable
data-efficient tree species mapping in temperate mountain forests.
*Science of Remote Sensing*, 14, 100466.
DOI: [10.1016/j.srs.2026.100466](https://doi.org/10.1016/j.srs.2026.100466)
(open access). — *Read (author manuscript from the Cambridge
repository; supplement not read). Baseline details also checked in the
authors' code,
[`PatBall1/trentino-trees`](https://github.com/PatBall1/trentino-trees)*

Compares TESSERA embeddings, AlphaEarth embeddings and conventional
Sentinel-1 + Sentinel-2 features for 18 tree species/groups (about
83 000 forest-inventory parcels) in Trentino, Italy. Embeddings are
used without fine-tuning.

**Conventional baseline:** every baseline combines Sentinel-1 and
Sentinel-2; there is no Sentinel-2-only baseline. Sentinel-2 SR
(`COPERNICUS/S2_SR_HARMONIZED`), scenes under 60% cloud, masked with
SCL (classes 4/5/6/7 kept) and QA60. Two variants: **annual** — one
median of 12 bands (B01–B12, B8A) plus NDVI, NDWI (McFeeters) and NBR;
**seasonal** — three medians (spring, summer, autumn; winter excluded
because of snow), 45 Sentinel-2 features. Sentinel-1 VV, VH, VV−VH,
VV/VH and incidence angle added the same way. Fixed 10 m UTM grid. The
headline baseline is **seasonal** (Table 3).

- Embeddings beat the seasonal baseline: weighted F1 0.83 vs. 0.80,
  macro F1 0.55 vs. 0.50 (TESSERA 0.827 / 0.551, AlphaEarth
  0.833 / 0.537). The annual baseline is 0.745 / 0.414.
- Near-optimal **weighted** F1 with about 5% of training parcels;
  macro F1 at 5% is about 10 points below full data (§3.1).
- A compact neural network was the best classifier. On TESSERA:
  Logistic Regression macro F1 0.38, MLP 0.55, Random Forest 0.08
  below the MLP (§3.2). Random Forest is included as a "widely
  adopted nonlinear baseline … robust to noisy labels".
- Robust to moderate label impurity, meaning mixed-species parcels,
  not off-target points; soft labels beat hard labels (macro F1
  0.586–0.589).
- Performance degraded across years (2018 → 2019): weighted F1 −9%
  TESSERA, −14% AlphaEarth. The authors warn it is one year-pair
  confounded by a storm and "should not be generalised" (§4.5).
- Inventory labels collected 2010–2021 are paired with 2018 imagery —
  a precedent for treating multi-year labels as one reference year.
- Main validation is parcel-level; a 5 km block check lowers macro F1
  by 6–7 points with rankings preserved (§4.1).

Conclusion: foundation models shift the bottleneck from feature
engineering to the availability, quality and temporal alignment of
reference data. Labels are curated, not citizen science. **Not in the
paper:** point data, a positional-accuracy threshold, or a cumulative
preprocessing ablation (it runs one-factor ablations).

### Spatial transfer of embeddings

What these show is narrower than "embeddings transfer worse than
conventional features": none of them compares the two under transfer
and finds embeddings worse.

**Stewart, Fang, Corley & Zhu (2026).** Earth Embeddings.
arXiv:2608.03410 (book chapter). — *Read*

Taxonomy of embedding products, a review of applications, licences and
publishing guidance; no experiments of its own. Says embeddings work
"in a narrower and more practical sense" than foundation-model
narratives imply. Its statement that embeddings are competitive
locally but less robust under spatial transfer is a one-sentence
report of **Ma, Shen, Swatantran & Lobell (2026)**, "Harvesting
AlphaEarth", *IJAEOG* 149, 105258 — not read; it is the primary
source for that claim.

- Classes TESSERA as a per-pixel model "neglecting spatial
  correlations", unlike AlphaEarth (§2.2).
- States that TESSERA weights and embeddings are public domain, and
  that only 2024 has global coverage, other years on request (§6.3,
  Table 3).
- Guidance (§7.1): compare embeddings against simple baselines and
  hand-designed covariates under spatial and temporal splits; random
  splits are insufficient evidence of transfer.

**Yang et al. (2026).** Evaluating the Performance of AlphaEarth
Foundation Embeddings for Irrigated Cropland Mapping Across Regions
and Years. *Remote Sensing*, 18(7), 1065.
DOI: [10.3390/rs18071065](https://doi.org/10.3390/rs18071065)
— *Read*

Seven light classifiers on frozen AlphaEarth embeddings for irrigated
cropland (Guanzhong Plain, China; Kansas, USA), labels from visual
interpretation. Within region, overall accuracy 0.90–0.95; across
years in the same region 0.87–0.88; from China to Kansas every model
falls below 0.5 (Random Forest best, 0.47).

- **No Sentinel baseline in the transfer test:** it shows embeddings
  transfer worse across regions than within, not worse than
  conventional features. The authors attribute the drop to
  region-specific associations learned by the classifier.
- No spatial validation (random 70/30 split of points).
- Accuracy columns in Tables A2–A3 do not match the confusion-matrix
  counts; quote its numbers with care.

**Ratsakatika, Zotta, Keshav & Lines (2026).** Geospatial embeddings
detect old-growth forests but buffered spatial validation narrows
their advantage over Sentinel features. arXiv:2609.28194 (preprint,
v1). — *Read (main text and supplementary tables)*

Old-growth forest mapping over 211 893 ha of Romania's Southern
Carpathians, expert-informed parcels with confirmed negatives,
AlphaEarth, TESSERA v2 and Sentinel-1/2 features added to a
topographic/access baseline, XGBoost, six spatial folds with
train–test buffers of 0, 10 and 20 km.

- **Unbuffered,** TESSERA reaches PR-AUC 0.84 and beats Sentinel-1/2
  by +0.08 [+0.05, +0.11]. **With a 10 km buffer** the advantage is
  +0.04 [−0.01, +0.11]. At 20 km it is +0.09 again, with little
  training data left. TESSERA has the highest point estimate at every
  buffer: the advantage narrows, embeddings are never worse.
- **Blocking is "necessary but not sufficient"** (§4.4): only buffering
  removes proximity across folds (PR-AUC 0.84 → 0.73). The 10 km
  buffer was chosen from measured autocorrelation (labels 6.6–6.7 km,
  TESSERA dimensions median 10.5 km).
- The unbuffered advantage is "unlikely to be attributable to spatial
  encoding within the embeddings", which are computed per pixel
  (§4.4).
- **Metrics:** PR-AUC is primary; ROC-AUC can look optimistic under
  class imbalance, and precision-based metrics are confounded by
  assumed negatives (§2.3, §4.2).
- Removing half the training parcels at random cost less than 0.04
  PR-AUC.
- Controls worth reusing: a coordinate-only model and a random-removal
  control matched to the buffer.

Also computes the area of applicability (Meyer & Pebesma, 2021 — see
[Spatial validation](#spatial-validation)) for its deployed model:
98.4% of forest inside the study area is within it, 65.0% across the
whole Carpathians. Done for one model only, not compared between
feature sets, and the authors state that applicability "refers to
feature-space support rather than model accuracy, which was not
tested outside the AOI or verified in the field" — the part a test
against independent reference data would add.

### EO foundation models in related applications

Listed to show RQ4 alone is not novel.

**Silva & Gonçalves (2026).** Evaluating AlphaEarth and TESSERA
Geospatial Embeddings for Machine Learning-Based Burned Area Mapping
in Portugal. Research Square preprint,
DOI: [10.21203/rs.3.rs-10285823/v1](https://doi.org/10.21203/rs.3.rs-10285823/v1)
(University of Porto; not peer reviewed). — *Read*

Twenty 2024 fires from the ICNF catalogue, burned vs. unburned points,
Random Forest, SVM and Gradient Boosting, cross-validation grouped by
fire. **The Sentinel-2 baseline wins:** F1 (SVM) 0.895, against 0.860
for TESSERA and 0.812 for AlphaEarth. The baseline uses pre- and
post-fire windows that an annual embedding cannot match. Embeddings of
the following year are worse (TESSERA 0.860 → 0.796). A Portuguese
case of Random Forest on TESSERA where the conventional features are
better, and evidence that fire changes a TESSERA annual embedding.

### Citizen science + remote sensing + plant mapping

**Gillespie, Ruffley & Exposito-Alonso (2024).** Deep learning models
map rapid plant species changes from citizen science and remote
sensing data. *PNAS*, 121(37), e2318296121.
DOI: [10.1073/pnas.2318296121](https://doi.org/10.1073/pnas.2318296121)
— *Read (main text; SI Appendix not read)*

Deepbiosphere: 652 027 research-grade observations of 2 221 plant
species in California, paired with 1 m NAIP imagery and deep learning.
Median per-species AUC 0.95 vs. 0.88 for Maxent and Random Forest on a
uniform split; 0.87 vs. 0.73 and 0.71 under latitudinal block
validation (Table 2). No EO foundation models, no invasive species. It
does address observation bias, with a sampling-aware loss.

- **Filters:** coordinate uncertainty ≤120 m, same-species duplicates
  within 150 m dropped, human observations only, 2015–2022.
- **Temporal:** observations from 2015–2022 are paired with 2012
  imagery — multi-year observations against one imagery year.
- **Background for the baselines:** 50 000 points drawn from circles
  around the training points, not uniform over the study area.
- **Point → image:** each point is paired with one 256 × 256 m image
  centred on it, and the model predicts per-image presence. Not a
  precedent for extending a label to the patch around a point.

**Qiang et al. (2026).** Mapping distribution of invasive plant
species and uncertainty using citizen science, remote sensing, and
deep learning. bioRxiv,
DOI: [10.64898/2026.06.10.731341](https://doi.org/10.64898/2026.06.10.731341)
(not peer reviewed; author name order to check on the bioRxiv page).
— *Read (supplement not read)*

Deepbiosphere applied to Michigan: a multispecies model (1 553
species) with two focal invasives, statewide at 256 m. Mean AUC 0.79
on a uniform split; median 0.69 across spatial bands, against 0.55 for
Random Forest. Acknowledges sampling bias as a limitation and states
there is no independent validation data. **Closest work on invasive
plants + citizen science + remote sensing**; differs in resolution,
no EO foundation models, no bias experiment. Its uncertainty map is
disagreement between future climate projections, not model or label
confidence.

**Cambridge TESSERA group (2026, work in progress).** Global habitat
maps from Tessera embeddings.
[Project page](https://anil.recoil.org/ideas/tessera-habitat-maps)
— *Unpublished (project page and M. Dales's weeknotes read; no paper
or preprint as of 2026-11-11)*

GBIF occurrences of terrestrial vertebrates, filtered against IUCN
ranges, used as weak labels of habitat class over TESSERA embeddings.
Reports heavy clustering of **places** (nature reserves, canals, a
zoo); observers are never analysed. **Closest work on foundation
models + citizen-science labels**; animals and habitats, not invasive
plants. From the weeknotes, informal and not citable: GBIF filtered to
≤10 m positional accuracy, spatial thinning on a 100 m grid, a linear
classifier on per-pixel embeddings.

**Radová (2026, unpublished).** Can citizen science data improve
*Acacia dealbata* maps from supervised satellite image classification?
A post-classification approach. Internal presentation, Department of
Mathematics, University of Coimbra, 2026-10-30 (CFE, advised by
Cidália Fonte and Diogo Duarte). — *Unpublished; I only attended the
talk, and the summary below may not match whatever the final thesis
says*

Post-classification recalibration of an existing Sentinel-2 Random
Forest *A. dealbata* probability map, using iNaturalist research-grade
observations (Sentinel-2 tile 29TNE, which contains the Coimbra study
area) as a correction signal, not as training data.

- Most disagreement between points and map is attributed to GPS/pixel
  misalignment rather than model error (median point probability
  18% → 51% once a 30–50 m neighbourhood is allowed).
- One observer made 85% of *A. dealbata* records, close to the
  concentration found in this thesis's own pilot.
- Points cluster along roads/trails.
- Uses COS 2023 and OrtoSat 2023 as independent checks.
- Proposes other-plant observations as negative evidence against
  *Acacia*, which this thesis does not do.

### Citizen-science sampling bias

**Dimson, Berio Fortini, Tingley & Gillespie (2023).** Citizen science
can complement professional invasive plant surveys and improve
estimates of suitable habitat. *Diversity and Distributions*, 29(9),
1141–1156. DOI: [10.1111/ddi.13749](https://doi.org/10.1111/ddi.13749)
— *Read (other version): the published article is blocked; read the
published abstract and the submitted version in M. Dimson's UCLA
dissertation, chapter 3. Download the article by hand before citing
any detail*

Hawaiʻi, four invasive species, Maxent fitted on iNaturalist only,
agency data only, and both. iNaturalist records are biased toward
roads/trails and disturbed vegetation; professional surveys tended
toward less accessible, native-dominated sites. Models from each
source overlap moderately; the authors conclude that combining both
gives more complete estimates, without measuring accuracy (no
independent test set).

- **"Inverse biases" is partial:** the abstract says "often". In the
  dissertation version accessibility bias is inverse for two of four
  species, and both sources share a bias toward protected open space.
- **Background:** restricted to cells within 500 m of any
  research-grade iNaturalist plant observation, citing Phillips et al.
  (2009).
- **Thinning** at 1 km barely changed the models; the conclusion
  recommends "including all available data regardless of suspected
  anthropogenic sampling biases".
- Filtering effects were confounded with sample size; they recommend
  controlling for it.

Its agencies sampled different places from the citizen scientists;
here experts and the dominant observer visited the same places, so it
is an analogy for the expert end of the RQ1 curve, not direct
evidence.

### Conventional invasive plant mapping

All three use a random train/test split, none a spatial one, and all
find the signal in specific months or phenological differences rather
than an annual composite.

**Martins, Alegria & Gil (2016).** Mapping invasive alien *Acacia
dealbata* Link using ASTER multispectral imagery: a case study in
central-eastern of Portugal. *Forest Systems*, 25(3), e078.
DOI: [10.5424/fs/2016253-09248](https://doi.org/10.5424/fs/2016253-09248)
— *Read*

One ASTER scene (15 m), Castelo Branco district, nine classes, 1 080
reference sites split 75/25 at random. Best result with March
(flowering) imagery and Maximum Likelihood: overall accuracy 85.2% in
Table 4 (the abstract says 86%), far above SVM and ANN; no Random
Forest. *Acacia* user's accuracy 100%, producer's 70%. March against
August is a comparison of two single dates two years apart. In March
*Acacia* was confused with agriculture and maritime pine, and the
authors suggest January–February imagery might be better. Field data
are 4–7 years later than the imagery, without discussion.

**Mouta et al. (2021).** 'The Best of Two Worlds' — Combining
Classifier Fusion and Ecological Models to Map and Explain Landscape
Invasion by an Alien Shrub. *Remote Sensing*, 13(16), 3287.
DOI: [10.3390/rs13163287](https://doi.org/10.3390/rs13163287)
— *Read*

Maps *Acacia longifolia* in Viana do Castelo with Sentinel-2 at 10 m
(one image per month, December–May, 12 bands plus six indices) and a
fusion of eight classifiers in biomod2.

- **Presence vs. pseudo-absence:** 167 presence areas, 40
  photo-interpreted absences and random pseudo-absences equal in
  number to the presences, evaluated with ROC, TSS and Kappa; random
  80/20 holdout.
- **Random Forest was third** as a classifier (TSS 0.824, ROC 0.962),
  behind GAM and FDA; the ensemble beat all (ROC 0.988). Maxent did
  poorly as a pixel classifier. The "Random Forest" that explains
  invasion drivers is a regression on 2 km² hexagons.
- **Importance:** green, SWIR2 and blue bands first; bands 78%,
  indices 22%; December–February mattered most.

**Domingo et al. (2023).** Assessing the Efficacy of Phenological
Spectral Differences to Detect Invasive Alien *Acacia dealbata* Using
Sentinel-2 Data in Southern Europe. *Remote Sensing*, 15(3), 722.
DOI: [10.3390/rs15030722](https://doi.org/10.3390/rs15030722)
— *Read (open-access copy, Universidad de Zaragoza repository)*

Sentinel-2 monthly composites and flowering-period spectral
differences, with Random Forest feature selection, map *A. dealbata*
presence/absence in Arnoia (Ourense, Galicia): 94% overall accuracy
(Kappa 0.86) with six metrics.

**Method:** Sentinel-2 L2A, blue (B02), green (B03), red (B04) and NIR
(B08) at 10 m; cloud/cirrus masked via the quality bitmask (scenes
under 20% cloud); monthly medians from 208 scenes, 2018–2021. Six
normalized-difference indices from all pairs of the four bands (RG,
GB, BR, NDVI, NIRG, NIRB). Flowering peak found from the time series
(blooming: March; pre-flowering: January; post-flowering: May).
Candidate features are blooming values and the pre→bloom and
bloom→post differences. Random Forest (GEE `smileRandomForest`, 75/25
random split, 10 repeats) with Gini importance gave **six final
features**: NIR in March, Δpre-NDVI, Δpre-BR, Δpre-RG, ΔBR-post,
ΔRG-post. Highest importance: Δpre-RG and Δpre-NDVI; March NIR lowest.
Differences between periods discriminated better than single-period
values.

**Limits:** 120 field plots (48 presences, 72 absences) in 20.7 km²,
so each validation run uses 30 points. Pure stands only, plots more
than 30 m from stand borders; mixed stands and understorey *Acacia*
are excluded, so 94% is not a comparable target for roadside
citizen-science points. Confusion with cropland and shrubland. The
authors note that flowering coincides with the cloudiest period.

### Presence-only modelling

**Phillips et al. (2009).** Sample selection bias and presence-only
distribution models: implications for background and pseudo-absence
data. *Ecological Applications*, 19(1), 181–197.
DOI: [10.1890/07-2153.1](https://doi.org/10.1890/07-2153.1)
— *Read*

Background data are usually drawn at random, but occurrence records
are biased toward accessible areas, so "a fitted model might be closer
to a model of survey effort than to a model of the true distribution".
Proposes **target-group background**: all occurrences of a group of
species recorded by similar methods, which share the same bias. Across
226 species in six regions it improved every method tested (e.g.
boosted trees AUC 0.728 → 0.754, Maxent 0.728 → 0.757), most where
bias was strongest. Random Forest was not tested.

- **The gains only show against independent presence–absence data.**
  Scored with test presences against random background, the
  target-group model looks *worse* (AUC 0.717 vs. 0.820, p. 193). A
  check that scores presences against a background therefore cannot
  show a uniform background is unbiased.
- **Restricting the background** to areas where the species could
  occur is "a special case of the biased background sampling approach"
  (p. 195), for one species with no effort information.
- **Stated failure case:** the correction assumes effort and presence
  are independent given the predictors; a pioneer plant correlated
  with disturbance, more common near roads, breaks it (p. 187).
- **AUC ceiling:** AUC against random background has a maximum
  "typically less than 1" (p. 188).
- Discarding or down-weighting records is "unpalatable" when records
  are few (p. 182); single-observer dominance is not discussed.

The adopted background is uniform-random, which this paper argues
against (step 7 of the
[Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)).

### One-class / positive-unlabeled classification

> Search done for the RQ1 method choice. True one-class methods were
> then tested and dropped in favour of presence-vs-background (see
> [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)).

Terminology is inconsistent in this literature: "one-class" is used
both for methods with no background data at all (true one-class,
novelty detection) and for methods with no *labelled negatives* that
still use unlabelled or background data (presence-background,
PU-learning). Phillips et al. (2009) and MaxEnt are the second kind.

**Deng, Li, Liu, Guo & Newsam (2018).** One-class remote sensing
classification: one-class vs. binary classifiers. *Int. J. Remote
Sensing*, 39(6), 1890–1910. DOI: 10.1080/01431161.2017.1416697.
— *Read*

Land cover on 0.3 m aerial photos and a 2 m WorldView-3 scene, 200 to
1 000 labelled pixels. Presence-and-Background Learning (a neural
network on positive vs. 5 000 unlabelled pixels, then calibrated) was
best in every scene and class, ahead of one-class SVM and binary
classifiers; the advantage comes from using unlabelled data. One-class
SVM was not always worst: in one scene it beat a neural network and a
binary SVM (Table 3). The closest support for presence-vs-background,
by analogy only (land cover, very high resolution, no spatial blocks).

**Malinowski, Krupiński, Skórka, Mikołajczyk, Chuda & Lenda (2025).**
Harnessing remote sensing and machine learning techniques for
detecting and monitoring the invasion of goldenrod invasive species.
*Scientific Reports*, 15, 32222. DOI: 10.1038/s41598-025-17440-0.
— *Read*

*Solidago* in Poland, Sentinel-2 and PlanetScope. Random Forest
outperformed one-class SVM by 1–15 points on Sentinel-2 (best F1 0.98
vs. 0.90); one-class SVM won in two single-date PlanetScope scenarios
and over-predicted extent. The closest in subject, with caveats: the
Random Forest is multi-class with real labelled samples of eight
land-cover classes, not presence-background; reference polygons are
homogeneous full-cover stands; no spatial blocks.

**Rapinel & Hubert-Moy (2021).** One-Class Classification of Natural
Vegetation Using Remote Sensing: A Review. *Remote Sensing*, 13(10),
1892. DOI: 10.3390/rs13101892. — *Read*

Review of 136 articles, 2013–2020, where "one-class" mostly means
MaxEnt-style models. No comparison of zero-background methods with
presence-background ones.

- **Background** should be drawn over the entire landscape, including
  the surroundings of occurrences, or accuracy may be overestimated;
  only 6 of 136 studies excluded field-plot areas from it. The usual
  number is 10 000 points (range 200–50 000).
- By its terms, background goes with presence-only classifiers
  (MaxEnt, biased SVM) and pseudo-absences with presence/absence
  classifiers such as Random Forest; 42% of studies confuse the two.
- Sampling bias was corrected in only 10 studies, and spatial
  autocorrelation in validation was usually ignored.
- Accuracy without absence data is biased; it recommends continuous
  maps over thresholds.

**Abstract only** (paywalled; consistent with the above, not citable
for details):

- **Li, Guo & Elkan (2011).** A Positive and Unlabeled Learning
  Algorithm for One-Class Classification of Remote-Sensing Data. *IEEE
  TGRS*, 49(2), 717–725. DOI: 10.1109/TGRS.2010.2058578. PU-learning
  outperformed biased SVM and one-class SVM on aerial scenes.
- **Li & Guo (2010).** A maximum entropy approach to one-class
  classification of remote sensing imagery. *Int. J. Remote Sensing*,
  31(8), 2227–2235. DOI: 10.1080/01431161003702245. MaxEnt beat
  one-class SVM.
- **Mack & Waske (2017).** In-depth comparisons of MaxEnt, biased SVM
  and one-class SVM for one-class classification of remote sensing
  data. *Remote Sensing Letters*, 8(3), 290–299.
  DOI: 10.1080/2150704X.2016.1265689. Biased SVM came first; even the
  best approach performed poorly in many tasks. Agrees with Li & Guo
  (2010) on one-class SVM being behind.

**Synthesis (my reading):** in the papers read, one-class SVM never
beat the best positive-unlabelled or presence-background method,
though it sometimes beat individual binary classifiers. None of these
studies matches this setup, but the thesis's own tests later agreed
with them.

### Evaluating presence-only models without confirmed absences

**Hirzel, Le Lay, Helfer, Randin & Guisan (2006).** Evaluating the
ability of habitat suitability models to predict species presences.
*Ecological Modelling*, 199(2), 142–152.
DOI: 10.1016/j.ecolmodel.2006.05.017 — *Read*

Introduces the **continuous Boyce index**. For each class of predicted
values, P is the share of evaluation presences and E the share of the
study area's cells in that class; the index is the Spearman
correlation between P/E and the class rank, from −1 to 1. Positive
means predictions are consistent with the distribution of presences,
near zero no better than chance, negative an incorrect model. Tested
on 114 alpine plant species (Swiss Alps, GLMs, 5-fold
cross-validation): correlated above 0.5 with AUC in most cases,
fairly insensitive to prevalence.

- **Moving window:** width 0.1 recommended, shifted upward in small
  steps over [0, 1]; wider windows and more than ten fixed classes
  both behave poorly.
- **It cannot rank models with monotone curves:** being rank-based,
  the indices "cannot discriminate between monotonic curves" (p. 150).
  A value near 1 means only that P/E rises with the score.
- **No guidance on near-ceiling values.** In the paper the median was
  −0.07 and the maximum 0.61, against a median AUC of 0.88.
- **Report the P/E curve itself:** its shape, its maximum and its
  variance across folds.
- Agreement with presence/absence metrics drops below about 50
  presences; evaluation data should ideally be independent.
- It needs predictions over the whole study area for E; a random
  background sample is an approximation of that, so the index is not
  background-free.

**No method was found that evaluates a presence-only model without
any background or unlabelled sample.** Even a zero-background training
method needs background data to be evaluated, which is why the shared
background pool exists.

### Spatial validation

**Karasiak, Dejoux, Monteil & Sheeren (2022).** Spatial dependence
between training and test sets: another pitfall of classification
accuracy assessment in remote sensing. *Machine Learning*, 111(7),
2715–2740. DOI:
[10.1007/s10994-021-05972-1](https://doi.org/10.1007/s10994-021-05972-1)
(online 2021). — *Read*

Sentinel-2 forest classification over one 100 km tile. Non-spatial
cross-validation overestimated overall accuracy by 8 to 14 points
against distant sites; spatial leave-one-out matched them (82.1%,
against 93.7% for k-fold).

- **The buffer is derived from the data:** Moran's I per band over
  increasing neighbourhoods, and the buffer is the distance where it
  falls to 0.05 — about **19.7 km** here.
- **Blocks without a buffer are not enough:** with blocks "residual
  correlation may exist"; "finding the ideal block size does not solve
  the problem, but the distance-based buffer approach avoids it" (§5).
- **Object-level splitting is the minimum:** all pixels of one polygon
  go to training or to test (§6).
- A 20 m inner buffer appears only to erode stand edges, unrelated to
  train/test separation.
- Released **Museo ToolBox**; its `SpatialLeaveOneOut` documents the
  distance threshold in pixels (software docstring, not the paper).

**Not in the paper:** duplicate samples in one pixel, or thinning to
one sample per pixel. It is about dependence between training and test
sets.

**Le Rest, Pinaud, Monestiez, Chadoeuf & Bretagnolle (2014).** Spatial
leave-one-out cross-validation for variable selection in the presence
of spatial autocorrelation. *Global Ecology and Biogeography*, 23(7),
811–820. DOI:
[10.1111/geb.12161](https://doi.org/10.1111/geb.12161) — *Read*

A variable-selection paper for generalised linear models, not a
map-accuracy paper. Formalises spatial leave-one-out with the buffer
set to the **range of residual spatial autocorrelation**, from the
variogram of the full model's residuals. Underestimating the range is
the unsafe direction: results were stable from the range (40–50 km in
its case study) up to five times it, and wrong below it. The range is
of model residuals, a different quantity from the autocorrelation of
predictors.

**Mahoney, Johnson, Silge, Frick, Kuhn & Beier (2023).** Assessing the
performance of spatial cross-validation approaches for models of
spatially structured data. arXiv:2303.07334. — *Read*

Simulation study (Random Forest regression on a regular grid)
comparing V-fold, blocked, clustered, buffered
leave-one-observation-out and leave-one-disc-out cross-validation.
The buffer distance is "a matter of some debate", with suggestions to
use the variogram range of the predictors, outcome or residuals.

- **Best estimates come from spatially contiguous assessment sets
  combined with exclusion buffers.** The best blocked settings all use
  a buffer; blocks without a buffer are not reported.
- Buffered leave-one-observation-out did no better than random V-fold
  (1.3% vs. 2.0% of iterations in the target range; blocked 27.9%,
  clustered 37.0%).
- The best settings separated sets by 25–41% of the grid length,
  against an outcome autocorrelation range of about 25%.
- Too few folds overestimates error. Clustered sampling, as in
  citizen science, is not covered. Introduces the R package
  `spatialsample`.

**Meyer & Pebesma (2021).** Predicting into unknown space? Estimating
the area of applicability of spatial prediction models. *Methods in
Ecology and Evolution*, 12(9), 1620–1633. DOI:
[10.1111/2041-210X.13650](https://doi.org/10.1111/2041-210X.13650)
— *Read (journal version, which differs from the arXiv preprint)*

Defines a dissimilarity index (DI): distance in predictor space from a
location to its nearest training point, with predictors standardised
and weighted by variable importance, divided by the mean pairwise
distance among training points; for training points, the nearest
point outside their own cross-validation fold. The area of
applicability (AOA) is where DI stays below the outlier-removed
maximum of the training data's cross-validated DI (75th percentile
+ 1.5 × IQR).

- Tested on simulated responses over Europe (Random Forest, 19
  bioclimatic predictors, 972 scenarios), including clustered training
  data with leave-cluster-out validation. Case study: RMSE 0.07 inside
  the AOA, 0.44 outside; DI correlates with true absolute error
  (r = 0.71).
- **The AOA depends on the cross-validation design:** with random
  folds on clustered data it shrinks to almost nothing.
- **The AOA is binary.** A continuous error estimate is a separate
  step (a model of error against DI), and its tested strength is weak
  (mean R² 0.21 across scenarios).
- It is "a precondition for reliable predictions, but … in no way … a
  guarantee".
- **Only tested on regression** with Random Forest and simulated data.
  Classification, presence-background data and high-dimensional
  learned embeddings are not addressed, so using it on TESSERA with a
  classifier is an extension.
- The variable-importance method changes the result. Implemented in
  the R package `CAST`.

**Applied here:** this project's own empirical variogram
result and what it was used for (not a paper finding) is logged in
[`thesis/notes.md`](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km),
notebook:
[`notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb`](../notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb).

### *Acacia* fire ecology

**Riveiro, Nereu, Reyes & Silva (2025).** Effectiveness of slash and
burn treatments in controlling *Acacia dealbata* Link invasion.
*Biological Invasions*, 27, 125.
DOI: [10.1007/s10530-025-03567-8](https://doi.org/10.1007/s10530-025-03567-8)
— *Read*

Eight stands, all in the Coimbra district, treated between 2018 and
2021 and monitored for up to three years. Burning promoted
*A. dealbata* seed germination; slashing stimulated resprouting. No
treatment prevented regeneration (at least 6.5 stems/m², 0 in
controls), and regrowth after two to three years is low seedlings and
resprouts, not a mature canopy.

**What it supports:** fire does not remove *A. dealbata*, so absence
cannot be assumed after a burn. **What it does not:** the burns were
prescribed, in 5 × 5 m plots, not wildfires, and the paper has no
remote sensing. Stand persistence appears only as one introduction
sentence citing Boland (1986) and as undisturbed control plots.

### Weak supervision from point labels

**Rivier, Hinojosa, Giancola & Ghanem (2024).** Efficient Semantic
Segmentation for Aerial Imagery Using Query Points and Superpixel
Supervision. IEEE ICIP 2024, pp. 2292–2298,
DOI: [10.1109/ICIP51287.2024.10647646](https://doi.org/10.1109/ICIP51287.2024.10647646);
arXiv:2309.05490.
PDF: [`literature/rivier_2024_superpixel_query_points.pdf`](literature/rivier_2024_superpixel_query_points.pdf).
Recommended by the supervisor for the segmentation mask (see
[RQ2](research_questions.md#rq2--from-point-observations-to-reference-data)).
— *Read*

Trains a full segmentation network (DeepLabV3, U-Net, FCN) from sparse
point labels (10–50 per 512 × 512 image) via superpixel propagation:
superpixels come from DAL-HERS, each takes the majority class among
the points inside it, and superpixels with no point are left out of
the loss. mIoU 75.64% on LandCoverAI (25–50 cm RGB aerial imagery,
four classes), against 83.99% fully supervised.

- **Points are simulated:** random pixels drawn from the ground-truth
  mask, so correctly labelled by construction.
- **Superpixel count:** 80–100 per image is best, 200–300 worse; 80 is
  the fewest DAL-HERS could produce, so nothing coarser was tested.
- Only the downstream mIoU is reported; the accuracy of the propagated
  masks is never measured.
- Differences from this thesis: sub-metre RGB imagery, an end-to-end
  trained network, and noise-free points. It supports the idea of
  propagating a point to its superpixel and gives no parameter usable
  at 10 m.

**Raine, Marchant, Kusy, Maire & Fischer (2022).** Point Label Aware
Superpixels for Multi-species Segmentation of Underwater Imagery.
*IEEE Robotics and Automation Letters*, 7(3), 8291–8298.
DOI: [10.1109/LRA.2022.3187836](https://doi.org/10.1109/LRA.2022.3187836),
arXiv:2202.13487. — *Read (arXiv accepted version)*

Not remote sensing (coral photo-quadrats), but species-level: sparse
ecologist point labels propagated to multi-species segmentation, 100
superpixels per 512 × 512 image, majority vote inside each.

- **Few points do badly:** propagation accuracy is 89–92% at 300
  points per image, 84–86% at 100, 79–81% at 50, 71–73% at 20 and
  64–68% at 10 (Fig. 4). Unlike Rivier, the propagated labels are
  measured directly.
- **Features matter less than the summary numbers suggest:** their
  method on learned features reaches 89.6–92.6% against 64.1% on raw
  colour, but colour-based baselines reach 86.6–88.9% and a
  randomly initialised encoder 87.9%; the authors conclude the
  algorithm "is not sensitive to the pixel features" (§V-B.2).
- Superpixels are shaped by the labels through a loss between
  differing classes, which has nothing to act on with presence-only
  labels.
- Unlabelled superpixels take the class of the most feature-similar
  labelled one, a rule that would label everything in a presence-only
  setting.
- Notes that earlier point-supervision work assumes points are placed
  centrally within the objects of interest (§II-B).

**Zhang, Tang, Corpetti & Zhao (2021).** WTS: A Weakly towards
Strongly Supervised Learning Framework for Remote Sensing Land Cover
Classification Using Segmentation Models. *Remote Sensing*, 13(3),
394. DOI: [10.3390/rs13030394](https://doi.org/10.3390/rs13030394)
— *Read*

Sentinel-2 (20 m, north-west France), 16 844 labelled points in five
classes. An SVM trained on the points labels high-confidence pixels as
seeds; a U-Net is trained on them; seeded region growing on the
U-Net's class-probability maps, after a fully connected CRF, enlarges
the labelled set over eight iterations. Overall accuracy 0.825 against
0.797 for the SVM on the same points.

- **Growth criterion:** a neighbour joins a class if that class is its
  most probable and the probability exceeds a threshold (0.95, raised
  each iteration). It grows on classifier confidence, not on
  similarity to the seed, and has no radius limit.
- Growth starts from SVM-densified seeds, not from the labelled
  points.
- Without the CRF accuracy hardly improves; with a stricter seed
  threshold it falls in later iterations.

A remote-sensing precedent for densifying point labels by region
growing at Sentinel-2 scale, but as iterative self-training with a
trained multi-class model.

**No paper read grows a region on feature similarity to the seed or
limits its radius**, the two elements of the RQ2 region-growing rule.

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
   (Gillespie 2024; Dimson 2023).
2. Remote sensing → invasive plant mapping, including *Acacia* in
   Iberia (Martins 2016; Mouta 2021; Domingo 2023).
3. Deep learning → plant species mapping (Gillespie 2024).
4. Citizen science + remote sensing → plant mapping (Gillespie 2024),
   including invasive plants at 256 m (Qiang 2026).
5. EO foundation models vs. conventional features → many tasks:
   trees (Ball 2026), crops (Yang 2026), and burned area in Portugal,
   where the conventional features won (Silva & Gonçalves 2026).
6. EO foundation models + iNaturalist labels → genus-level evaluation
   (Brown 2025); habitat mapping with GBIF labels in progress
   (Cambridge).
7. EO foundation models → label efficiency (Ball 2026).
8. Embedding-based models lose accuracy when moved to another region
   (Yang 2026), and their advantage over Sentinel features narrows
   when training and test sets are separated by a buffer (Ratsakatika
   2026).
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
  a generic benchmark, with no analysis of label bias.
- Cambridge TESSERA group: foundation models + GBIF labels with
  observed clustering, but habitats, and not yet published.
- Qiang et al. (2026): invasive plants + citizen science + remote
  sensing, but 256 m and no foundation models.
- Dimson et al. (2023): citizen-science bias for invasive plants, but
  no foundation models.
- Yang et al. (2026) and Ratsakatika et al. (2026): embeddings under
  spatial transfer or separation, but not with concentrated
  citizen-science labels, and not compared with conventional features
  away from the sampled area.

Four specific questions not answered by any of the above:

1. **How much is lost by training on citizen science instead of
   expert reference data**, with the same representation and test
   set? (RQ1)
2. **Does extending a citizen-science point label to the patch around
   it, using frozen embeddings, change mapping performance?** Existing
   point-to-patch work uses many correctly placed points per image and
   trained segmentation networks (Rivier 2024; Raine 2022). (RQ2)
3. **Does a model trained on spatially concentrated citizen-science
   observations lose performance away from the sampled area?** (RQ3)
   Whether foundation models amplify or mitigate that effect, compared
   with conventional features, is also unanswered and is not tested in
   this thesis.
4. **Do foundation-model embeddings improve on conventional
   Sentinel-2 features when the labels are citizen-science points for
   an invasive plant?** Ball et al. (2026) make the comparison with
   curated tree-species labels. (RQ4)

## Contribution

**Citizen science as a substitute for expert reference data in
invasive plant mapping with EO foundation models.** Not "apply TESSERA
to invasive plants", but a controlled study of how far
citizen-science observations, turned into reference data, can replace
expert reference data: with increasing amounts of expert data, with
point labels extended to patches, away from the sampled area, and
against a conventional satellite baseline. Wording mine, to confirm
with the supervisor.

Two parts:

1. **Methodological:** a documented, justified pipeline that turns
   citizen-science points into satellite reference data (the
   proposal's first objective; see
   [Reference-Data Pipeline](research_questions.md#reference-data-pipeline-proposed)) —
   each step documented and justified from literature or data. A
   cumulative ablation measuring each step's effect is an optional
   stretch goal. The segmentation mask, which extends a
   citizen-science point to the patch around it using frozen
   embeddings, has no precedent found and is tested in
   [RQ2](research_questions.md#rq2--from-point-observations-to-reference-data),
   together with the effect of the grade and accuracy filters.
2. **Empirical:** RQ1–RQ4 in
   [`research_questions.md`](research_questions.md).
