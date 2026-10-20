# Data

```
data/
├── raw/                  ← original, unmodified data
│   ├── citizen_science/
│   └── satellite/
├── interim/              ← data after intermediate processing
│   ├── citizen_science/
│   ├── satellite/
│   └── spatial/          ← intermediate spatial joins/products
├── processed/            ← final data used by the models
│   ├── datasets/          ← labelled ML-ready datasets
│   ├── features/          ← conventional (non-foundation-model) features
│   └── embeddings/        ← Earth Observation Foundation Model embeddings
└── external/             ← auxiliary third-party data
    ├── shapefiles/
    ├── land_cover/
    └── auxiliary/
```

Data files are not version-controlled (see `.gitignore`), except the
expert reference polygons in `raw/expert_reference/` (the repository
is private; do not make it public while they are included). This file
documents the provenance of each dataset and the candidates not yet
obtained.

## Obtained (pilot downloads)

> Pulled to validate access, not a final choice of region, species or
> source. The iNaturalist and TESSERA pilots use **different Coimbra
> boundaries** (district vs. municipality) — to reconcile before any
> real experiment.

### iNaturalist *Acacia* observations (Coimbra pilot)

- **Source:** iNaturalist API (`api.inaturalist.org/v1/observations`)
- **URL:** https://www.inaturalist.org/observations?place_id=8422&taxon_id=47452
- **Access date:** 2026-09-22
- **Spatial coverage:** place id 8422, "Coimbra, PT" — resolves to the
  **Coimbra district** (bbox lon -8.9596 to -7.7318, lat 39.9238 to
  40.5333), not the municipality.
- **Temporal coverage:** 1992–2026 (no date filter); 43% of records
  from 2021.
- **License:** mixed, per observation (`license_code` column) — check
  before redistribution.
- **Query filters:** `place_id=8422`, `taxon_id=47452` (genus
  *Acacia*, all descendants), all quality grades (`quality_grade`
  column kept; filtering left to modelling code).
- **Result:** 7,943 observations.
- **File:** `raw/citizen_science/inaturalist_acacia_coimbra_pilot.csv`
- **Preprocessing:** none — one row per observation (id, date, taxon,
  coordinates, positional accuracy, quality grade, place guess,
  license, observer, URI).

### TESSERA embeddings (Coimbra pilot)

- **Source:** GeoTessera (`geotessera` package / data.source.coop/tessera)
- **URL:** https://geotessera.org ; data at
  https://data.source.coop/tessera/tessera
- **Access date:** 2026-09-22
- **Spatial coverage:** bbox lon -8.5917 to -8.3129, lat 40.0989 to
  40.3520 — the **Coimbra municipality** (OSM relation 5379538). 12
  tiles on the 0.1° (~11 km) grid.
- **Temporal coverage:** 2024 only (one annual composite of
  Sentinel-1/2). The proposed design needs 2023.
- **License:** MIT.
- **Format:** quantized `npy` (128-channel embeddings + per-tile scale
  factors + landmask GeoTIFFs), ~1.5 GB. GeoTIFF format would be
  ~5.5 GB.
- **File:** `raw/satellite/tessera_coimbra_pilot/`
  (`global_0.1_degree_representation/2024/grid_<lon>_<lat>/`)
- **Preprocessing:** none — `geotessera download --bbox ... --year 2024 --format npy`.
  Dequantization is a downstream step.

### COS 2023 (Carta de Uso e Ocupação do Solo, Série 2)

- **Source:** Direção-Geral do Território (DGT), via dados.gov.pt
- **URL:** https://dados.gov.pt/datasets/carta-de-uso-e-ocupacao-do-solo-cos-serie-2-2018v3-2023v1
  (file: https://geo2.dgterritorio.gov.pt/cos/S2/COS2023/COS2023v1-S2-gpkg.zip)
- **Access date:** 2026-09-22
- **Spatial coverage:** continental Portugal (not clipped).
- **Temporal coverage:** 2023 (COS2023v1).
- **License:** CC BY 4.0.
- **Format:** vector GeoPackage, 93 classes, minimum mapping unit
  1 ha, scale 1:25,000.
- **File:** `raw/satellite/cos/COS2023v1-S2-gpkg.zip` (857 MB, not
  unzipped).
- **Preprocessing:** none.
- **Possible uses:** land-cover context for error analysis, absence
  checks, independent validation.

### iNaturalist other plants, all years (Coimbra pilot)

Other-plant classes (see `docs/research_questions.md`).

- **Source:** iNaturalist API (`api.inaturalist.org/v1/observations`)
- **Access date:** 2026-10-17 (2021–2025); 2026-10-20 (other ranges)
- **Query filters:** `place_id=8422` (Coimbra district), `taxon_id=47126`
  (Plantae), `without_taxon_id=47452` (excluding *Acacia*), all
  quality grades. Downloaded in three date ranges: `d2=2020-12-31`,
  `d1=2021-01-01` + `d2=2025-12-31`, `d1=2026-01-01`.
- **Temporal coverage:** 1976–2026 (observations without a date are
  not returned by the date filters).
- **License:** mixed, per observation (`license_code` column).
- **Result:** 120,479 observations (11,924 before 2021; 85,543 in
  2021–2025; 23,012 in 2026); 9,903 have obscured coordinates (user
  or taxon geoprivacy), listed in the matching `*_obscured_ids.csv`
  files and excluded in analysis.
- **Files:** `raw/citizen_science/inaturalist_plantae_no_acacia_coimbra_{before_2021,2021_2025,from_2026}.csv`
  and `..._obscured_ids.csv` per range.
- **Preprocessing:** none — one row per observation, same columns as
  the *Acacia* pilot. Downloaded by
  `notebooks/04_data_integration/background_and_disturbance_checks.ipynb`.

### ICNF burned areas, 1975–2025

- **Source:** ICNF, "Áreas ardidas (desde 1975)", via dados.gov.pt
- **URL:** https://dados.gov.pt/datasets/areas-ardidas-desde-1975 ; WFS
  https://si.icnf.pt/wfs/areas_ardidas
- **Access date:** 2026-10-17 (2021–2025); 2026-10-20 (1975–2020)
- **Spatial coverage:** continental Portugal (full layers, not clipped).
- **Temporal coverage:** 1975–2025. Grouped layers `BDG:ardida_1975_1989`,
  `BDG:ardida_1990_1999`, `BDG:ardida_2000_2008`, then one layer per
  year (`BDG:ardida_<year>`, 2009–2025). Every fire has a year (`Ano`);
  most fires from 2014 also have a start date (`DH_Inicio`), older
  ones do not.
- **License:** not specified on dados.gov.pt — check before
  redistribution.
- **Format:** GeoJSON, EPSG:3763.
- **File:** `external/auxiliary/icnf_burned_areas/ardida_<layer>.geojson`
- **Preprocessing:** none. Downloaded by the same notebook.

### *Acacia dealbata* expert reference polygons

Expert reference data for the RQ1 upper bound (see
`docs/research_questions.md`).

- **Source:** sent by the supervisor by email. Collected by visual
  interpretation and/or field work.
- **Access date:** 2026-10-20
- **Files:** `raw/expert_reference/TNE_17MAY2026_5.gpkg`
  (Sentinel-2 tile TNE only, layer `tne`, 7 057 polygons) and
  `raw/expert_reference/notTNE_18MAY2026_6.gpkg` (rest of
  continental Portugal, 437 polygons).
- **Attributes:** only `classifica`. Use `classifica = 1`
  (*A. dealbata* present): 2 072 polygons in TNE, 398 elsewhere. Other
  values are "not *A. dealbata*" but, per the sender, many lie on water
  or built-up areas and are of little use.
- **Spatial coverage:** continental Portugal, sparse; tile TNE covers
  the Coimbra district (1 849 positive polygons in the district).
- **Temporal coverage:** not stated (no date field) — to ask.
- **License:** not stated; project data shared for the thesis — do not
  redistribute. Versioned in this private repository.
- **Format:** GeoPackage, EPSG:3763.
- **Preprocessing:** none.

## Not Yet Obtained

| Source | Use | Status |
|---|---|---|
| **Sentinel-2** (and possibly Sentinel-1), 10 m, open | Conventional baseline (RQ1–RQ3); precedent: Mouta et al. (2021) | Needs Copernicus Data Space or Google Earth Engine account |
| **OrtoSat 30 cm** (Pleiades-Neo, RGB+NIR, continental Portugal, Apr–Oct 2023, CC BY 4.0) | Possible validation reference | Full resolution restricted to public-administration entities; only WMS confirmed public. University access unconfirmed |
| **AlphaEarth embeddings** | Second foundation model (RQ1) | Access terms unconfirmed |
| **Roads/trails, accessibility** (e.g. OpenStreetMap) | RQ3 bias covariates | Not downloaded |
| **CAOP administrative boundaries** | Study-area clipping | Not downloaded (bounding boxes used) |
| **A second, distinct region** | RQ3 geographic comparison | Not chosen |

Scope (proposed, not decided): start with Coimbra as a pilot, extend
to continental Portugal once the pipeline works. GBIF (which
aggregates iNaturalist and other sources) is an alternative to the
iNaturalist API.

## Template

### Dataset: <name>

- **Source:**
- **URL:**
- **Access date:**
- **Spatial coverage:**
- **Temporal coverage:**
- **License:**
- **Preprocessing:**
