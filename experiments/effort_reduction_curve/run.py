"""Effort-reduction curve (RQ1): citizen-science base plus 0% to 100% of the expert polygons.

Trains presence-vs-background models on TESSERA embeddings at every level, with one fixed
spatial test set per seed, and scores each model on the pooled test presences and on each
source separately. Design and reading of the result:
notebooks/07_foundation_models/effort_reduction_curve.ipynb, which only reads the tables
written here.

A One-Class SVM is trained on the same presences at every level and scored on the pooled
test presences only (one_class_per_seed.csv); it is used by the forest-only background check.

Usage: python experiments/effort_reduction_curve/run.py [--background uniform|forest_only]
           [--buffer-m METRES] [--out-dir DIR]
Writes to results/effort_reduction_curve/ (uniform background, the curve of RQ1) or to
results/effort_reduction_curve_forest_only/ (forest-only background, the robustness check
read by notebooks/07_foundation_models/forest_only_background_check.ipynb): tables and
run.json with the configuration and the hashes of the inputs.

--buffer-m (default 0, no buffer): in each seed, drops from TRAINING every point
(citizen-science presence, expert pixel, background point) within that distance of any test
point of that seed. Test points are all points inside the test blocks, of the three sources
and at every level, as in section 5 of notebooks/05_data_integration/design_counts.ipynb.
The test set is unchanged, so runs with and without buffer are scored on the same points.
A positive buffer writes to its own folder, <default folder>_buffer_<metres>m/.
--out-dir overrides the output folder (used to check a run against an existing one).
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.spatial import cKDTree
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT))
from src import manifest
from src.background import load_background, pool_file
from src.embeddings import block_id, load_pilot_embeddings, match_to_pixel
from src.evaluation import continuous_boyce

# ---------------------------------------------------------------- configuration
LEVELS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # % of expert polygons; 100 = expert only
SEEDS = [1, 2, 3, 4, 5]          # one draw of test blocks per seed
POLYGON_ORDER_SEED = 0           # nested order in which expert polygons are added
TEST_FRACTION = 0.2              # share of candidate 10 km blocks held out per seed
OUT_DIRS = {"uniform": "effort_reduction_curve", "forest_only": "effort_reduction_curve_forest_only"}
_parser = argparse.ArgumentParser(description="Effort-reduction curve (RQ1).")
_parser.add_argument("--background", choices=sorted(OUT_DIRS), default="uniform")
_parser.add_argument("--buffer-m", type=float, default=0.0,
                     help="drop training points within this distance (m) of any test point of the seed")
_parser.add_argument("--out-dir", type=Path, default=None, help="output folder (default: under results/)")
_args = _parser.parse_args()
BACKGROUND = _args.background  # background pool, see src/background.py
BUFFER_M = _args.buffer_m      # 0 = no buffer between training and test
if BUFFER_M < 0:
    _parser.error("--buffer-m must be 0 or positive")
CLASSIFIERS = {
    "RandomForest": dict(n_estimators=300, class_weight="balanced", random_state=42),
    "LogisticRegression": dict(class_weight="balanced", max_iter=1000),
}
MAKERS = {"RandomForest": RandomForestClassifier, "LogisticRegression": LogisticRegression}
ONE_CLASS = dict(kernel="rbf", nu=0.05, gamma="scale")  # One-Class SVM, presences only

PILOT_DIR = ROOT / "data" / "processed" / "embeddings" / "tessera_v1.1_2023_rq1_pilot"
CS_FILE = ROOT / "data" / "interim" / "citizen_science" / "inat_dealbata_clean.csv"
EXPERT_FILE = ROOT / "data" / "interim" / "expert_reference" / "expert_polygons_clean.gpkg"
OUT_DIR = _args.out_dir.resolve() if _args.out_dir else ROOT / "results" / (
    OUT_DIRS[BACKGROUND] + (f"_buffer_{BUFFER_M:g}m" if BUFFER_M > 0 else ""))

# ---------------------------------------------------------------- data
pilot_df, pilot_emb = load_pilot_embeddings(PILOT_DIR)
bg = load_background(ROOT, BACKGROUND)  # checked against data/processed_manifest.csv
bg_x, bg_y, bg_emb = bg["x"], bg["y"], bg["emb"]

# citizen-science presences
dealbata = pd.read_csv(CS_FILE)
cs_x, cs_y, cs_emb, cs_n_matched = match_to_pixel(dealbata["pixel"], pilot_df, pilot_emb)

# expert presences, pixel -> polygon id
expert_gdf = gpd.read_file(EXPERT_FILE).to_crs(32629)
pilot_points = gpd.GeoDataFrame(pilot_df, geometry=gpd.points_from_xy(pilot_df["x"], pilot_df["y"]), crs=32629)
joined = gpd.sjoin(pilot_points, expert_gdf[["geometry"]], predicate="within", how="inner")
joined = joined[~joined.index.duplicated(keep="first")]
expert_idx = joined.index.values
expert_poly_id_all = joined["index_right"].values
expert_emb_all = pilot_emb[expert_idx]
valid = ~np.isnan(expert_emb_all).any(axis=1)
expert_x, expert_y = pilot_df["x"].values[expert_idx][valid], pilot_df["y"].values[expert_idx][valid]
expert_emb = expert_emb_all[valid]
expert_poly_id = expert_poly_id_all[valid]

cs_block = block_id(cs_x, cs_y)
expert_block = block_id(expert_x, expert_y)
bg_block = block_id(bg_x, bg_y)

print(f"citizen-science presences: {len(cs_emb):,} (matched {cs_n_matched}/{len(dealbata)})")
print(f"expert presence pixels: {len(expert_emb):,}, across {len(np.unique(expert_poly_id)):,} polygons")
print(f"background points: {len(bg_emb):,}")

# ---------------------------------------------------------------- effort order and levels
poly_ids_available = np.unique(expert_poly_id)
poly_order = np.random.default_rng(POLYGON_ORDER_SEED).permutation(poly_ids_available)


def included_polygons(level_pct):
    if level_pct >= 100:
        return poly_ids_available
    n_incl = round(level_pct / 100 * len(poly_order))
    return poly_order[:n_incl]


nominal_rows = []
for lvl in LEVELS:
    incl = included_polygons(lvl)
    n_expert_px = len(expert_poly_id) if lvl >= 100 else int(np.isin(expert_poly_id, incl).sum())
    n_cs = 0 if lvl >= 100 else len(cs_emb)
    nominal_rows.append({
        "level_pct": lvl, "n_polygons_included": len(incl),
        "n_expert_pixels": n_expert_px, "n_cs_presences": n_cs, "total_N": n_cs + n_expert_px,
    })
nominal_df = pd.DataFrame(nominal_rows)

# ---------------------------------------------------------------- fixed test blocks per seed
candidate_blocks = sorted(set(cs_block) | set(expert_block))
test_blocks_by_seed = {}
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    test_blocks_by_seed[seed] = set(
        rng.choice(candidate_blocks, size=max(1, round(TEST_FRACTION * len(candidate_blocks))), replace=False)
    )
print(f"{len(candidate_blocks)} candidate blocks (citizen-science ∪ expert presences)")

# ---------------------------------------------------------------- run the curve
source_records, one_class_records, test_size_rows, buffer_removed = [], [], [], {}
for seed in SEEDS:
    test_blocks = test_blocks_by_seed[seed]
    cs_test_mask = np.isin(cs_block, list(test_blocks))
    expert_test_mask = np.isin(expert_block, list(test_blocks))
    bg_test_mask = np.isin(bg_block, list(test_blocks))

    cs_train_mask, expert_train_mask, bg_train_mask = ~cs_test_mask, ~expert_test_mask, ~bg_test_mask

    # Buffer: training points within BUFFER_M of any test point of this seed leave training.
    coords = {"citizen_science": (cs_x, cs_y, cs_test_mask, cs_train_mask),
              "expert": (expert_x, expert_y, expert_test_mask, expert_train_mask),
              "background": (bg_x, bg_y, bg_test_mask, bg_train_mask)}
    buffer_removed[str(seed)] = {}
    if BUFFER_M > 0:
        test_tree = cKDTree(np.vstack([np.column_stack([x[t], y[t]]) for x, y, t, _ in coords.values()]))
    for source, (x, y, _, train_mask) in coords.items():
        n_before = int(train_mask.sum())
        if BUFFER_M > 0:
            dist, _ = test_tree.query(np.column_stack([x[train_mask], y[train_mask]]))
            train_mask[np.flatnonzero(train_mask)[dist <= BUFFER_M]] = False  # in place
        buffer_removed[str(seed)][source] = {"n_train_before": n_before, "n_removed": n_before - int(train_mask.sum())}

    cs_train_emb, cs_test_emb = cs_emb[cs_train_mask], cs_emb[cs_test_mask]
    expert_train_emb, expert_test_emb = expert_emb[expert_train_mask], expert_emb[expert_test_mask]
    expert_train_poly = expert_poly_id[expert_train_mask]
    bg_train_emb, bg_test_emb = bg_emb[bg_train_mask], bg_emb[bg_test_mask]

    test_size_rows.append({
        "seed": seed,
        "n_test_cs": len(cs_test_emb),
        "n_test_expert_pixels": len(expert_test_emb),
        "n_test_expert_polygons": len(np.unique(expert_poly_id[expert_test_mask])),
        "n_test_expert_blocks": len(np.unique(expert_block[expert_test_mask])),
        "expert_share_of_test_presences": len(expert_test_emb) / (len(cs_test_emb) + len(expert_test_emb)),
        "n_test_background": len(bg_test_emb),
    })

    for lvl in LEVELS:
        if lvl >= 100:  # expert only, no citizen science
            train_pres_emb = expert_train_emb
        else:
            incl = included_polygons(lvl)
            train_pres_emb = np.concatenate([cs_train_emb, expert_train_emb[np.isin(expert_train_poly, incl)]])

        # One-Class SVM: presences only in training, pooled test presences against the test background
        scaler_oc = StandardScaler().fit(train_pres_emb)
        oc_model = OneClassSVM(**ONE_CLASS).fit(scaler_oc.transform(train_pres_emb))
        oc_pres = oc_model.decision_function(scaler_oc.transform(np.concatenate([cs_test_emb, expert_test_emb])))
        oc_bg = oc_model.decision_function(scaler_oc.transform(bg_test_emb))
        one_class_records.append({
            "seed": seed, "level_pct": lvl, "classifier": "OneClassSVM", "n_train_presence": len(train_pres_emb),
            "roc_auc": roc_auc_score(np.concatenate([np.ones(len(oc_pres)), np.zeros(len(oc_bg))]),
                                     np.concatenate([oc_pres, oc_bg])),
            "boyce": continuous_boyce(oc_pres, oc_bg),
        })

        X_train = np.concatenate([train_pres_emb, bg_train_emb])
        y_train = np.concatenate([np.ones(len(train_pres_emb)), np.zeros(len(bg_train_emb))])
        scaler = StandardScaler().fit(X_train)

        for name, params in CLASSIFIERS.items():
            model = MAKERS[name](**params).fit(scaler.transform(X_train), y_train)
            score_cs = model.predict_proba(scaler.transform(cs_test_emb))[:, 1]
            score_expert = model.predict_proba(scaler.transform(expert_test_emb))[:, 1]
            score_bg = model.predict_proba(scaler.transform(bg_test_emb))[:, 1]
            # Each subset of test presences is scored against the same test background.
            subsets = {
                "pooled": np.concatenate([score_cs, score_expert]),
                "expert only": score_expert,
                "citizen science only": score_cs,
            }
            for subset, score_pres in subsets.items():
                y_true = np.concatenate([np.ones(len(score_pres)), np.zeros(len(score_bg))])
                source_records.append({
                    "seed": seed, "level_pct": lvl, "classifier": name, "test_presences": subset,
                    "n_test_presences": len(score_pres),
                    "roc_auc": roc_auc_score(y_true, np.concatenate([score_pres, score_bg])),
                    "boyce": continuous_boyce(score_pres, score_bg),
                })
    print(f"seed {seed} done")

test_size_df = pd.DataFrame(test_size_rows)
source_df = pd.DataFrame(source_records)
source_summary = (
    source_df.groupby(["classifier", "level_pct", "test_presences"], sort=False)
    .agg(roc_auc_mean=("roc_auc", "mean"), roc_auc_sd=("roc_auc", "std"),
         boyce_mean=("boyce", "mean"), boyce_sd=("boyce", "std"),
         n_test_presences_mean=("n_test_presences", "mean"))
    .reset_index()
)

# ---------------------------------------------------------------- reuse of expert test blocks across seeds
expert_blocks_all = set(np.unique(expert_block))
pixels_in_block = Counter(expert_block.tolist())
block_uses, pixel_sets, reuse_rows = Counter(), [], []
for seed in SEEDS:
    blocks = sorted(str(b) for b in set(test_blocks_by_seed[seed]) & expert_blocks_all)
    block_uses.update(blocks)
    pixel_sets.append(set(np.flatnonzero(np.isin(expert_block, blocks))))
    counts = [pixels_in_block[b] for b in blocks]
    reuse_rows.append({
        "seed": seed, "expert_test_blocks": ", ".join(blocks),
        "expert_pixels_per_block": ", ".join(map(str, counts)),
        "largest_block_share": max(counts) / sum(counts),
    })

# ---------------------------------------------------------------- paired differences per seed (same test blocks)
wide = source_df.pivot_table(index=["classifier", "test_presences", "seed"], columns="level_pct", values=["roc_auc", "boyce"])
paired_rows = []
for metric in ["roc_auc", "boyce"]:
    for lvl in LEVELS[1:]:
        diff = (wide[metric][lvl] - wide[metric][0]).rename("diff").reset_index()
        for (clf, subset), d in diff.groupby(["classifier", "test_presences"], sort=False):
            paired_rows.append({
                "classifier": clf, "test_presences": subset, "metric": metric, "comparison": f"{lvl}% minus 0%",
                "diff_mean": d["diff"].mean(), "diff_sd": d["diff"].std(),
                "seeds_up": int((d["diff"] > 0).sum()), "seeds_down": int((d["diff"] < 0).sum()),
            })
paired_df = pd.DataFrame(paired_rows)

# ---------------------------------------------------------------- save
OUT_DIR.mkdir(parents=True, exist_ok=True)
source_df.to_csv(OUT_DIR / "per_seed.csv", index=False)
source_summary.to_csv(OUT_DIR / "summary.csv", index=False)
paired_df.to_csv(OUT_DIR / "paired_differences.csv", index=False)
test_size_df.to_csv(OUT_DIR / "test_sizes.csv", index=False)
pd.DataFrame(reuse_rows).to_csv(OUT_DIR / "block_reuse.csv", index=False)
nominal_df.to_csv(OUT_DIR / "nominal_levels.csv", index=False)
pd.DataFrame(one_class_records).to_csv(OUT_DIR / "one_class_per_seed.csv", index=False)


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


BG_FILE = pool_file(ROOT, BACKGROUND)
(OUT_DIR / "run.json").write_text(json.dumps({
    "run_date": date.today().isoformat(),
    "script": "experiments/effort_reduction_curve/run.py",
    "command": f"python experiments/effort_reduction_curve/run.py --background {BACKGROUND}"
               + (f" --buffer-m {BUFFER_M:g}" if BUFFER_M > 0 else ""),
    "git_commit": _git("rev-parse", "HEAD"),
    "git_uncommitted_changes": bool(_git("status", "--porcelain")),
    "levels_pct": LEVELS, "seeds": SEEDS, "polygon_order_seed": POLYGON_ORDER_SEED,
    "test_fraction": TEST_FRACTION, "background": BACKGROUND, "classifiers": CLASSIFIERS,
    "buffer_m": BUFFER_M, "buffer_removed_from_training_by_seed": buffer_removed,
    "one_class_svm": ONE_CLASS,
    "embeddings": PILOT_DIR.name,
    "n_cs_presences": len(cs_emb), "n_cs_matched": cs_n_matched, "n_cs_rows": len(dealbata),
    "n_expert_pixels": len(expert_emb), "n_expert_polygons": len(np.unique(expert_poly_id)),
    "n_background": len(bg_emb), "n_candidate_blocks": len(candidate_blocks),
    "n_test_blocks_per_seed": {str(s): len(b) for s, b in test_blocks_by_seed.items()},
    "n_expert_blocks": len(expert_blocks_all),
    "n_expert_blocks_in_a_test_set": len(block_uses),
    "n_expert_blocks_in_two_or_more_seeds": sum(v >= 2 for v in block_uses.values()),
    "n_expert_test_pixels_summed_over_seeds": sum(map(len, pixel_sets)),
    "n_expert_test_pixels_distinct": len(set().union(*pixel_sets)),
    "inputs_sha256": {
        CS_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(CS_FILE),
        EXPERT_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(EXPERT_FILE),
        PILOT_DIR.relative_to(ROOT).as_posix() + "/": manifest.sha256_dir(PILOT_DIR),
        BG_FILE.relative_to(ROOT).as_posix(): manifest.sha256_file(BG_FILE),
    },
}, indent=1))
print(f"saved to {OUT_DIR}")
