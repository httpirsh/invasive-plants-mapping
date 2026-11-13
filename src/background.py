"""Background pools of the presence-vs-background models: sampling, building and loading.

The pools are built only by notebooks/05_data_integration/background_pools.ipynb. Every
other notebook reads them with `load_background`, which checks the file and its inputs
against data/processed_manifest.csv first (see src/manifest.py).

The points are sampled again from the current inputs on every build. If they are the
stored ones, the stored embeddings are kept; if they differ, new TESSERA embeddings are
needed, which is a remote read and only happens with allow_fetch=True.
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from src import manifest
from src.embeddings import load_pilot_embeddings

YEAR = 2023
BUFFER_M = 50
N_BACKGROUND = 2000
TESSERA_STORE = "GeoTessera v1.1 Zarr (GeoTesseraZarr.sample_points), geotessera 0.11.0"

# kind -> file name, seed, candidates per sampling batch
POOLS = {
    "uniform": ("background_points.npz", 42, 4000),
    "forest_only": ("background_points_forest_only.npz", 0, 8000),
}
FOREST_GROUPS = {"3 eucalyptus forest", "5 pine forest", "6 other forest", "7 shrubland (matos)"}


class FetchNeeded(RuntimeError):
    """The sampled points are not the stored ones, so new embeddings would have to be read."""


def paths(root: Path) -> dict[str, Path]:
    emb = root / "data" / "processed" / "embeddings"
    return {
        "pilot": emb / "tessera_v1.1_2023_rq1_pilot",
        "pool_dir": emb / "tessera_v1.1_2023_rq1_background",
        "presences": root / "data" / "interim" / "citizen_science" / "inat_dealbata_clean.csv",
        "expert": root / "data" / "interim" / "expert_reference" / "expert_polygons_clean.gpkg",
        "cos": root / "data" / "interim" / "spatial" / "COS2023v1-S2.gpkg",
    }


def pool_file(root: Path, kind: str) -> Path:
    return paths(root)["pool_dir"] / POOLS[kind][0]


def cos_group(code):
    """Land-cover group of a COS 2023 level-4 code."""
    if pd.isna(code):
        return "9 no COS coverage"
    if code.startswith("1"):
        return "1 artificial (buildings, industry, roads)"
    if code[0] in "234":
        return "2 agriculture and pasture"
    if code == "5.1.1.6":
        return "3 eucalyptus forest"
    if code == "5.1.1.7":
        return "4 acacia forest (COS)"
    if code.startswith("5.1.2"):
        return "5 pine forest"
    if code.startswith("5"):
        return "6 other forest"
    if code.startswith("6"):
        return "7 shrubland (matos)"
    return "8 water, wetlands, bare"


def sampling_inputs(root: Path):
    """Bounding box of the pilot points and the exclusion zone around every known presence."""
    p = paths(root)
    pilot_df, _ = load_pilot_embeddings(p["pilot"])
    bbox = (pilot_df["x"].min(), pilot_df["x"].max(), pilot_df["y"].min(), pilot_df["y"].max())
    dealbata = pd.read_csv(p["presences"])
    dealbata_gdf = gpd.GeoDataFrame(
        dealbata, geometry=gpd.points_from_xy(dealbata.longitude, dealbata.latitude), crs=4326
    ).to_crs(32629)
    expert = gpd.read_file(p["expert"]).to_crs(32629)
    exclusion = pd.concat([dealbata_gdf.buffer(BUFFER_M), expert.buffer(BUFFER_M)], ignore_index=True)
    return bbox, exclusion.union_all()


def sample_uniform(bbox, exclusion_union, seed: int, batch: int, n: int = N_BACKGROUND):
    """Uniform random points in the bounding box, rejected inside the exclusion zone."""
    xmin, xmax, ymin, ymax = bbox
    rng = np.random.default_rng(seed)
    kept_x, kept_y = [], []
    while len(kept_x) < n:
        cx = rng.uniform(xmin, xmax, batch)
        cy = rng.uniform(ymin, ymax, batch)
        pts = gpd.GeoSeries(gpd.points_from_xy(cx, cy), crs=32629)
        ok = ~pts.intersects(exclusion_union).values
        kept_x.extend(cx[ok].tolist()); kept_y.extend(cy[ok].tolist())
    return np.array(kept_x[:n]), np.array(kept_y[:n])


def sample_forest_only(bbox, exclusion_union, cos_path: Path, seed: int, batch: int, n: int = N_BACKGROUND):
    """As sample_uniform, keeping only points in a COS 2023 forest or shrubland class."""
    xmin, xmax, ymin, ymax = bbox
    rng = np.random.default_rng(seed)
    kept_x, kept_y, kept_group = [], [], []
    while len(kept_x) < n:
        cx = rng.uniform(xmin, xmax, batch)
        cy = rng.uniform(ymin, ymax, batch)
        pts = gpd.GeoSeries(gpd.points_from_xy(cx, cy), crs=32629)
        ok_excl = ~pts.intersects(exclusion_union).values
        if ok_excl.sum() == 0:
            continue
        cand = gpd.GeoDataFrame({"x": cx[ok_excl], "y": cy[ok_excl]}, geometry=pts[ok_excl].values, crs=32629).to_crs(3763)

        blocks = pd.Series(list(zip(cand.geometry.x // 10_000, cand.geometry.y // 10_000)), index=cand.index)
        joined = []
        for (bx, by), d in cand.groupby(blocks):
            cos = gpd.read_file(cos_path, layer="COS2023v1", bbox=(bx * 1e4, by * 1e4, (bx + 1) * 1e4, (by + 1) * 1e4), columns=["COS23_n4_C"])
            joined.append(gpd.sjoin(d, cos, predicate="within", how="left").drop(columns="index_right"))
        cand = pd.concat(joined)
        cand = cand[~cand.index.duplicated()]
        cand["cos_group"] = cand["COS23_n4_C"].map(cos_group)

        forest = cand[cand["cos_group"].isin(FOREST_GROUPS)]
        kept_x.extend(forest["x"].tolist()); kept_y.extend(forest["y"].tolist()); kept_group.extend(forest["cos_group"].tolist())
    return np.array(kept_x[:n]), np.array(kept_y[:n]), np.array(kept_group[:n])


def fetch_embeddings(root: Path, lon, lat, year: int = YEAR) -> np.ndarray:
    """TESSERA embeddings at the points. Remote read."""
    from geotessera.store import GeoTesseraZarr

    store = GeoTesseraZarr(cache_dir=root / "data" / "raw" / "satellite" / "tessera_zarr_cache")
    coords = list(zip(lon, lat))
    chunk = 200
    return np.concatenate([store.sample_points(coords[i : i + chunk], year=year) for i in range(0, len(coords), chunk)], axis=0)


def ensure_pool(root: Path, kind: str, built_by: str, built_by_if_kept: str, allow_fetch: bool = False) -> dict:
    """Sample the pool from the current inputs, keep or rebuild the file, write its manifest row.

    `built_by_if_kept` names what built a file that is kept and has no manifest row yet.
    Returns the manifest row plus "status": "kept" or "built".
    """
    p = paths(root)
    name, seed, batch = POOLS[kind]
    file = p["pool_dir"] / name
    bbox, exclusion_union = sampling_inputs(root)
    group = None
    if kind == "uniform":
        x, y = sample_uniform(bbox, exclusion_union, seed, batch)
    else:
        x, y, group = sample_forest_only(bbox, exclusion_union, p["cos"], seed, batch)

    kept = False
    if file.exists():
        old = np.load(file, allow_pickle=True)
        # the stored file holds only points with a valid embedding, in sampling order
        kept = len(old["x"]) == len(x) and np.array_equal(old["x"], x) and np.array_equal(old["y"], y)
    if not kept:
        if not allow_fetch:
            raise FetchNeeded(
                f"{name}: the points sampled from the current inputs are not the stored ones. "
                "Rebuilding needs new TESSERA embeddings (a remote read): set ALLOW_FETCH = True to do it."
            )
        lonlat = gpd.GeoSeries(gpd.points_from_xy(x, y), crs=32629).to_crs(4326)
        emb = fetch_embeddings(root, lonlat.x.values, lonlat.y.values)
        valid = ~np.isnan(emb).any(axis=1)
        arrays = dict(x=x[valid], y=y[valid], lon=lonlat.x.values[valid], lat=lonlat.y.values[valid],
                      emb=emb[valid].astype(np.float32))
        if group is not None:
            arrays["cos_group"] = group[valid]
        file.parent.mkdir(parents=True, exist_ok=True)
        np.savez(file, **arrays)

    inputs = [manifest.input_ref(root, p["presences"]), manifest.input_ref(root, p["expert"]),
              manifest.input_ref(root, p["pilot"])]
    if kind == "forest_only":
        inputs.append(manifest.input_ref(root, p["cos"]))
    previous = manifest.read(root).get(file.relative_to(root).as_posix())
    params = {"buffer_m": BUFFER_M, "n_points": N_BACKGROUND, "year": YEAR, "batch": batch,
              "bbox_epsg32629": [float(v) for v in bbox], "tessera": TESSERA_STORE}
    if kind == "forest_only":
        params["cos_groups"] = sorted(FOREST_GROUPS)
    row = manifest.record(
        root, file,
        built_by=built_by if not kept else (previous["built_by"] if previous else built_by_if_kept),
        built_on=previous["built_on"] if kept and previous else None,
        inputs=inputs, seed=seed, params=params,
    )
    return {**row, "status": "kept" if kept else "built"}


def load_background(root: Path, kind: str = "uniform"):
    """The background pool, after checking the file and its inputs against the manifest."""
    file = pool_file(root, kind)
    manifest.verify(root, file)
    return np.load(file, allow_pickle=True)
