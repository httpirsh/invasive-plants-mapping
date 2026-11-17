"""Effort-reduction curve (RQ1): citizen-science base plus 0% to 100% of the expert polygons.

Presence-only design (2026-11-17, thesis/notes.md entry "rq1-presence-only"): the classifier
is the presence-background logistic regression chosen in
notebooks/07_foundation_models/presence_only_method_selection.ipynb (background as an
unlabelled sample of the landscape, never as absence), validated by leave-one-block-out over
the 10 km blocks, and scored by sensitivity at a fixed fraction of predicted area: for each
held-out presence, the fraction of its block's background scoring at or above it is the area
needed to include it; sensitivity at X% of area is the share of held-out presences needing at
most X%. ROC-AUC per fold against the block background is secondary. The Boyce index is not
computed: a block holds 5-41 background points, too few for its windows.

Folds: every 10 km block with at least MIN_PRESENCES presences of either source (citizen
science or expert pixels). In each fold the block's presences of both sources and its
background are the test set; everything in the other blocks trains. Expert polygons that
cross a block border contribute their test-block pixels to the test set and the rest to
training (as before). Results pooled over folds (every held-out presence counted once) and
per fold (blocks weighted equally).

Levels: expert polygons added on top of the whole citizen-science base, 0% to 100% in
10-point steps, polygons in a fixed nested order; level 100 is expert only (the reference
point) and "100% + citizen science" is the additive end of the curve (thesis/notes.md,
entry "curva-100-mais-ciencia-cidada"). Primary comparison: 90% minus 0%, pooled test
presences; expert-only and citizen-science-only test presences reported next to it.

Usage: python experiments/effort_reduction_curve/run.py [--background uniform|forest_only]
           [--buffer-m METRES] [--out-dir DIR] [--max-folds N]
Writes to results/effort_reduction_curve/ (or results/effort_reduction_curve_forest_only/):
tables and run.json with the configuration and the hashes of the inputs. The notebook
notebooks/07_foundation_models/effort_reduction_curve.ipynb only reads them.

--buffer-m (default 0): in each fold, drops from TRAINING every point (citizen-science
presence, expert pixel, background point) within that distance of any test point of the
fold; the test set is unchanged. Writes to <default folder>_buffer_<metres>m/.
--max-folds runs only the first N folds (smoke test); never use its output as a result.
"""
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT))
from src import manifest
from src.background import load_background, pool_file
from src.embeddings import block_id, load_pilot_embeddings, match_to_pixel
from src.evaluation import needed_area, sensitivity_at

# ---------------------------------------------------------------- configuration
LEVELS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # % of expert polygons; 100 = expert only
PLUS_CS = "100% + citizen science"                      # additive end of the curve
CONDITIONS = [*LEVELS, PLUS_CS]
POLYGON_ORDER_SEED = 0            # nested order in which expert polygons are added
MIN_PRESENCES = 5                 # a block is a fold if either source has at least this many presences in it
PRIMARY_AREA = 0.10               # primary number: sensitivity at 10% of predicted area (own choice)
CURVE_AREAS = np.round(np.arange(0.01, 0.51, 0.01), 2)  # pooled sensitivity-by-area curve
SUBSETS = ["pooled", "expert only", "citizen science only"]
CLASSIFIER = dict(C=10.0, class_weight="balanced", max_iter=5000)  # presence_only_method_selection.ipynb
OUT_DIRS = {"uniform": "effort_reduction_curve", "forest_only": "effort_reduction_curve_forest_only"}

_parser = argparse.ArgumentParser(description="Effort-reduction curve (RQ1), presence-only design.")
_parser.add_argument("--background", choices=sorted(OUT_DIRS), default="uniform")
_parser.add_argument("--buffer-m", type=float, default=0.0,
                     help="drop training points within this distance (m) of any test point of the fold")
_parser.add_argument("--out-dir", type=Path, default=None, help="output folder (default: under results/)")
_parser.add_argument("--max-folds", type=int, default=None, help="smoke test: run only the first N folds")
_args = _parser.parse_args()
BACKGROUND, BUFFER_M, MAX_FOLDS = _args.background, _args.buffer_m, _args.max_folds
if BUFFER_M < 0:
    _parser.error("--buffer-m must be 0 or positive")
if MAX_FOLDS is not None and _args.out_dir is None:
    _parser.error("--max-folds needs --out-dir (its output is not a result)")

PILOT_DIR = ROOT / "data" / "processed" / "embeddings" / "tessera_v1.1_2023_rq1_pilot"
CS_FILE = ROOT / "data" / "interim" / "citizen_science" / "inat_dealbata_clean.csv"
EXPERT_FILE = ROOT / "data" / "interim" / "expert_reference" / "expert_polygons_clean.gpkg"
OUT_DIR = _args.out_dir.resolve() if _args.out_dir else ROOT / "results" / (
    OUT_DIRS[BACKGROUND] + (f"_buffer_{BUFFER_M:g}m" if BUFFER_M > 0 else ""))

# ---------------------------------------------------------------- data
pilot_df, pilot_emb = load_pilot_embeddings(PILOT_DIR)
bg = load_background(ROOT, BACKGROUND)  # checked against data/processed_manifest.csv
bg_x, bg_y, bg_emb = bg["x"], bg["y"], bg["emb"]

dealbata = pd.read_csv(CS_FILE)
cs_x, cs_y, cs_emb, cs_n_matched = match_to_pixel(dealbata["pixel"], pilot_df, pilot_emb)

expert_gdf = gpd.read_file(EXPERT_FILE).to_crs(32629)
pilot_points = gpd.GeoDataFrame(pilot_df, geometry=gpd.points_from_xy(pilot_df["x"], pilot_df["y"]), crs=32629)
joined = gpd.sjoin(pilot_points, expert_gdf[["geometry"]], predicate="within", how="inner")
joined = joined[~joined.index.duplicated(keep="first")]
expert_idx = joined.index.values
valid = ~np.isnan(pilot_emb[expert_idx]).any(axis=1)
expert_x, expert_y = pilot_df["x"].values[expert_idx][valid], pilot_df["y"].values[expert_idx][valid]
expert_emb = pilot_emb[expert_idx][valid]
expert_poly_id = joined["index_right"].values[valid]

cs_block, expert_block, bg_block = block_id(cs_x, cs_y), block_id(expert_x, expert_y), block_id(bg_x, bg_y)
print(f"citizen-science presences: {len(cs_emb):,} (matched {cs_n_matched}/{len(dealbata)})")
print(f"expert presence pixels: {len(expert_emb):,}, across {len(np.unique(expert_poly_id)):,} polygons")
print(f"background points: {len(bg_emb):,}")

# ---------------------------------------------------------------- effort order and levels
poly_ids_available = np.unique(expert_poly_id)
poly_order = np.random.default_rng(POLYGON_ORDER_SEED).permutation(poly_ids_available)


def included_polygons(level_pct):
    if level_pct >= 100:
        return poly_ids_available
    return poly_order[:round(level_pct / 100 * len(poly_order))]


nominal_df = pd.DataFrame([{
    "condition": str(c), "n_polygons_included": len(included_polygons(100 if c == PLUS_CS else c)),
    "n_expert_pixels": int(np.isin(expert_poly_id, included_polygons(100 if c == PLUS_CS else c)).sum()),
    "n_cs_presences": 0 if c == 100 else len(cs_emb),
} for c in CONDITIONS])
nominal_df["total_N"] = nominal_df["n_expert_pixels"] + nominal_df["n_cs_presences"]

# ---------------------------------------------------------------- folds: leave-one-block-out
cs_counts, expert_counts = pd.Series(cs_block).value_counts(), pd.Series(expert_block).value_counts()
folds = sorted(set(cs_counts[cs_counts >= MIN_PRESENCES].index) | set(expert_counts[expert_counts >= MIN_PRESENCES].index))
print(f"{len(folds)} folds (blocks with >= {MIN_PRESENCES} presences of either source)")
if MAX_FOLDS is not None:
    folds = folds[:MAX_FOLDS]
    print(f"SMOKE TEST: first {len(folds)} folds only")

# ---------------------------------------------------------------- run
per_fold_rows, test_size_rows, buffer_removed = [], [], {}
needed = {(c, s): [] for c in CONDITIONS for s in SUBSETS}  # per-presence needed area, pooled over folds
for fold in folds:
    cs_te, ex_te, bg_te = cs_block == fold, expert_block == fold, bg_block == fold
    cs_tr, ex_tr, bg_tr = ~cs_te, ~ex_te, ~bg_te

    coords = {"citizen_science": (cs_x, cs_y, cs_te, cs_tr), "expert": (expert_x, expert_y, ex_te, ex_tr),
              "background": (bg_x, bg_y, bg_te, bg_tr)}
    buffer_removed[fold] = {}
    if BUFFER_M > 0:
        test_tree = cKDTree(np.vstack([np.column_stack([x[t], y[t]]) for x, y, t, _ in coords.values()]))
    for source, (x, y, _, train_mask) in coords.items():
        n_before = int(train_mask.sum())
        if BUFFER_M > 0:
            dist, _ = test_tree.query(np.column_stack([x[train_mask], y[train_mask]]))
            train_mask[np.flatnonzero(train_mask)[dist <= BUFFER_M]] = False  # in place
        buffer_removed[fold][source] = {"n_train_before": n_before, "n_removed": n_before - int(train_mask.sum())}

    cs_train, cs_test = cs_emb[cs_tr], cs_emb[cs_te]
    ex_train, ex_test, ex_train_poly = expert_emb[ex_tr], expert_emb[ex_te], expert_poly_id[ex_tr]
    bg_train, bg_test = bg_emb[bg_tr], bg_emb[bg_te]
    test_size_rows.append({
        "fold": fold, "n_test_cs": len(cs_test), "n_test_expert_pixels": len(ex_test),
        "n_test_expert_polygons": len(np.unique(expert_poly_id[ex_te])), "n_test_background": len(bg_test),
    })
    if len(bg_test) == 0:
        print(f"fold {fold}: no background in the block, skipped"); continue

    for cond in CONDITIONS:
        if cond == 100:
            train_pres = ex_train
        elif cond == PLUS_CS:
            train_pres = np.concatenate([cs_train, ex_train])
        else:
            train_pres = np.concatenate([cs_train, ex_train[np.isin(ex_train_poly, included_polygons(cond))]])
        X = np.concatenate([train_pres, bg_train])
        y = np.concatenate([np.ones(len(train_pres)), np.zeros(len(bg_train))])
        scaler = StandardScaler().fit(X)
        model = LogisticRegression(**CLASSIFIER).fit(scaler.transform(X), y)
        s_cs = model.decision_function(scaler.transform(cs_test)) if len(cs_test) else np.empty(0)
        s_ex = model.decision_function(scaler.transform(ex_test)) if len(ex_test) else np.empty(0)
        s_bg = model.decision_function(scaler.transform(bg_test))
        for subset, s_pres in {"pooled": np.concatenate([s_cs, s_ex]), "expert only": s_ex,
                               "citizen science only": s_cs}.items():
            if len(s_pres) == 0:
                continue
            na = needed_area(s_pres, s_bg)
            needed[(cond, subset)].append(na)
            per_fold_rows.append({
                "fold": fold, "condition": str(cond), "test_presences": subset,
                "n_train_presences": len(train_pres), "n_test_presences": len(s_pres), "n_test_background": len(s_bg),
                f"sensitivity_at_{int(PRIMARY_AREA*100)}pct": sensitivity_at(na, PRIMARY_AREA),
                "roc_auc": roc_auc_score(np.r_[np.ones(len(s_pres)), np.zeros(len(s_bg))], np.r_[s_pres, s_bg]),
            })
    print(f"fold {fold} done")

SENS = f"sensitivity_at_{int(PRIMARY_AREA*100)}pct"
per_fold_df = pd.DataFrame(per_fold_rows)
pooled = {k: np.concatenate(v) for k, v in needed.items() if v}

curve_df = pd.DataFrame([{"condition": str(c), "test_presences": s, "area_fraction": a,
                          "sensitivity": sensitivity_at(pooled[(c, s)], a)}
                         for (c, s) in pooled for a in CURVE_AREAS])
summary_df = pd.DataFrame([{
    "condition": str(c), "test_presences": s, "n_test_presences": len(pooled[(c, s)]),
    f"pooled_{SENS}": sensitivity_at(pooled[(c, s)], PRIMARY_AREA),
    f"per_fold_{SENS}_mean": g[SENS].mean(), f"per_fold_{SENS}_sd": g[SENS].std(),
    "per_fold_roc_auc_mean": g["roc_auc"].mean(), "per_fold_roc_auc_sd": g["roc_auc"].std(), "n_folds": len(g),
} for (c, s) in pooled for g in [per_fold_df[(per_fold_df["condition"] == str(c)) & (per_fold_df["test_presences"] == s)]]])

# paired differences per fold (same test block), plus the pooled difference
wide = per_fold_df.pivot_table(index=["test_presences", "fold"], columns="condition", values=SENS)
pooled_sens = summary_df.set_index(["condition", "test_presences"])[f"pooled_{SENS}"]
COMPARISONS = [(str(l), "0") for l in LEVELS[1:]] + [(PLUS_CS, "0"), (PLUS_CS, "90"), (PLUS_CS, "100")]
paired_df = pd.DataFrame([{
    "test_presences": s, "comparison": f"{a} minus {b}",
    "pooled_diff": pooled_sens[(a, s)] - pooled_sens[(b, s)],
    "per_fold_diff_mean": d.mean(), "per_fold_diff_sd": d.std(),
    "folds_up": int((d > 0).sum()), "folds_down": int((d < 0).sum()), "folds_tied": int((d == 0).sum()),
} for s in SUBSETS if s in wide.index.get_level_values(0) for a, b in COMPARISONS
  for d in [(wide.loc[s][a] - wide.loc[s][b]).dropna()]])

# ---------------------------------------------------------------- save
OUT_DIR.mkdir(parents=True, exist_ok=True)
per_fold_df.to_csv(OUT_DIR / "per_fold.csv", index=False)
summary_df.to_csv(OUT_DIR / "summary.csv", index=False)
curve_df.to_csv(OUT_DIR / "pooled_curve.csv", index=False)
paired_df.to_csv(OUT_DIR / "paired_differences.csv", index=False)
pd.DataFrame(test_size_rows).to_csv(OUT_DIR / "test_sizes.csv", index=False)
nominal_df.to_csv(OUT_DIR / "nominal_levels.csv", index=False)


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


BG_FILE = pool_file(ROOT, BACKGROUND)
(OUT_DIR / "run.json").write_text(json.dumps({
    "run_date": date.today().isoformat(),
    "script": "experiments/effort_reduction_curve/run.py",
    "command": f"python experiments/effort_reduction_curve/run.py --background {BACKGROUND}"
               + (f" --buffer-m {BUFFER_M:g}" if BUFFER_M > 0 else "") + (f" --max-folds {MAX_FOLDS}" if MAX_FOLDS else ""),
    "smoke_test": MAX_FOLDS is not None,
    "git_commit": _git("rev-parse", "HEAD"),
    "git_uncommitted_changes": bool(_git("status", "--porcelain")),
    "design": "leave-one-block-out; sensitivity at fixed predicted area; background as landscape sample only",
    "classifier": {"LogisticRegression": CLASSIFIER, "scaling": "StandardScaler on training presences + background"},
    "primary_area_fraction": PRIMARY_AREA, "curve_area_fractions": CURVE_AREAS.tolist(),
    "conditions": [str(c) for c in CONDITIONS], "polygon_order_seed": POLYGON_ORDER_SEED,
    "min_presences_per_fold": MIN_PRESENCES, "folds": folds, "n_folds": len(folds),
    "background": BACKGROUND, "buffer_m": BUFFER_M, "buffer_removed_from_training_by_fold": buffer_removed,
    "embeddings": PILOT_DIR.name,
    "n_cs_presences": len(cs_emb), "n_cs_matched": cs_n_matched, "n_cs_rows": len(dealbata),
    "n_expert_pixels": len(expert_emb), "n_expert_polygons": len(poly_ids_available),
    "n_expert_polygons_crossing_blocks": int((pd.Series(expert_block).groupby(expert_poly_id).nunique() > 1).sum()),
    "n_background": len(bg_emb),
    "inputs_sha256": {
        CS_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(CS_FILE),
        EXPERT_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(EXPERT_FILE),
        PILOT_DIR.relative_to(ROOT).as_posix() + "/": manifest.sha256_dir(PILOT_DIR),
        BG_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(BG_FILE),
    },
}, indent=1))
print(f"saved to {OUT_DIR}")
