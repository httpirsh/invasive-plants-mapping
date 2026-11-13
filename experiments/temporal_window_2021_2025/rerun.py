"""Re-run the RQ1 notebooks and the flat-curve diagnostics on a given presence file.

Each notebook in notebooks/07_foundation_models/ is executed as a copy: the only change
is the citizen-science presence file it reads. The notebooks themselves are not modified.
Executed copies and the tables below go to results/temporal_window_2021_2025/<variant>/.

Usage: python rerun.py <variant> [notebook ...]
  variant = all_years  -> data/interim/citizen_science/inat_dealbata_clean.csv
  variant = 2021_2025  -> data/interim/citizen_science/inat_dealbata_clean_2021_2025.csv

The background pools are the existing files (built with a 50 m buffer around the
all-years presences and the expert polygons); they are read, never rebuilt.
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
NB_DIR = ROOT / "notebooks" / "07_foundation_models"
OUT_ROOT = ROOT / "results" / "temporal_window_2021_2025"
VARIANTS = {"all_years": "inat_dealbata_clean.csv", "2021_2025": "inat_dealbata_clean_2021_2025.csv"}
OUT_DIRS = {"all_years": "old_all_years", "2021_2025": "new_2021_2025"}

# What each notebook leaves behind, written by one cell appended to the copy.
DUMPS = {
    "one_class_method_selection": """
summary.to_csv(_OUT / "one_class_selection.csv")
_json(dict(n_presences=len(pres_emb), n_blocks=len(all_blocks)), "one_class_selection.json")
""",
    "presence_background_citizen_science": """
summary.to_csv(_OUT / "presence_background.csv")
_json(dict(n_presences=len(pres_emb), n_blocks=len(all_blocks)), "presence_background.json")
""",
    "effort_reduction_curve": """
results_df.to_csv(_OUT / "curve_per_seed.csv", index=False)
summary.to_csv(_OUT / "curve_summary.csv", index=False)
nominal_df.to_csv(_OUT / "curve_nominal.csv", index=False)
_json(dict(n_cs=len(cs_emb), n_expert=len(expert_emb), n_candidate_blocks=len(candidate_blocks),
           test_blocks={str(k): sorted(v) for k, v in test_blocks_by_seed.items()}), "curve.json")
""",
    "forest_only_background_check": """
results_df.to_csv(_OUT / "curve_forest_per_seed.csv", index=False)
summary_forest.to_csv(_OUT / "curve_forest_summary.csv", index=False)
""",
    "expert_polygon_redundancy_check": """
summary.to_csv(_OUT / "redundancy_cosine.csv", index=False)
_json(dict(n_cs=len(cs_emb), icc_observed=float(icc_obs), icc_null_mean=float(null_icc.mean())), "redundancy.json")
""",
    "expert_polygon_geographic_diversity": """
from shapely.geometry import MultiPoint as _MP
comp.sort_index().to_csv(_OUT / "habitat_composition.csv")
_json(dict(n_cs=len(cs_emb), n_cs_blocks=len(np.unique(cs_block)), n_expert_blocks=len(np.unique(expert_block)),
           cs_hull_km2=_MP(list(zip(cs_x, cs_y))).convex_hull.area / 1e6,
           cs_pairwise_km_mean=float(cs_dist.mean() / 1000),
           n_cs_in_expert_blocks=int(cs_in_expert_blocks.sum()),
           cos_cs_full=float(cs_sims_full.mean()), cos_cs_expert_blocks=float(cs_sims_restricted.mean()),
           cos_expert_between=float(expert_between_sims.mean())), "habitat.json")
""",
    "label_purity_check": """
_near = pres_pts[pres_pts["dist_to_expert_m"] <= 100]
_json(dict(n_presences=len(matched),
           distance_bands=pres_pts["expert_distance_band"].value_counts().reindex(labels).to_dict(),
           n_within_100m=len(_near), n_inside=int((_near["dist_to_expert_m"] == 0).sum()),
           n_outliers=len(outliers), p95=float(p95),
           others_share_outliers=float((outliers["observer"] != "Observer A").mean()),
           others_share_rest=float((rest["observer"] != "Observer A").mean()),
           accuracy_missing_outliers=float(outliers["accuracy_missing"].mean()),
           accuracy_missing_rest=float(rest["accuracy_missing"].mean()),
           purity={k: dict(roc_auc=float(np.mean(v["auc"])), boyce=float(np.mean(v["boyce"])), n_splits=len(v["auc"]))
                   for k, v in purity_results.items()}), "label_purity.json")
""",
}


def run(variant, name):
    out = OUT_ROOT / OUT_DIRS[variant]
    (out / "notebooks").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    nb = nbformat.read(NB_DIR / f"{name}.ipynb", as_version=4)
    n_swapped = 0
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        n_swapped += c.source.count('"inat_dealbata_clean.csv"')
        c.source = c.source.replace('"inat_dealbata_clean.csv"', f'"{VARIANTS[variant]}"')
        c.source = c.source.replace('"/tmp/', f'"{out / "figures"}/')
    assert n_swapped > 0, f"{name}: presence file not found in the code"
    header = (
        "import json as _j\nfrom pathlib import Path as _P\n"
        f"_OUT = _P({str(out)!r})\n"
        "def _json(d, f):\n    (_OUT / f).write_text(_j.dumps(d, indent=1, default=str))\n"
    )
    nb.cells.append(nbformat.v4.new_code_cell(header + DUMPS[name]))
    NotebookClient(nb, timeout=None, kernel_name="python3",
                   resources={"metadata": {"path": str(NB_DIR)}}).execute()
    nbformat.write(nb, out / "notebooks" / f"{name}.ipynb")
    print(f"[{variant}] {name}: done", flush=True)


if __name__ == "__main__":
    variant = sys.argv[1]
    for name in (sys.argv[2:] or list(DUMPS)):
        run(variant, name)
