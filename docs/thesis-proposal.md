# Advancing the Mapping of Invasive Alien Plants by Combining Citizen Science, Earth Observation Foundation Models and Satellite Imagery

## Enquadramento

Invasive alien plants (IAP) are species introduced outside their native range that establish and spread without direct human intervention. They are recognised as one of the five main drivers of global biodiversity loss, causing severe ecological impacts and economic losses estimated at over 12 billion euros per year in Europe and worldwide.

Reliable, up-to-date spatial information on IAP distribution is essential for effective prevention, control, and impact assessment. However, existing products developed by national and European institutions are often updated infrequently, spatially coarse, and lack species-level detail, limiting their operational usefulness. Although Earth Observation (EO) offers strong potential for IAP mapping, a key limitation remains the scarcity of high-quality reference data required for supervised learning approaches.

At the same time, citizen science platforms such as iNaturalist provide publicly available, species-specific, geolocated observations of invasive plants. While rich in content, these data are point-based and heterogeneous in quality, making their direct use in satellite-based classification challenging.

Recent advances in Earth observation foundation models, pre-trained on large volumes of EO data (e.g., satellite imagery using both optical and radar bands, auxiliary georeferenced data) using self-supervised learning, offer a promising solution. These models provide robust and transferable feature representations that can be fine-tuned with limited and noisy training data, potentially enabling the effective use of citizen science observations.

This MSc project is conducted within the framework of the ongoing research project MAP.INVADER (www.mapinvader.pt), which focuses on innovative EO-based methods for mapping and monitoring invasive alien plants.

## Objetivo

The main objective of this project is to reduce the dependency on costly and time-consuming reference data generation by leveraging citizen science point-based observations to create training data for satellite-image-based classifiers of invasive alien plants.

Specifically, the project aims to:

- Investigate methods to transform citizen science species observations into usable EO reference data.
- Exploit the representational power of EO foundation models to compensate for the limited and noisy nature of citizen science data.
- Assess to what extent citizen science contributions can support accurate, species-level mapping of invasive alien plants using satellite imagery.

## Plano de Trabalhos

1. Literature review on the use of citizen science data for EO-based mapping and environmental monitoring, with emphasis on invasive species applications. Study recent developments, architectures, and applications of EO foundation models, focusing on fine-tuning strategies for vegetation and land cover mapping.
2. Collect and curate citizen science observations (e.g., from iNaturalist) regarding invasive alien plants, focusing on a limited number of representative species.
3. Develop methodologies to transform point-based citizen science observations into spatial reference data compatible with satellite imagery, accounting for uncertainty and data quality.
4. Fine-tune EO foundation models using the generated reference data and evaluate their performance for invasive alien plant mapping, analysing accuracy, limitations, and transferability.

## Condições

- All required datasets, including satellite imagery and citizen science observations, are publicly available.