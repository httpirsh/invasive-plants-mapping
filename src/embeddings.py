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
