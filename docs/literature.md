# Literature

A small set of directly relevant papers, **not** a systematic review.
"Appears underexplored" claims reflect this reading list only and
must be revisited after a broader search (Web of Science, Scopus,
Google Scholar).

## Papers

### EO foundation models and species mapping

**Ball et al. (2026).** Geospatial foundation models enable
data-efficient tree species mapping in temperate mountain forests.
*Science of Remote Sensing*, 14, 100466.
DOI: [10.1016/j.srs.2026.100466](https://doi.org/10.1016/j.srs.2026.100466)

Compares TESSERA embeddings, AlphaEarth embeddings and conventional
Sentinel-1 + Sentinel-2 features for 18 tree species/groups
(parcel-level forest inventories) in Trentino, Italy.

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

### Citizen science + remote sensing + plant mapping

**Gillespie et al. (2024).** Deep learning models map rapid plant
species changes from citizen science and remote sensing data.
*PNAS*, 121(37), e2318296121.
DOI: [10.1073/pnas.2318296121](https://doi.org/10.1073/pnas.2318296121)

Deepbiosphere: 650,000+ research-grade (mostly iNaturalist)
observations of 2,221 plant species, paired with remote sensing and
deep learning, in California only. Beats conventional SDM baselines
(AUC 0.95 vs. 0.88). No EO foundation models, no focus on invasive
species or data sparsity/bias.

### Citizen science + invasive plants + deep learning

**Cardoso et al. (2024).** Can citizen science and social media
images support the detection of new invasion sites? A deep learning
test case with *Cortaderia selloana*. *Ecological Informatics*, 81,
102602. DOI: [10.1016/j.ecoinf.2024.102602](https://doi.org/10.1016/j.ecoinf.2024.102602)

CNNs on ground-level citizen-science and social-media photos detect
*Cortaderia selloana* in Portugal (>77% identification success) and
map unreported occurrences. Image-based computer vision, not
satellite EO.

### Citizen-science sampling bias

**Dimson et al. (2023).** Citizen science can complement professional
invasive plant surveys and improve estimates of suitable habitat.
*Diversity and Distributions*.
DOI: [10.1111/ddi.13749](https://doi.org/10.1111/ddi.13749)

Hawaiʻi, four invasive species. iNaturalist records are biased toward
roads/trails and disturbed vegetation; professional surveys toward
less accessible, native-dominated sites. Habitat models from each
source overlap only moderately; combining both gives more complete
estimates. Whether the same bias axes hold in Portugal is untested.

### Conventional invasive plant mapping

**Mouta et al. (2021).** 'The Best of Two Worlds' — Combining
Classifier Fusion and Ecological Models to Map and Explain Landscape
Invasion by an Alien Shrub. *Remote Sensing*, 13(16), 3287.
DOI: [10.3390/rs13163287](https://doi.org/10.3390/rs13163287)

Maps *Acacia longifolia* in a northern Portugal municipality with
Sentinel-2 (10 m), a fusion of eight classifiers, and Random Forest
to explain invasion drivers. Portuguese precedent for a credible
conventional baseline.

**Domingo et al. (2023).** Assessing the Efficacy of Phenological
Spectral Differences to Detect Invasive Alien *Acacia dealbata* Using
Sentinel-2 Data in Southern Europe. *Remote Sensing*, 15(3), 722.
DOI: [10.3390/rs15030722](https://doi.org/10.3390/rs15030722)

Sentinel-2 time series and flowering-period spectral differences,
with Random Forest feature selection, map *A. dealbata* in Arnoia
(Ourense, Galicia): 94% overall accuracy with six metrics. Sentinel-2
only; no spatial cross-validation confirmed.

**Eskandari, Acuña-Alonso & Álvarez (2025).** Identification of
Acacia invasive species in protected areas of Spain using PlanetScope
high-resolution satellite images and machine learning models in time
series. *Forest Ecology and Management*, 586, 122696.
DOI: [10.1016/j.foreco.2025.122696](https://doi.org/10.1016/j.foreco.2025.122696)

PlanetScope time series + Random Forest map *Acacia* sp. in the Cíes
Islands, Galicia; Random Forest beat the other algorithms. Specific
area-change figures (2016–2024) are **unverified** — the publisher
page blocks automated access.

### Weak supervision from point labels

**Rivier et al. (2023/2024).** Efficient Semantic Segmentation for
Aerial Imagery Using Query Points and Superpixel Supervision.
arXiv:2309.05490v2.

Trains segmentation from sparse point labels (as few as 50 per image)
via superpixel propagation and a loss on labelled pixels only;
mIoU 75.64% on LandCoverAI, close to full supervision. A method lead
only: relevant if the task ever moves from point classification to
segmentation (currently rejected, see
[`research_questions.md`](research_questions.md#prediction-task-adopted)).

## What Has Already Been Done

1. Citizen science → plant/invasive-species observations at scale
   (Gillespie 2024; Dimson 2023; Cardoso 2024).
2. Remote sensing → invasive plant mapping (Mouta 2021; Domingo 2023;
   Eskandari 2025).
3. Deep learning → plant species mapping (Gillespie 2024; Cardoso
   2024).
4. Citizen science + remote sensing → plant mapping (Gillespie 2024).
5. EO foundation models → species mapping (Ball 2026, trees).
6. EO foundation models → label efficiency (Ball 2026).
7. Citizen-science invasive-plant data are spatially biased (Dimson
   2023).

None of these, on its own, is this thesis's novelty.

## Gap

Each ingredient has prior work; their intersection — **EO foundation
models + invasive plant mapping + citizen-science reference data,
with explicit evaluation of sparsity and spatial bias** — appears
underexplored:

- Ball et al. (2026): foundation models + label efficiency, but tree
  species with curated labels.
- Dimson et al. (2023): citizen-science bias for invasive plants, but
  no foundation models.
- Cardoso et al. (2024): citizen science + invasive plants in
  Portugal, but ground-level images, not satellite EO.

## Contribution

**Data-efficient and bias-aware invasive plant mapping using EO
foundation models and citizen science.** Not "apply TESSERA to
invasive plants", but a controlled study of how foundation-model
representations behave under realistic citizen-science limitations
(sparsity, spatial bias), against a conventional satellite baseline.
The resulting questions are in
[`research_questions.md`](research_questions.md).
