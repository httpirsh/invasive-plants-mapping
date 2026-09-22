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
documents the provenance of each dataset used.

## Datasets

> **Status: pilot downloads only.** These three were pulled to
> validate access and get real numbers for the open questions in
> [`docs/datasets.md`](../docs/datasets.md) — not a final choice of
> region, species, or data source. In particular, the iNaturalist and
> TESSERA pilots use **two different Coimbra boundaries** (district vs.
> municipality, respectively) because that's what each source's own
> place lookup returned; this was not reconciled and should be before
> any real experiment. OrtoSat and Sentinel-2 are not yet obtained —
> see [Not Yet Obtained](#not-yet-obtained) below.

### Dataset: iNaturalist Acacia observations (Coimbra pilot)

- **Source:** iNaturalist API (`api.inaturalist.org/v1/observations`)
- **URL:** https://www.inaturalist.org/observations?place_id=8422&taxon_id=47452
- **Access date:** 2026-09-22
- **Spatial coverage:** iNaturalist place id 8422, "Coimbra, PT" — this
  resolved to the **Coimbra district** boundary (bbox: lon
  -8.9596 to -7.7318, lat 39.9238 to 40.5333), not the smaller
  municipality/concelho. Confirm this is the intended pilot area before
  reuse.
- **Temporal coverage:** all available observation dates (no date
  filter applied); earliest/latest not yet checked.
- **License:** mixed, per-observation (`license_code` column
  retained, e.g. `cc-by`); not all records may be reusable — check
  per-record license before any redistribution.
- **Query filters:** `place_id=8422` (Coimbra, PT), `taxon_id=47452`
  (genus *Acacia*, all descendant species/subspecies), all quality
  grades (`quality_grade` column retained — not filtered to
  research-grade only; that filtering decision is left to modelling
  code, not baked into the raw download).
- **Result:** 7,943 observations.
- **File:** `raw/citizen_science/inaturalist_acacia_coimbra_pilot.csv`
- **Preprocessing:** none — one row per observation as returned by the
  API (id, date, taxon, coordinates, positional accuracy, quality
  grade, place guess, license, observer, URI).

### Dataset: TESSERA embeddings (Coimbra pilot)

- **Source:** GeoTessera (`geotessera` Python package /
  data.source.coop/tessera)
- **URL:** https://geotessera.org ; data hosted at
  https://data.source.coop/tessera/tessera
- **Access date:** 2026-09-22
- **Spatial coverage:** bbox lon -8.5917 to -8.3129, lat 40.0989 to
  40.3520 — the **Coimbra municipality/concelho** boundary (OSM/
  Nominatim relation 5379538), **not** the district boundary used for
  the iNaturalist pilot above. 12 tiles at the native 0.1°
  (~11 km) grid.
- **Temporal coverage:** year 2024 only (one annual composite; TESSERA
  compresses a full year of Sentinel-1/Sentinel-2 observations per
  embedding).
- **License:** MIT (GeoTessera library and embeddings).
- **Format/detail:** quantized `npy` format (128-channel embeddings +
  per-tile scale factors + landmask GeoTIFFs), ~1.5 GB total. GeoTIFF
  format (georeferenced, unquantized) was also considered but not
  downloaded here — would be ~5.5 GB for the same area/bands.
- **File:** `raw/satellite/tessera_coimbra_pilot/` (registry
  structure: `global_0.1_degree_representation/2024/grid_<lon>_<lat>/`)
- **Preprocessing:** none — as downloaded via
  `geotessera download --bbox ... --year 2024 --format npy`.
  Dequantizing the embeddings (using the per-tile scale files) is a
  downstream step, not yet done.

### Dataset: COS 2023 (Carta de Uso e Ocupação do Solo, Série 2)

- **Source:** Direção-Geral do Território (DGT), via dados.gov.pt
- **URL:** https://dados.gov.pt/datasets/carta-de-uso-e-ocupacao-do-solo-cos-serie-2-2018v3-2023v1
  (direct file: https://geo2.dgterritorio.gov.pt/cos/S2/COS2023/COS2023v1-S2-gpkg.zip)
- **Access date:** 2026-09-22
- **Spatial coverage:** continental Portugal (full national file — no
  bbox-clipping API was available, so this was not clipped to any
  pilot region; clipping to Coimbra, if wanted, is a preprocessing
  step, not yet done).
- **Temporal coverage:** reference year 2023 (Série 2, COS2023v1);
  chosen over the older COS2018v3 for temporal proximity to OrtoSat
  2023 and to recent Sentinel-2 imagery.
- **License:** CC BY 4.0.
- **Format:** vector, GeoPackage, 93 land-use/land-cover classes,
  minimum mapping unit 1 ha, nominal scale 1:25,000.
- **File:** `raw/satellite/cos/COS2023v1-S2-gpkg.zip` (857 MB, not
  yet unzipped).
- **Preprocessing:** none — original zipped GeoPackage as downloaded.

## Not Yet Obtained

- **OrtoSat 30 cm** (Pleiades-Neo, continental Portugal, 2023) —
  full-resolution download requires signed terms of use as a
  public-administration entity via SharePoint with individual
  credentials; not something this session could complete. See
  [`docs/datasets.md`](../docs/datasets.md#satellite--earth-observation-data).
- **Sentinel-1 / Sentinel-2** — requires a Copernicus Data Space
  Ecosystem (or Google Earth Engine) account and API credentials, not
  available in this session.

### Dataset: <name>

- **Source:**
- **URL:**
- **Access date:**
- **Spatial coverage:**
- **Temporal coverage:**
- **License:**
- **Preprocessing:**
