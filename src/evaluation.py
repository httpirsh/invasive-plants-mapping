"""Presence-only evaluation metrics for RQ1 (still need background, see thesis/notes.md).

Extracted from notebooks/07_foundation_models/one_class_method_selection.ipynb
once a second notebook (presence-vs-background) needed the same metric.
"""
import numpy as np
from scipy.stats import spearmanr


def continuous_boyce(p_scores: np.ndarray, bg_scores: np.ndarray, n_bins: int = 10, window_frac: float = 0.1) -> float:
    """Boyce index (Hirzel et al., 2006) over `n_bins` adjacent windows of the observed
    score range: rank correlation between each window's score and the ratio of presences
    to background found there. Not the moving window over [0, 1] of the paper; limits in
    docs/methodology.md (Evaluation)."""
    lo, hi = min(p_scores.min(), bg_scores.min()), max(p_scores.max(), bg_scores.max())
    window = window_frac * (hi - lo)
    centers = np.linspace(lo + window / 2, hi - window / 2, n_bins)
    p_ratio, bg_ratio, mids = [], [], []
    for c in centers:
        lo_w, hi_w = c - window / 2, c + window / 2
        p_in = ((p_scores >= lo_w) & (p_scores <= hi_w)).sum()
        bg_in = ((bg_scores >= lo_w) & (bg_scores <= hi_w)).sum()
        if bg_in == 0:
            continue
        p_ratio.append(p_in / len(p_scores)); bg_ratio.append(bg_in / len(bg_scores)); mids.append(c)
    f_ratio = np.array(p_ratio) / np.array(bg_ratio)
    ok = np.isfinite(f_ratio)
    if ok.sum() < 3:
        return np.nan
    rho, _ = spearmanr(np.array(mids)[ok], f_ratio[ok])
    return rho
