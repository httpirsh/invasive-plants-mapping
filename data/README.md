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

Data files are not version-controlled (see `.gitignore`); this file
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

## Not Yet Obtained

| Source | Use | Status |
|---|---|---|
| **Sentinel-2** (and possibly Sentinel-1), 10 m, open | Conventional baseline (RQ1–RQ3); precedent: Mouta et al. (2021) | Needs Copernicus Data Space or Google Earth Engine account |
| **OrtoSat 30 cm** (Pleiades-Neo, RGB+NIR, continental Portugal, Apr–Oct 2023, CC BY 4.0) | Possible validation reference | Full resolution restricted to public-administration entities; only WMS confirmed public. University access unconfirmed |
| **AlphaEarth embeddings** | Second foundation model (RQ1) | Access terms unconfirmed |
| **iNaturalist other plants** (same area/window) | Target-group background (absences) | Not downloaded |
| **ICNF burned areas** | Disturbance filter | Not downloaded |
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
