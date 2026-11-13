"""TESSERA embedding loading and spatial blocks for RQ1 (pilot points + background).

Extracted from notebooks/07_foundation_models/one_class_method_selection.ipynb
once a second notebook (presence-vs-background) needed the same pieces.
"""
from pathlib import Path

import numpy as np
import pandas as pd


def load_pilot_embeddings(pilot_dir: Path) -> tuple[pd.DataFrame, np.ndarray]:
    """Every embedding already fetched for the RQ1 pilot (citizen-science,
    expert and old COS-negative points) — see data/README.md."""
    px, py, emb = [], [], []
    for b in sorted(pilot_dir.glob("block_*.npz")):
        d = np.load(b)
        px.append(d["px"]); py.append(d["py"]); emb.append(d["emb"])
    px, py, emb = np.concatenate(px), np.concatenate(py), np.concatenate(emb)
    col = ((px - 5) / 10).round().astype(np.int64)
    row = ((py - 5) / 10).round().astype(np.int64)
    pixel = pd.Series(col).astype(str) + "_" + pd.Series(row).astype(str)
    return pd.DataFrame({"pixel": pixel, "x": px, "y": py}), emb


def block_id(x, y, block_size: int = 10_000) -> np.ndarray:
    """10 km UTM block id for each point, for spatial-block train/test splits."""
    return (
        np.floor(np.asarray(x) / block_size).astype(int).astype(str)
        + "_" + np.floor(np.asarray(y) / block_size).astype(int).astype(str)
    )


def match_to_pixel(pixel_ids: pd.Series, pilot_df: pd.DataFrame, pilot_emb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """Join a presence dataset's pixel ids to its TESSERA embedding already
    fetched into pilot_df/pilot_emb (see load_pilot_embeddings), dropping rows
    that didn't match a pilot pixel or whose embedding is NaN.

    Returns (x, y, emb, n_matched) — n_matched is before the NaN-embedding drop,
    for reporting how many presences had no pilot embedding at all.
    """
    pixel_to_idx = {p: i for i, p in enumerate(pilot_df["pixel"])}
    idx = pixel_ids.map(pixel_to_idx)
    n_matched = int(idx.notna().sum())
    idx = idx[idx.notna()].astype(int).values
    x, y, emb = pilot_df["x"].values[idx], pilot_df["y"].values[idx], pilot_emb[idx]
    valid = ~np.isnan(emb).any(axis=1)
    return x[valid], y[valid], emb[valid], n_matched


# --- Rebuilding the RQ1 pilot embeddings -------------------------------------------------
# The points of the pilot set are a fixed list (data/tessera_rq1_pilot_points.csv): the
# notebook that chose them was removed on 2026-10-20 and part of them (old negatives)
# cannot be derived again from the source files. See data/README.md.

PILOT_POINTS = Path("data") / "tessera_rq1_pilot_points.csv"


def pilot_points(root: Path) -> pd.DataFrame:
    """The point list of the pilot set: block, px, py (pixel centres, EPSG:32629)."""
    return pd.read_csv(root / PILOT_POINTS)


def fetch_pilot_embeddings(root: Path, out_dir: Path, log=print) -> None:
    """Read the TESSERA embedding of every point of the list (remote read, about 2 h) and
    write one block_<x>_<y>.npz per block into out_dir. Blocks already in out_dir are kept,
    so an interrupted run can be resumed; start from an empty folder for a full rebuild."""
    import geopandas as gpd

    from src.background import fetch_embeddings

    out_dir.mkdir(parents=True, exist_ok=True)
    for block, pts in pilot_points(root).groupby("block", sort=True):
        file = out_dir / f"block_{block}.npz"
        if file.exists():
            continue
        px, py = pts["px"].to_numpy(np.float64), pts["py"].to_numpy(np.float64)
        lonlat = gpd.GeoSeries(gpd.points_from_xy(px, py), crs=32629).to_crs(4326)
        emb = fetch_embeddings(root, lonlat.x.values, lonlat.y.values).astype(np.float32)
        np.savez(file, px=px, py=py, emb=emb)
        log(f"{file.name}: {len(px)} points")


def compare_pilot_embeddings(root: Path, pilot_dir: Path, other_dir: Path) -> pd.DataFrame:
    """Per block: whether pilot_dir holds the points of the list, and whether the arrays of
    other_dir are identical to those of pilot_dir (NaN in the same places)."""
    rows = []
    for block, pts in pilot_points(root).groupby("block", sort=True):
        a_file, b_file = pilot_dir / f"block_{block}.npz", other_dir / f"block_{block}.npz"
        row = {"block": block, "n_points": len(pts), "points_as_listed": False, "refetched": b_file.exists(),
               "same_points": False, "same_embeddings": False}
        if a_file.exists():
            a = np.load(a_file)
            row["points_as_listed"] = np.array_equal(a["px"], pts["px"]) and np.array_equal(a["py"], pts["py"])
            if b_file.exists():
                b = np.load(b_file)
                row["same_points"] = np.array_equal(a["px"], b["px"]) and np.array_equal(a["py"], b["py"])
                row["same_embeddings"] = a["emb"].shape == b["emb"].shape and np.array_equal(a["emb"], b["emb"], equal_nan=True)
        rows.append(row)
    return pd.DataFrame(rows)
