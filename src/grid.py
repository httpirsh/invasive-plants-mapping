"""10 m pixel ids, so observations can be matched to the pixel the model sees.

Uses a 10 m grid in UTM 29N (EPSG:32629), aligned to multiples of 10 m, the CRS of the
Sentinel-2 and TESSERA tiles over Coimbra. The exact alignment is checked when the
satellite data are added.
"""
import geopandas as gpd
import pandas as pd

PIXEL_CRS = 32629
PIXEL_SIZE = 10


def pixel_id(points: gpd.GeoDataFrame) -> pd.Series:
    """One id per 10 m pixel, as "<column>_<row>" in EPSG:32629."""
    p = points.geometry.to_crs(PIXEL_CRS)
    return (p.x // PIXEL_SIZE).astype(int).astype(str) + "_" + (p.y // PIXEL_SIZE).astype(int).astype(str)
