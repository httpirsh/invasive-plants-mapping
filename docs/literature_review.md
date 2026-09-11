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
groups in Trentino, Italy. Evaluates classification performance,
label efficiency, classifier complexity, sensitivity to label
impurity, and temporal transferability. Foundation-model embeddings
outperform conventional baselines and approach performance saturation
with a small fraction of the training labels. Concludes that
foundation models may shift the practical bottleneck away from
feature engineering and toward the availability, quality, and
temporal alignment of ecological reference data.

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

Develops Deepbiosphere: more than 650,000 iNaturalist observations
across 2,221 plant species, paired with remote-sensing imagery and
deep learning, for species distribution mapping and temporal
monitoring of plant-community change, at large geographic scale.

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

Investigates iNaturalist observations of invasive plants and
quantifies systematic spatial sampling bias: observations are biased
toward roads/trails, accessible locations, and disturbed vegetation.
Compares citizen-science observations against professional survey
data and shows resulting habitat-suitability estimates can differ.

Relevance: establishes that citizen-science invasive-plant
observations can contain systematic spatial sampling bias — "citizen
science is biased" is therefore not, on its own, a novel claim for
this thesis. Motivates the sampling-bias experiment in
[research_gaps.md](research_gaps.md).

## Conventional Invasive Plant Mapping

### Mouta et al. (2021)

The Best of Two Worlds — Combining Classifier Fusion and Ecological
Models to Map and Explain Landscape Invasion by an Alien Shrub.
(*Acacia longifolia*, Portugal.)

Maps *Acacia longifolia* invasion using Sentinel-2 imagery,
machine-learning/statistical classifiers, classifier fusion, and
ecological modelling. Demonstrates that invasive alien plants can be
mapped effectively with conventional EO features and ML.

Relevance: Portuguese precedent for a credible conventional
satellite + ML baseline, which this thesis should match or exceed
before attributing any advantage to foundation models.

### Recent Sentinel-1/Sentinel-2 + ML invasive-plant studies (citation needed)

Referenced qualitatively (not yet a verified citation) as recent work
combining Sentinel-1/Sentinel-2 optical/radar fusion, Random Forest,
and spatial cross-validation for invasive plant mapping, reportedly
including *Acacia* mapping in Galicia/Northern Iberia.

**Action needed:** identify and add the actual paper(s) before citing
this in the thesis; do not cite this entry as a verified source in the
meantime.

Relevance: if confirmed, reinforces that conventional EO + ML for
invasive plants is an active research area, further supporting that
this should be treated as a baseline rather than a contribution.
