# Literature Review

> **Status: early / partial.** This is not a systematic review. It
> currently covers a small set of directly relevant papers identified
> so far, used in [`research_gaps.md`](research_gaps.md) to scope the
> thesis contribution. Expected areas of coverage:
>
> - Invasive alien plant mapping and species distribution modelling
> - Citizen science data quality, bias and use in ecological modelling
> - Earth Observation for vegetation and invasive species detection
> - Earth Observation Foundation Models and their representations
> - Spatially aware model evaluation

## Earth Observation Foundation Models and Species Mapping

### Ball et al. (2026)

Geospatial foundation models enable data-efficient tree species
mapping in temperate mountain forests. *Science of Remote Sensing*,
14, 100466. DOI: [10.1016/j.srs.2026.100466](https://doi.org/10.1016/j.srs.2026.100466)

Compares TESSERA embeddings, AlphaEarth embeddings, and conventional
Sentinel-1 + Sentinel-2 features for mapping 18 tree species/species
groups (parcel-level forest inventories) in Trentino, Italy. Verified
against the paper's own summary (2026-09-11):

- **Classification performance:** foundation-model embeddings beat
  conventional composites (weighted F1 0.83 vs. 0.80; macro F1 0.55
  vs. 0.50).
- **Label efficiency:** near-optimal accuracy reached with as little
  as ~5% of available training parcels.
- **Classifier complexity:** a compact neural network was optimal,
  outperforming Random Forest and matching deeper networks; linear
  classifiers on foundation-model embeddings underperformed neural
  networks on conventional composites.
- **Label impurity:** robust to moderate label impurity; soft labels
  (parcel-level species proportions) outperformed hard labels (macro
  F1 0.586–0.589).
- **Temporal transferability:** performance *degraded* across years
  (weighted F1 down 9% for TESSERA, 15% for AlphaEarth), hitting rare
  species disproportionately hard.

Conclusion (near-verbatim): geospatial foundation models shift a
primary bottleneck in species mapping from feature engineering toward
the availability, quality, and temporal alignment of ecological
reference data.

Relevance: establishes EO foundation models + species mapping + label
efficiency as already studied — see
[research_gaps.md](research_gaps.md). Reference data here is
presumably more systematic than citizen-science data; this thesis
would test whether the same label-efficiency advantage holds under
citizen-science sampling conditions instead.

## Citizen Science + Remote Sensing + Plant Mapping

### Gillespie et al. (2024)

Deep learning models map rapid plant species changes from citizen
science and remote sensing data. *PNAS*, 121(37), e2318296121.
DOI: [10.1073/pnas.2318296121](https://doi.org/10.1073/pnas.2318296121)

Develops Deepbiosphere: a curated dataset of 650,000+ research-grade,
primarily iNaturalist, observations across 2,221 vascular plant
species — with a subset of ~500,000 observations used for
training — paired with remote-sensing imagery and deep learning, for
species distribution mapping and temporal monitoring of
plant-community change. **Study region: California, USA** (not a
global or multi-region study — worth noting since geographic
generalization is a concern for this thesis). Reports the model
outperforming common species distribution modelling baselines (AUC
0.95 vs. 0.88) at up to a few metres resolution.

Relevance: establishes that citizen science + remote sensing + deep
learning for plant species mapping already exists at large scale.
Does not use EO foundation-model representations or specifically
examine invasive species or reference-data sparsity/bias/temporal
mismatch.

## Citizen Science + Invasive Plants + Deep Learning

### Cardoso et al. (2024)

Can citizen science and social media images support the detection of
new invasion sites? A deep learning test case with *Cortaderia
selloana*. *Ecological Informatics*, 81, 102602.
DOI: [10.1016/j.ecoinf.2024.102602](https://doi.org/10.1016/j.ecoinf.2024.102602)

Uses citizen-science and social-media ground-level images with CNN
classification/object detection to detect and map *Cortaderia
selloana* occurrences in Portugal. Reports species identification
success in more than 77% of cases and uses the models to map
previously unreported occurrences.

Relevance: establishes Portuguese invasive-plant mapping + citizen
science + deep learning as already studied — but as image-based
computer vision on ground-level/social-media photos, not satellite EO
foundation-model representation learning. See
[research_gaps.md](research_gaps.md) for the distinction this thesis
would need to draw.

## Citizen Science Sampling Bias

### Dimson et al. (2023)

Citizen science can complement professional invasive plant surveys
and improve estimates of suitable habitat. *Diversity and
Distributions*. DOI: [10.1111/ddi.13749](https://doi.org/10.1111/ddi.13749)

**Study region: Hawaiʻi, USA** (not stated in earlier notes — added
2026-09-11). Examines four invasive plant species as examples.
Confirmed abstract: iNaturalist observations were biased toward areas
with higher road/trail density and vegetation disturbance, while
professional agency observations tended toward less accessible,
native-dominated sites. Habitat-suitability models built from each
data source showed only moderate overlap, with different distributions
across disturbance classes; combining both datasets gave more
comprehensive habitat estimates than either alone.

Relevance: establishes that citizen-science invasive-plant
observations can contain systematic spatial sampling bias — "citizen
science is biased" is therefore not, on its own, a novel claim for
this thesis. Motivates the sampling-bias experiment in
[research_gaps.md](research_gaps.md). Note the bias pattern was
documented in Hawaiʻi; whether the same road/trail/accessibility bias
axes hold for this thesis's (not yet decided) region is itself an
open question, not an assumption.

## Conventional Invasive Plant Mapping

### Mouta et al. (2021)

'The Best of Two Worlds' — Combining Classifier Fusion and Ecological
Models to Map and Explain Landscape Invasion by an Alien Shrub.
*Remote Sensing*, 13(16), 3287.
DOI: [10.3390/rs13163287](https://doi.org/10.3390/rs13163287)
(**DOI added 2026-09-11** — missing from earlier notes.)

Maps *Acacia longifolia* invasion in a municipality of northern
Portugal using Sentinel-2 (10 m) imagery, an ensemble ("classifier
fusion") of eight statistical/ML classifiers, and a Random Forest
model to explore the ecological/landscape drivers of invasion
abundance. Demonstrates that invasive alien plants can be mapped
effectively with conventional EO features and ML.

Relevance: Portuguese precedent for a credible conventional
satellite + ML baseline, which this thesis should match or exceed
before attributing any advantage to foundation models.

### Domingo et al. (2023)

Assessing the Efficacy of Phenological Spectral Differences to Detect
Invasive Alien *Acacia dealbata* Using Sentinel-2 Data in Southern
Europe. *Remote Sensing*, 15(3), 722.
DOI: [10.3390/rs15030722](https://doi.org/10.3390/rs15030722)

Uses Sentinel-2 time series and flowering-period phenological
spectral-peak differences, with machine-learning-selected spectral
metrics (random forest importance), to discriminate *Acacia dealbata*
from native vegetation in the municipality of Arnoia, Ourense
province, Galicia (Spain). Reports 94% overall accuracy using six
Sentinel-2-derived metrics.

Relevance: a verified, recent, Galicia-specific precedent for
conventional Sentinel-2 + ML invasive-plant mapping — replaces part of
the earlier "citation needed" placeholder. Note: this paper uses
Sentinel-2 only (no Sentinel-1 radar fusion), and no spatial
cross-validation was confirmed in the abstract.

### Eskandari, Acuña-Alonso & Álvarez (2025)

Identification of Acacia invasive species in protected areas of Spain
using PlanetScope high-resolution satellite images and machine
learning models in time series: an important action for protective
management of forests. *Forest Ecology and Management*, 586, 122696.
DOI: [10.1016/j.foreco.2025.122696](https://doi.org/10.1016/j.foreco.2025.122696)

Uses PlanetScope high-resolution time-series imagery and Random Forest
to map forest cover and *Acacia* sp. in the Cíes Islands, Galicia (NW
Spain). Random Forest reportedly outperformed the other algorithms
compared. Search snippets (not an independently fetched primary
abstract — publisher page blocks automated access) consistently
suggest forest cover increased 2016–2024 while mapped *Acacia* area
increased 2016–2020 then decreased 2020–2024; treat these specific
figures as **unverified** until the primary text is checked directly.

Relevance: a more recent (2025) Galicia precedent, though it uses
PlanetScope rather than Sentinel-1/Sentinel-2 — replaces the remainder
of the earlier placeholder. Together with Domingo et al. (2023), this
reinforces that conventional EO + ML for invasive Acacia mapping in
Galicia is an active, recent research area, further supporting that
this should be treated as a baseline precedent rather than this
thesis's contribution. Neither paper was confirmed to combine
Sentinel-1 radar with Sentinel-2 optical fusion and spatial
cross-validation as the original (pre-verification) research-gap notes
sketched — that specific combination remains a general characterization
of the field's direction, not a claim tied to one verified Galicia
paper.
