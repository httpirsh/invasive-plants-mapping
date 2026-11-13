"""Counts quoted in the design docs, and the RQ2 150-presence draw, for both presence files.

Writes results/temporal_window_2021_2025/design_counts.csv (one column per file) and
<variant dir>/rq2_sample_150_seed0.csv. Run from anywhere: python design_counts.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from shapely.geometry import shape

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT))
from src.embeddings import block_id, load_pilot_embeddings, match_to_pixel

CS = ROOT / "data" / "interim" / "citizen_science"
OUT = ROOT / "results" / "temporal_window_2021_2025"
FILES = {"old_all_years": CS / "inat_dealbata_clean.csv", "new_2021_2025": CS / "inat_dealbata_clean_2021_2025.csv"}
RQ2_N, RQ2_SEED = 150, 0

place = requests.get("https://api.inaturalist.org/v1/places/8422", timeout=60).json()["results"][0]
district = gpd.GeoSeries([shape(place["geometry_geojson"])], crs=4326).to_crs(3763).iloc[0]

EXPERT = ROOT / "data" / "raw" / "expert_reference"
raw = gpd.GeoDataFrame(pd.concat([gpd.read_file(EXPERT / f).assign(file=k) for k, f in
                                  {"TNE": "TNE_17MAY2026_5.gpkg", "notTNE": "notTNE_18MAY2026_6.gpkg"}.items()],
                                 ignore_index=True), crs=3763)
pos = raw[pd.to_numeric(raw["classifica"], errors="coerce") == 1].copy()
pos["geometry"] = pos.geometry.make_valid()
pos["in_district"] = pos.intersects(district)
pos_d = pos[pos.in_district]

pilot_df, pilot_emb = load_pilot_embeddings(ROOT / "data" / "processed" / "embeddings" / "tessera_v1.1_2023_rq1_pilot")

cols = {}
for variant, f in FILES.items():
    d = pd.read_csv(f)
    g = gpd.GeoDataFrame(d, geometry=gpd.points_from_xy(d.longitude, d.latitude), crs=4326).to_crs(3763)
    a = g.observer == "Observer A"
    blk = pd.Series(list(zip(g.geometry.x // 10_000, g.geometry.y // 10_000)), index=g.index)
    r = {
        "presences": len(d), "first year": int(d.year.min()), "last year": int(d.year.max()),
        "Observer A": int(a.sum()), "Observer A %": round(100 * a.mean(), 1), "other observers": int((~a).sum()),
        "within 2 years of 2023 %": round(100 * ((d.year - 2023).abs() <= 2).mean(), 1),
        "within 4 years of 2023 %": round(100 * ((d.year - 2023).abs() <= 4).mean(), 1),
        "burned flag": int(d.burned.sum()),
        "10 km blocks (EPSG:3763), all": blk.nunique(), "10 km blocks, Observer A": blk[a].nunique(),
        "10 km blocks, other observers": blk[~a].nunique(),
        "other observers outside Observer A's blocks": int((~a & ~blk.isin(set(blk[a]))).sum()),
    }
    x, y, emb, n_matched = match_to_pixel(d["pixel"], pilot_df, pilot_emb)
    r["with a valid TESSERA embedding"] = len(emb)
    r["10 km blocks (UTM, with embedding)"] = len(set(block_id(x, y)))

    gd = g[g.within(district)]
    for buf in (0, 50):
        near = gpd.sjoin(gd[["id", "observer", "geometry"]], gpd.GeoDataFrame(geometry=pos_d.buffer(buf), crs=3763),
                         predicate="within").drop_duplicates("id")
        k = "inside an expert polygon" if buf == 0 else "within 50 m of an expert polygon"
        r[k] = len(near)
        r[k + ", Observer A %"] = round(100 * (near.observer == "Observer A").mean(), 1)

    # expert polygons by distance to the nearest citizen-science point
    # (centroid of the polygon to the nearest point: the definition that reproduces the documented counts)
    dist = gpd.sjoin_nearest(pos[["file", "in_district"]].set_geometry(pos.geometry.centroid), g[["geometry"]], distance_col="dist")
    dist = dist[~dist.index.duplicated()]
    band = pd.cut(dist["dist"], [-1, 1000, 5000, 20000, np.inf], labels=["0-1 km", "1-5 km", "5-20 km", ">20 km"])
    grp = np.where(dist.file == "notTNE", "notTNE", np.where(dist.in_district, "TNE in district", "TNE outside district"))
    tab = pd.crosstab(grp, band)
    for gname, row in tab.iterrows():
        r[f"expert polygons, {gname} (0-1/1-5/5-20/>20 km)"] = " / ".join(str(v) for v in row.values)
    tne = dist.file == "TNE"
    r["expert polygons near (<= 1 km, TNE)"] = int((tne & (dist["dist"] <= 1000)).sum())
    r["expert polygons far (> 1 km, TNE)"] = int((tne & (dist["dist"] > 1000)).sum())
    r["expert polygons, notTNE"] = int((~tne).sum())

    # RQ2: random draw of 150 presences
    s = d.sample(RQ2_N, random_state=RQ2_SEED)
    s[["id", "pixel", "year", "observer", "latitude", "longitude"]].to_csv(OUT / variant / f"rq2_sample_{RQ2_N}_seed{RQ2_SEED}.csv", index=False)
    _, _, s_emb, _ = match_to_pixel(s["pixel"], pilot_df, pilot_emb)
    r[f"RQ2 draw of {RQ2_N} (seed {RQ2_SEED}): Observer A %"] = round(100 * (s.observer == "Observer A").mean(), 1)
    r[f"RQ2 draw of {RQ2_N}: with a valid embedding"] = len(s_emb)
    r[f"RQ2 draw of {RQ2_N}: share of the file %"] = round(100 * RQ2_N / len(d), 1)
    r[f"RQ2 draw of {RQ2_N}: year range"] = f"{int(s.year.min())}-{int(s.year.max())}"
    cols[variant] = r
    cols.setdefault("_samples", {})[variant] = set(s.id)

samples = cols.pop("_samples")
table = pd.DataFrame(cols)
table.loc[f"RQ2 draw of {RQ2_N}: ids shared by the two draws"] = len(samples["old_all_years"] & samples["new_2021_2025"])
table.to_csv(OUT / "design_counts.csv")
print(table.to_string())
