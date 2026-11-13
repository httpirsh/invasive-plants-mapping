"""Side-by-side comparison of the all-years and the 2021-2025 runs.

Reads what rerun.py and design_counts.py wrote under results/temporal_window_2021_2025/
and writes comparison.md and comparison_curve.csv there.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
OUT = ROOT / "results" / "temporal_window_2021_2025"
OLD, NEW = OUT / "old_all_years", OUT / "new_2021_2025"
L = []  # lines of the report


def md(df, floatfmt=".3f"):
    """Markdown table (no extra dependency)."""
    def cell(v):
        if isinstance(v, float):
            return "" if pd.isna(v) else (f"{v:.0f}" if float(v).is_integer() and abs(v) >= 10 else f"{v:{floatfmt}}")
        return str(v)
    d = df.reset_index()
    rows = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * len(d.columns)]
    rows += ["| " + " | ".join(cell(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join(rows)


def side(old, new, cols, index):
    o, n = old.set_index(index)[cols], new.set_index(index)[cols]
    t = pd.concat({"all years": o, "2021-2025": n, "difference": n - o}, axis=1)
    t.columns = [f"{c} ({k})" for k, c in t.columns]
    order = [f"{c} ({k})" for c in cols for k in ("all years", "2021-2025", "difference")]
    return t[order]


L += ["# All years (3 000 presences) vs. 2021-2025 (2 465 presences)", "",
      "Same code, same background pools, same seeds; only the citizen-science presence file changes.",
      "Made by `experiments/temporal_window_2021_2025/` (`rerun.py`, `design_counts.py`, `compare.py`).",
      "ROC-AUC and continuous Boyce index, mean over 5 spatial-block seeds.", ""]

# --- what is and is not held fixed -------------------------------------------------
co, cn = json.loads((OLD / "curve.json").read_text()), json.loads((NEW / "curve.json").read_text())
same_blocks = sum(co["test_blocks"][s] == cn["test_blocks"][s] for s in co["test_blocks"])
so, sn = json.loads((OLD / "presence_background.json").read_text()), json.loads((NEW / "presence_background.json").read_text())
L += ["## What differs between the two runs besides the training presences", "",
      f"- Curve: {co['n_cs']} vs. {cn['n_cs']} citizen-science presences with an embedding; "
      f"{co['n_candidate_blocks']} vs. {cn['n_candidate_blocks']} candidate 10 km blocks; "
      f"test blocks identical in {same_blocks} of {len(co['test_blocks'])} seeds.",
      f"- Standalone 0% notebooks: {so['n_blocks']} vs. {sn['n_blocks']} blocks (presences + background).",
      "- The test presences change with the file too: each run is tested on its own citizen-science presences "
      "(plus the same expert pixels in the curve).",
      "- So a difference between the two curve columns mixes three things: training presences, test presences and "
      "test blocks. The 100% level shows the size of the last two: there the training set (expert pixels only) is "
      "identical in both runs, and only the test set changes.",
      "- The all-years column is a fresh run of the unmodified notebooks; it matches the outputs they had before "
      "(kept in `old_all_years/notebooks_as_found/`).", ""]

# --- curve ---------------------------------------------------------------------------
cols = ["roc_auc_mean", "boyce_mean"]
cur = side(pd.read_csv(OLD / "curve_summary.csv"), pd.read_csv(NEW / "curve_summary.csv"), cols + ["roc_auc_sd", "boyce_sd"], ["classifier", "level_pct"])
cur.to_csv(OUT / "comparison_curve.csv")
show = [c for c in cur.columns if "_sd" not in c or "difference" not in c]
L += ["## RQ1 effort-reduction curve (uniform background)", "", md(cur[[c for c in cur.columns if "_sd" not in c]]), "",
      "Standard deviation across seeds:", "", md(cur[[c for c in cur.columns if "_sd" in c and "difference" not in c]]), ""]
nom = side(pd.read_csv(OLD / "curve_nominal.csv"), pd.read_csv(NEW / "curve_nominal.csv"), ["n_cs_presences", "n_expert_pixels", "total_N"], ["level_pct"])
L += ["Training-set size (nominal, before the test split):", "", md(nom[[c for c in nom.columns if "difference" not in c]], ".0f"), ""]

forest = side(pd.read_csv(OLD / "curve_forest_summary.csv"), pd.read_csv(NEW / "curve_forest_summary.csv"), cols, ["classifier", "level_pct"])
forest.to_csv(OUT / "comparison_curve_forest.csv")
L += ["## Diagnostic 1: the curve under the forest-only background", "", md(forest), ""]

# --- standalone 0% notebooks ----------------------------------------------------------
for title, f in [("Presence vs. background, citizen science only (standalone notebook)", "presence_background.csv"),
                 ("One-class method selection, citizen science only (standalone notebook)", "one_class_selection.csv")]:
    o, n = pd.read_csv(OLD / f, index_col=0), pd.read_csv(NEW / f, index_col=0)
    t = pd.concat({"all years": o, "2021-2025": n, "difference": n - o}, axis=1)[
        [(k, c) for c in ("ROC-AUC (mean)", "Boyce (mean)") for k in ("all years", "2021-2025", "difference")]]
    t.columns = [f"{c} ({k})" for k, c in t.columns]
    L += [f"## {title}", "", md(t), ""]

# --- diagnostics ----------------------------------------------------------------------
def two(name, rows):
    return pd.DataFrame(rows, columns=[name, "all years", "2021-2025"]).set_index(name)

ro, rn = json.loads((OLD / "redundancy.json").read_text()), json.loads((NEW / "redundancy.json").read_text())
cso, csn = pd.read_csv(OLD / "redundancy_cosine.csv"), pd.read_csv(NEW / "redundancy_cosine.csv")
rows = [("citizen-science presences", ro["n_cs"], rn["n_cs"]),
        ("ICC between expert polygons (expert data only)", ro["icc_observed"], rn["icc_observed"])]
rows += [(f"mean cosine similarity, {a}", b, c) for a, b, c in zip(cso["pair type"], cso["mean cosine sim"], csn["mean cosine sim"])]
L += ["## Diagnostic 2: redundancy inside expert polygons", "", md(two("quantity", rows)), ""]

ho, hn = json.loads((OLD / "habitat.json").read_text()), json.loads((NEW / "habitat.json").read_text())
keys = [("citizen-science presences", "n_cs"), ("10 km blocks with citizen science", "n_cs_blocks"),
        ("convex hull of citizen science (km2)", "cs_hull_km2"), ("presences inside the expert-containing blocks", "n_cs_in_expert_blocks"),
        ("mean cosine similarity, citizen science, whole extent", "cos_cs_full"),
        ("mean cosine similarity, citizen science, expert blocks only", "cos_cs_expert_blocks"),
        ("mean cosine similarity, expert, between polygons", "cos_expert_between")]
L += ["## Diagnostic 3: habitat", "", md(two("quantity", [(a, ho[k], hn[k]) for a, k in keys])), ""]
comp = pd.concat({"all years": pd.read_csv(OLD / "habitat_composition.csv", index_col=0),
                  "2021-2025": pd.read_csv(NEW / "habitat_composition.csv", index_col=0)}, axis=1)
comp.columns = [f"{c} ({k})" for k, c in comp.columns]
L += ["COS 2023 class under each point (%):", "", md(comp, ".1f"), ""]

po, pn = json.loads((OLD / "label_purity.json").read_text()), json.loads((NEW / "label_purity.json").read_text())
rows = [("presences with an embedding", po["n_presences"], pn["n_presences"]),
        ("inside an expert polygon", po["n_inside"], pn["n_inside"]),
        ("within 100 m of an expert polygon", po["n_within_100m"], pn["n_within_100m"]),
        ("flagged as embedding outliers (top 5%)", po["n_outliers"], pn["n_outliers"]),
        ("other observers among the outliers (%)", 100 * po["others_share_outliers"], 100 * pn["others_share_outliers"]),
        ("other observers among the rest (%)", 100 * po["others_share_rest"], 100 * pn["others_share_rest"])]
for k in po["purity"]:
    rows += [(f"Random Forest ROC-AUC, {k}", po["purity"][k]["roc_auc"], pn["purity"][k]["roc_auc"]),
             (f"Random Forest Boyce, {k}", po["purity"][k]["boyce"], pn["purity"][k]["boyce"])]
L += ["## Diagnostic 4: label purity", "", md(two("quantity", rows)), ""]

# --- counts and RQ2 draw --------------------------------------------------------------
dc = pd.read_csv(OUT / "design_counts.csv", index_col=0)
dc.columns = ["all years", "2021-2025"]
L += ["## Counts quoted in the design docs, and the RQ2 draw of 150", "", md(dc), ""]

(OUT / "comparison.md").write_text("\n".join(L))
print("\n".join(L))
