# Data

```
data/
├── raw/                  ← original, unmodified data
│   ├── citizen_science/
│   ├── expert_reference/
│   └── satellite/
├── interim/              ← data after intermediate processing
│   ├── citizen_science/
│   ├── expert_reference/
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

> All cover the Coimbra district (iNaturalist place 8422) or a larger
> area.

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
  license, observer, URI). Downloaded by section 0 of
  `notebooks/02_citizen_science/acacia_observations.ipynb`, which only
  runs if the file is missing (the code was added to the repository
  on 2026-10-28; a new download would return more observations).

### TESSERA embeddings 2023 (RQ1 pilot points)

- **Source:** GeoTessera v1.1 Zarr store, read with `geotessera`
  0.11.0 (`GeoTesseraZarr.sample_points`), without downloading tiles.
- **Access date:** 2026-10-20
- **Spatial coverage:** only the labelled pixels of the RQ1 pilot
  (iNaturalist, expert polygons and COS negatives in Coimbra district),
  ~29 000 pixels.
- **Temporal coverage:** 2023.
- **License:** MIT.
- **File:** `processed/embeddings/tessera_v1.1_2023_rq1_pilot/`, one
  `block_<x>_<y>.npz` per 10 km UTM 29N block (`px`, `py` = pixel
  centre in EPSG:32629; `emb` = 128 dequantized values, NaN where no
  embedding).
- **Preprocessing:** points snapped to the centre of their 10 m pixel
  on the TESSERA grid before reading. Made by an RQ1 pilot notebook
  removed on 2026-10-20 (experiments paused until the exploratory
  analysis is done); kept because reading them takes ~2 h.

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
- **File:** `raw/satellite/cos/COS2023v1-S2-gpkg.zip` (857 MB), read
  by the notebooks. An unzipped copy with the DGT layer style, for
  QGIS, is in `interim/spatial/COS2023v1-S2.gpkg` (1.5 GB).
- **Preprocessing:** none.
- **Possible uses:** land-cover context for error analysis, absence
  checks, independent validation.

### QGIS overview (derived)

- **File:** `interim/spatial/qgis_overview.gpkg`, to look at all the
  cleaned data together in QGIS; not read by any notebook.
- **Made by:** `notebooks/05_data_integration/qgis_overview.ipynb`.
- **Layers (EPSG:3763):** `distrito_coimbra` (iNaturalist place 8422),
  `inat_dealbata` and `inat_outras_plantas` (the cleaned files in
  `interim/citizen_science/`), `especialistas_poligonos` (the cleaned
  expert polygons, with `use`), `areas_ardidas` (ICNF 1975–2025
  burned areas that intersect the district).

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
  `notebooks/02_citizen_science/other_plants_observations.ipynb`.

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
- **Preprocessing:** none. Downloaded by `src/burned_areas.py`, first
  called from `notebooks/02_citizen_science/acacia_observations.ipynb`.

### *Acacia dealbata* expert reference polygons

Expert reference data for the RQ1 upper bound (see
`docs/research_questions.md`).

- **Source:** sent by the supervisor by email. Made from field visits
  and manual visual interpretation of OrtoSat 2023 (30 cm). The small
  (~75 m²) polygons probably come from a student's unsupervised segmentation of
  the image, each segment then labelled (supervisor, 2026-10-28).
- **Access date:** 2026-10-20
- **Files:** `raw/expert_reference/TNE_17MAY2026_5.gpkg`
  (Sentinel-2 tile TNE only, layer `tne`, 7 057 polygons) and
  `raw/expert_reference/notTNE_18MAY2026_6.gpkg` (rest of
  continental Portugal, 437 polygons).
- **Attributes:** only `classifica`. `classifica = 1` (*A. dealbata*
  present): 2 072 polygons in TNE, 398 elsewhere. `classifica = 0`
  ("not *A. dealbata*"): 5 013; 44% lie in COS 2023 artificial areas,
  3 in water, 56% in vegetation. 11 rows have no value.
- **Spatial coverage:** continental Portugal, sparse; tile TNE covers
  the Coimbra district (1 849 positive polygons in the district).
- **Temporal coverage:** 2023 (no date field; per the supervisor).
- **License:** not stated; project data shared for the thesis — do not
  redistribute. Versioned in this private repository.
- **Format:** GeoPackage, EPSG:3763.
- **Preprocessing:** none (cleaned copy below).

### iNaturalist observations, cleaned (derived)

- **Files:** `interim/citizen_science/inat_dealbata_clean.csv` (3 000
  *A. dealbata*) and `interim/citizen_science/inat_other_plants_clean.csv`
  (47 353 other plants).
- **Made by:** part 2 of
  `notebooks/02_citizen_science/acacia_observations.ipynb` and
  `notebooks/02_citizen_science/other_plants_observations.ipynb`.
- **Steps:** dropped observations without a date and with obscured
  coordinates; main observer anonymised (`observer` = "Observer A" /
  "Others", no username kept); `burned` flag (fire between the
  observation and 2023, ICNF) and `burned_same_year` (ambiguous
  cases). *Acacia* file: only *A. dealbata* kept (species and
  subspecies) (2026-10-29). Both files: only research grade
  (2026-10-29). The other-plants download already excludes the whole
  genus *Acacia*. Both files: positional accuracy above 30 m dropped;
  missing values kept and marked (`accuracy_missing`) (2026-10-29).
  Same 10 m pixel (`pixel`, EPSG:32629 grid, `src/grid.py`): one
  presence per pixel, the closest in date to 2023 (`n_obs_in_pixel`
  keeps how many there were); other plants in a presence's pixel
  dropped (2026-10-29).
- **Columns:** `id`, `observed_on`, `year`, `taxon_id`, `taxon_name`,
  `taxon_rank`, `latitude`, `longitude`, `positional_accuracy`,
  `quality_grade`, `accuracy_missing`, `observer`, `pixel`,
  `n_obs_in_pixel` (presences only), `burned`, `burned_same_year`.

### Expert reference polygons, cleaned (derived)

- **File:** `interim/expert_reference/expert_polygons_clean.gpkg`,
  layer `expert_polygons_clean`, EPSG:3763, 7 483 polygons.
- **Made by:** `notebooks/03_expert_reference/expert_polygons.ipynb`
  (part 2), 2026-10-28.
- **Steps:** dropped the 11 rows without `classifica`; repaired the
  531 invalid geometries with `make_valid`, keeping polygon parts only
  (total area unchanged); overlaps checked and left as they are
  (negligible, no label conflicts).
- **Columns:** `label` (`dealbata` / `not_dealbata`), `source` (`TNE`
  / `notTNE`), `area_m2`, `segment` (< 100 m²), `in_district`,
  `cos_code`, `cos_label`, `cos_group` (COS 2023 class at a point
  inside the polygon), `use` (proposed: `presence`,
  `absence_vegetation`, `absence_artificial`, `absence_other`).

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
