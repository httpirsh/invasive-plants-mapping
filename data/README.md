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

### TESSERA embeddings — RQ1 background pool (2026-11-06)

- **Source:** same store as above (`GeoTesseraZarr.sample_points`).
- **Access date:** 2026-11-06.
- **Spatial coverage:** 2 000 points sampled uniformly at random within
  the bounding box of the RQ1 pilot points above (507 905–607 985 mE,
  4 419 545–4 485 285 mN, EPSG:32629), excluding a 50 m buffer around
  every citizen-science and expert-polygon *A. dealbata* presence.
- **Temporal coverage:** 2023.
- **License:** MIT.
- **File:** `processed/embeddings/tessera_v1.1_2023_rq1_background/background_points.npz`
  (`x`, `y` = point coordinates in EPSG:32629; `lon`, `lat` = WGS84;
  `emb` = 128 dequantized values; all 2 000 valid, no NaN rows).
- **Preprocessing:** candidate points rejected if inside the 50 m
  buffer (own choice, no literature value found for the exact radius —
  see
  [`thesis/notes.md`](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)).
  Not COS-stratified (ruled out 2026-11-06, supervisor). Made by
  [`notebooks/07_foundation_models/one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb),
  regenerated only if this file is missing.
- **Status:** first version of the background pool meant to be shared
  across the whole RQ1 effort-reduction curve; not yet confirmed by
  the supervisor as final.

### TESSERA embeddings — patch access (2026-11-03)

- **Source:** same store as above, dataset variant `dclimate` (the
  default for v1.1), but read with `GeoTesseraZarr.read_patch`
  instead of `sample_points`: a small square patch around a point,
  not just its one pixel — needed for the segmentation-mask region
  growing (see
  [`notebooks/04_satellite/tessera_embeddings.ipynb`](../notebooks/04_satellite/tessera_embeddings.ipynb)).
  Reads directly over HTTPS from
  `https://data.source.coop/tessera/tessera/zarr/v1.1-dclimate`, no
  bulk download; a local byte-range cache is kept in
  `raw/satellite/tessera_zarr_cache` (not committed).
- **Note:** `GeoTessera` (the high-level class used by
  `fetch_embedding`/`fetch_mosaic_for_region`) only serves the
  `cambridge` NPY dataset, which has no coverage over Portugal — use
  `GeoTesseraZarr` instead for this project.

### TESSERA GeoTIFF tile, 2023 (grid template)

- **Source:** same Zarr store (`v1.1-dclimate`), exported to GeoTIFF
  with the `geotessera` CLI (`geotessera download --bbox
  "-8.46,40.21,-8.44,40.29" --year 2023`), which for `--format tiff`
  reads from the same Zarr/`GeoTesseraZarr` path as above (confirmed
  with `--dry-run`), not the `cambridge`-only path.
- **Access date:** 2026-11-03.
- **Spatial coverage:** one narrow strip, 1.75 × 8.89 km (889 × 175
  px at 10 m, EPSG:32629) — whatever the bbox above resolves to in
  the Zarr store's tiling, not the full pilot extent above.
- **Temporal coverage:** 2023.
- **File:** `raw/satellite/tessera_tiles/coimbra_2023_geotiff/tessera_2023_utm29.tif`
  (128 bands, float32).
- **Use:** read only for its grid (`rioxarray` + `tess.odc.geobox`),
  to resample Sentinel-2 onto the same pixels (see next entry) — not
  used itself as embeddings here.

### Sentinel-2 L2A, TESSERA grid, 2023

- **Source:** AWS Earth Search STAC catalog
  (`https://earth-search.aws.element84.com/v1`, `sentinel-2-l2a`
  collection; Element84's COG mirror of the Copernicus L2A archive),
  no account needed.
- **Access date:** 2026-11-03.
- **Spatial coverage:** MGRS tile `29TNE`, read only for the geobox of
  the TESSERA tile above (1.75 × 8.89 km) via windowed/range reads
  (`odc.stac.load(..., geobox=...)`) — no full-tile download.
- **Temporal coverage:** 2023-01-01 to 2023-12-31, `eo:cloud_cover <
  20%` → 61 scenes.
- **Bands:** blue, green, red, nir, rededge1–3, nir08 (B8A), swir16,
  swir22, scl. Coastal aerosol (B01), water vapour (B09), AOT, WVP,
  visual (TCI) and thumbnail assets not downloaded.
- **License:** Copernicus Sentinel data, free and open (EU Copernicus
  licence).
- **Files:** `raw/satellite/sentinel2/tessera_grid_2023/<scene_id>/<band>.tif`
  (one GeoTIFF per band per scene), plus `manifest.csv` (scene id,
  datetime, cloud cover) in the same folder.
- **Preprocessing:** every band resampled onto the TESSERA tile's 10 m
  grid (bilinear for reflectance, nearest for `scl`) — so, unlike the
  rest of this project's `raw/` data, this is not byte-for-byte
  original; done so Sentinel-2 and TESSERA embeddings are pixel-
  aligned. No mosaicking, no cloud masking.
- **Scope note:** this covers only the narrow test strip of the
  TESSERA tile above, not the full Coimbra pilot extent (the
  iNaturalist/expert-polygon area in the entries above) — a quick
  pipeline check; widen the TESSERA tile/area once this is confirmed
  to work for the actual modelling extent.
- **No precedent found in the literature read so far for this exact
  access route** (Earth Search STAC with windowed/geobox-aligned
  reads); Sentinel-2 itself as the baseline sensor is grounded in
  Mouta et al. (2021) and Domingo et al. (2023) (see
  `docs/methodology.md`).
- **Made by:** `notebooks/04_satellite/sentinel2_download.ipynb`.

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

- **File:** `interim/spatial/qgis/qgis_overview.gpkg`, to look at all
  the cleaned data together in QGIS; not read by any notebook.
  `interim/spatial/qgis/` holds every GeoPackage made only for visual
  inspection in QGIS (not read back by code) — see also the
  segmentation-mask sample below.
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
  and `..._obscured_ids.csv` per range. Also
  `raw/citizen_science/inaturalist_taxa_ancestry.csv`: the iNaturalist
  ancestors (`ancestor_ids`) of each taxon in the cleaned file, from
  `api.inaturalist.org/v1/taxa`, accessed 2026-10-30; used to drop
  non-vascular plants.
- **Preprocessing:** none — one row per observation, same columns as
  the *Acacia* pilot. Downloaded by
  `notebooks/02_citizen_science/other_plants_observations.ipynb`.

### GIFT plant traits (growth form, climber, height, aquatic)

- **Source:** GIFT, Global Inventory of Floras and Traits, version 3.2
  (2024-06-13), API `https://gift.uni-goettingen.de/api/extended/index3.2.php`
- **Access date:** 2026-10-30
- **References:** Weigelt, König & Kreft (2020), *J. Biogeography* 47,
  16–43; Denelle, Weigelt & Kreft (2023), *Methods Ecol. Evol.* 14,
  2738–2748. The GIFT site asks to cite the version used and the 2020
  paper.
- **License:** see GIFT terms; some contributors restrict access.
- **Files:** `external/auxiliary/gift/gift_species.csv` (372 098
  species: `work_ID`, `work_species`) and `gift_trait_<id>.csv` for
  traits 1.2.1 (growth form: herb, shrub, tree, other), 1.4.1
  (climber), 1.6.2 (maximum height, m), 1.7.1 (aquatic); columns
  `work_ID`, `trait_value`, `agreement`.
- **Preprocessing:** none. Downloaded and used in step 11 of
  `notebooks/02_citizen_science/other_plants_observations.ipynb`.

### National list of invasive species (Decreto-Lei 92/2019, Annex II)

- **Source:** ICNF, "Lista Nacional de Espécies Invasoras" (Annex II
  of Decreto-Lei n.º 92/2019, 10 July), PDF
  https://www.icnf.pt/api/file/doc/cf455e5a84ab1d96
- **Access date:** 2026-10-30
- **File:** `external/auxiliary/icnf_invasive_list/lista_nacional_especies_invasoras_anexo_II_DL92_2019.pdf`
- **Notes:** species marked "\*" are invasive only in Madeira and are
  not used. 113 plant names for the mainland are read from the
  "Plantas" section in step 11 of
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
  (13 554 other plants).
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
  dropped (2026-10-29). Other-plants file (2026-10-30, to confirm
  with the supervisor): non-vascular plants dropped; species grouped
  into 8 classes (`group`) from GIFT growth forms, the national
  invasive list and the iNaturalist taxonomy; COS 2023 class added
  (`cos2023`, level-4 code); herbaceous plants kept only in COS
  classes where herbs are the top layer; one observation per pixel,
  the tallest group first, then the closest in date to 2023.
- **Columns:** `id`, `observed_on`, `year`, `taxon_id`, `taxon_name`,
  `taxon_rank`, `latitude`, `longitude`, `positional_accuracy`,
  `quality_grade`, `accuracy_missing`, `observer`, `pixel`,
  `n_obs_in_pixel` (presences only), `group` and `cos2023` (other
  plants only), `burned`, `burned_same_year`.

### Expert reference polygons, cleaned (derived)

- **File:** `interim/expert_reference/expert_polygons_clean.gpkg`,
  layer `expert_polygons_clean`, EPSG:3763, 2 470 polygons (all
  `classifica = 1`, *A. dealbata* presences).
- **Made by:** `notebooks/03_expert_reference/expert_polygons.ipynb`
  (part 2), 2026-10-28; updated 2026-11-06 to drop `classifica = 0`
  rows entirely, per the supervisor's decision
  ([`thesis/notes.md`](../thesis/notes.md#usar-os-dados-de-especialistas-com-limpeza)).
- **Steps:** dropped the 11 rows without `classifica` and all 5 013
  `classifica = 0` rows (2026-11-04 decision: they are not reliable
  absences, 44% sit in artificial areas); repaired the 49 invalid
  geometries among the remaining positives with `make_valid`, keeping
  polygon parts only (total area unchanged); overlaps checked and left
  as they are (negligible, 1 pair sharing 1.6 m²).
- **Columns:** `source` (`TNE` / `notTNE`), `area_m2`, `segment`
  (< 100 m²), `in_district`, `cos_code`, `cos_label`, `cos_group` (COS
  2023 class at a point inside the polygon — informational only, not
  used to assign a label). No `label`/`use` columns: every row is a
  presence, so they would be constant.

## Not Yet Obtained

| Source | Use | Status |
|---|---|---|
| **Sentinel-2**, full pilot extent | Conventional baseline (RQ1–RQ3); precedent: Mouta et al. (2021) | Pilot obtained via AWS Earth Search STAC, no account needed, for a small test strip only (see "Sentinel-2 L2A, TESSERA grid, 2023" above) — extend to the full Coimbra pilot extent |
| **Sentinel-1** | Possible second conventional sensor (RQ1–RQ3) | Not obtained |
| **OrtoSat 30 cm** (Pleiades-Neo, RGB+NIR, continental Portugal, Apr–Oct 2023, CC BY 4.0) | Possible validation reference | Full resolution restricted to public-administration entities; only WMS confirmed public. University access unconfirmed |
| **AlphaEarth embeddings** | Second foundation model (RQ1) | Access terms unconfirmed |
| **Roads/trails, accessibility** (e.g. OpenStreetMap) | RQ3 bias covariates | Not downloaded |
| **CAOP administrative boundaries** | Study-area clipping | Not downloaded (bounding boxes used) |
| **A second, distinct region** | RQ3 geographic comparison | Candidate found (2026-11-04), not chosen — see below |

Scope (proposed, not decided): start with Coimbra as a pilot, extend
to continental Portugal once the pipeline works. GBIF (which
aggregates iNaturalist and other sources) is an alternative to the
iNaturalist API.

### Candidate second region for RQ3 (found, not chosen)

Checked 2026-11-04, while the segmentation-mask work took priority in
`docs/todo.md`: the 398 `classifica = 1` expert polygons outside tile
TNE (`raw/expert_reference/notTNE_18MAY2026_6.gpkg`) are not spread
evenly — DBSCAN (5 km radius, min. 5 polygons) on their centroids
finds three clusters of 165 polygons total within ~15 km of each
other, reverse-geocoded (Nominatim/OSM) to the Covilhã–Fundão area,
Castelo Branco district (MGRS tile **29TPE**, adjacent to Coimbra's
29TNE — confirmed via an Earth Search STAC point query). A quick
iNaturalist bounding-box count (39.95–40.40°N, -7.60–-7.30°E, not yet
cleaned the way the Coimbra pilot was) found **57 research-grade
*A. dealbata* observations** there (Coimbra pilot has 3 000 after
cleaning, so this is a much smaller pool) and >10 000 other-plant
observations.

This is a real, data-backed candidate — expert ground truth and some
citizen-science presence both exist, in a different MGRS tile — but it
is not a decision: the citizen-science pool is small, nothing has been
cleaned or downloaded there the way the Coimbra data was, and RQ3's
design ("train with all/capped/without the dominant observer, test on
other observers' records and regions") assumed a test region with its
own citizen-science records to hold out, which 57 observations may or
may not support. Picking the actual second region is the supervisor's
call (he supplied the expert data and knows this area), so this is
raised as a question in
[`docs/meetings/proxima-reuniao.md`](../docs/meetings/proxima-reuniao.md)
rather than decided here.

## Template

### Dataset: <name>

- **Source:**
- **URL:**
- **Access date:**
- **Spatial coverage:**
- **Temporal coverage:**
- **License:**
- **Preprocessing:**
