"""Sensitivity of the effort-reduction curve (RQ1) to a train-test buffer.

Reads the curve without buffer (results/effort_reduction_curve/) and the runs of run.py with
--buffer-m 300 and --buffer-m 1000, and writes the differences paired by seed (with buffer
minus without) to results/effort_reduction_curve_buffer_comparison/. It trains nothing.

Compared: ROC-AUC and Boyce at 0%, 90% and 100% of the expert polygons and the difference
90% minus 0%, for both classifiers, on the pooled test presences and on the expert ones.

Criterion, fixed on 2026-11-14 before the buffered runs: for ROC-AUC, a comparison is met if
|mean difference| < its standard deviation across the five seeds (or all differences are 0);
the buffer "does not change the reading of RQ1" only if all 16 comparisons are met. The same
is reported without seed 5 as a secondary reading, which does not decide. Boyce is reported
only. Reasoning: thesis/notes.md, entry on the buffer in spatial validation.

Usage: python experiments/effort_reduction_curve/compare_buffer.py
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT))
from src import manifest

BUFFERS_M = [300, 1000]
LEVELS = [0, 90, 100]
SUBSETS = ["pooled", "expert only"]
SEED_LEFT_OUT = 5  # the seed where the 1 km buffer removes most training presences
BASE_DIR = ROOT / "results" / "effort_reduction_curve"
OUT_DIR = ROOT / "results" / "effort_reduction_curve_buffer_comparison"
KEY = ["classifier", "test_presences", "seed"]


def buffer_dir(buffer_m):
    return ROOT / "results" / f"effort_reduction_curve_buffer_{buffer_m}m"


def wide(folder, metric):
    """One row per classifier, test subset and seed; columns 0, 90, 100 and '90 minus 0'."""
    df = pd.read_csv(folder / "per_seed.csv")
    df = df[df["level_pct"].isin(LEVELS) & df["test_presences"].isin(SUBSETS)]
    w = df.pivot(index=KEY, columns="level_pct", values=metric)
    w.columns = [f"{c}%" for c in w.columns]
    w["90% minus 0%"] = w["90%"] - w["0%"]
    return w


def met(d):
    return bool((d == 0).all() or abs(d.mean()) < d.std())


base_run = json.loads((BASE_DIR / "run.json").read_text())
rows, removed_rows, inputs = [], [], {}
for buffer_m in BUFFERS_M:
    folder = buffer_dir(buffer_m)
    run = json.loads((folder / "run.json").read_text())
    # The runs are comparable only with the same inputs, the same test set and the stated buffer.
    assert run["buffer_m"] == buffer_m, f"{folder.name}: buffer_m is {run['buffer_m']}"
    assert run["inputs_sha256"] == base_run["inputs_sha256"], f"{folder.name}: inputs differ from the curve without buffer"
    assert (folder / "test_sizes.csv").read_bytes() == (BASE_DIR / "test_sizes.csv").read_bytes(), f"{folder.name}: test set differs"
    for seed, by_source in run["buffer_removed_from_training_by_seed"].items():
        for source, n in by_source.items():
            removed_rows.append({"buffer_m": buffer_m, "seed": int(seed), "source": source, **n})
    for metric in ["roc_auc", "boyce"]:
        w0, w1 = wide(BASE_DIR, metric), wide(folder, metric)
        for what in w0.columns:
            diff = (w1[what] - w0[what]).unstack("seed")
            for (clf, subset), d in diff.iterrows():
                d_rest = d.drop(SEED_LEFT_OUT)
                rows.append({
                    "buffer_m": buffer_m, "metric": metric, "classifier": clf, "test_presences": subset, "what": what,
                    "no_buffer_mean": w0[what].unstack("seed").loc[(clf, subset)].mean(),
                    "buffer_mean": w1[what].unstack("seed").loc[(clf, subset)].mean(),
                    "diff_mean": d.mean(), "diff_sd": d.std(),
                    "seeds_up": int((d > 0).sum()), "seeds_down": int((d < 0).sum()),
                    "criterion_met": met(d) if metric == "roc_auc" else None,
                    f"seed{SEED_LEFT_OUT}_share_of_diff_sum": d[SEED_LEFT_OUT] / d.sum() if d.sum() != 0 else None,
                    f"diff_mean_without_seed{SEED_LEFT_OUT}": d_rest.mean(), f"diff_sd_without_seed{SEED_LEFT_OUT}": d_rest.std(),
                    f"criterion_met_without_seed{SEED_LEFT_OUT}": met(d_rest) if metric == "roc_auc" else None,
                    **{f"diff_seed{s}": v for s, v in d.items()},
                })
    for name in ["per_seed.csv", "run.json"]:
        inputs[(folder / name).relative_to(ROOT).as_posix()] = manifest.sha256_file(folder / name)
for name in ["per_seed.csv", "run.json"]:
    inputs[(BASE_DIR / name).relative_to(ROOT).as_posix()] = manifest.sha256_file(BASE_DIR / name)

paired = pd.DataFrame(rows)
auc = paired[paired["metric"] == "roc_auc"]
verdict = {
    str(b): {"comparisons": int(len(g)), "met": int(g["criterion_met"].sum()),
             f"met_without_seed{SEED_LEFT_OUT}": int(g[f"criterion_met_without_seed{SEED_LEFT_OUT}"].sum())}
    for b, g in auc.groupby("buffer_m")
}

OUT_DIR.mkdir(parents=True, exist_ok=True)
paired.to_csv(OUT_DIR / "paired_vs_no_buffer.csv", index=False)
pd.DataFrame(removed_rows).to_csv(OUT_DIR / "removed_from_training.csv", index=False)


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


(OUT_DIR / "run.json").write_text(json.dumps({
    "run_date": date.today().isoformat(),
    "script": "experiments/effort_reduction_curve/compare_buffer.py",
    "git_commit": _git("rev-parse", "HEAD"),
    "git_uncommitted_changes": bool(_git("status", "--porcelain")),
    "buffers_m": BUFFERS_M, "levels_pct": LEVELS, "test_presences": SUBSETS, "seed_left_out": SEED_LEFT_OUT,
    "criterion": "ROC-AUC: |mean paired difference| < its standard deviation across seeds, in all comparisons",
    "criterion_met_count": verdict,
    "inputs_sha256": inputs,
}, indent=1))
print(json.dumps(verdict, indent=1))
print(f"saved to {OUT_DIR.relative_to(ROOT)}")
