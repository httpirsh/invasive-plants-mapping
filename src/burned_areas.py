"""ICNF burned areas: download and the burned-between-observation-and-2023 rule.

Used by both citizen-science notebooks (Acacia and other plants).
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

# ICNF publishes grouped layers before 2009 and one layer per year from 2009.
FIRE_LAYERS = ["1975_1989", "1990_1999", "2000_2008", *map(str, range(2009, 2026))]


def load_burned_areas(folder: Path, crs: int = 3763) -> gpd.GeoDataFrame:
    """All ICNF burned areas 1975–2025, downloaded once to `folder` as GeoJSON."""
    folder.mkdir(parents=True, exist_ok=True)
    layers = []
    for layer in FIRE_LAYERS:
        f = folder / f"ardida_{layer}.geojson"
        if not f.exists():
            params = dict(service="WFS", version="2.0.0", request="GetFeature",
                          typeNames=f"BDG:ardida_{layer}", outputFormat="application/json")
            r = requests.get("https://si.icnf.pt/wfs/areas_ardidas", params=params, timeout=600)
            r.raise_for_status()
            f.write_bytes(r.content)
        layers.append(gpd.read_file(f).set_crs(crs, allow_override=True))
    fires = pd.concat(layers, ignore_index=True)
    fires["fire_date"] = pd.to_datetime(fires.get("DH_Inicio"), utc=True, errors="coerce").dt.tz_localize(None)
    return fires


def burned_between(points: gpd.GeoDataFrame, fires: gpd.GeoDataFrame, ref_year: int = 2023):
    """Flags points inside an area that burned between the observation date and `ref_year`.

    Fires with a start date are compared by date; fires with only a year by year. A fire in
    the same year as the observation without a date is counted as burned (order unknown) and
    also returned in the second series. `points` needs `id`, `date` and `year` columns.
    """
    ref_start, ref_end = pd.Timestamp(f"{ref_year}-01-01"), pd.Timestamp(f"{ref_year}-12-31")
    j = gpd.sjoin(points[["id", "date", "year", "geometry"]],
                  fires[["Ano", "fire_date", "geometry"]], predicate="within")
    dated = j["fire_date"].notna()
    lo = j["date"].where(j["date"] < ref_start, ref_start)
    hi = j["date"].where(j["date"] > ref_end, ref_end)
    by_date = dated & (j["fire_date"] >= lo) & (j["fire_date"] <= hi)
    by_year = ~dated & j["Ano"].between(j["year"].clip(upper=ref_year), j["year"].clip(lower=ref_year))
    ambiguous = ~dated & (j["Ano"] == j["year"])
    return points["id"].isin(j.loc[by_date | by_year, "id"]), points["id"].isin(j.loc[ambiguous, "id"])
