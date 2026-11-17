"""Sensitivity of the effort-reduction curve (RQ1) to a train-test buffer.

Reads the curve without buffer (results/effort_reduction_curve/) and the runs of run.py with
--buffer-m 300 and --buffer-m 1000, and writes the differences paired by fold (with buffer
minus without) to results/effort_reduction_curve_buffer_comparison/. It trains nothing.

Compared: sensitivity at 10% of predicted area at 0%, 90% and 100% of the expert polygons
and the difference 90% minus 0%, on the pooled test presences and on the expert ones; both
the per-fold values (paired by block) and the pooled values.

Criterion (own choice, fixed 2026-11-17 before the buffered runs of the presence-only
design): a comparison is met if the absolute mean of the per-fold differences is smaller
than their standard deviation across folds (or every difference is 0); the buffer "does not
change the reading of RQ1" only if all 8 comparisons are met. ROC-AUC is reported only.
Reasoning: thesis/notes.md, entry on the buffer in spatial validation.

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
CONDITIONS = ["0", "90", "100"]
SUBSETS = ["pooled", "expert only"]
METRICS = ["sensitivity_at_10pct", "roc_auc"]
BASE_DIR = ROOT / "results" / "effort_reduction_curve"
OUT_DIR = ROOT / "results" / "effort_reduction_curve_buffer_comparison"


def buffer_dir(buffer_m):
    return ROOT / "results" / f"effort_reduction_curve_buffer_{buffer_m}m"


def wide(folder, metric):
    """One row per test subset and fold; columns 0, 90, 100 and '90 minus 0'."""
    df = pd.read_csv(folder / "per_fold.csv", dtype={"condition": str})
    df = df[df["condition"].isin(CONDITIONS) & df["test_presences"].isin(SUBSETS)]
    w = df.pivot(index=["test_presences", "fold"], columns="condition", values=metric)
    w.columns = [f"{c}%" for c in w.columns]
    w["90% minus 0%"] = w["90%"] - w["0%"]
    return w


def pooled(folder):
    df = pd.read_csv(folder / "summary.csv", dtype={"condition": str})
    df = df[df["condition"].isin(CONDITIONS) & df["test_presences"].isin(SUBSETS)]
    w = df.pivot(index="test_presences", columns="condition", values="pooled_sensitivity_at_10pct")
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
    # The runs are comparable only with the same inputs, the same folds and the stated buffer.
    assert run["buffer_m"] == buffer_m, f"{folder.name}: buffer_m is {run['buffer_m']}"
    assert not run["smoke_test"] and not base_run["smoke_test"]
    assert run["inputs_sha256"] == base_run["inputs_sha256"], f"{folder.name}: inputs differ from the curve without buffer"
    assert run["folds"] == base_run["folds"], f"{folder.name}: folds differ"
    assert (folder / "test_sizes.csv").read_bytes() == (BASE_DIR / "test_sizes.csv").read_bytes(), f"{folder.name}: test set differs"
    for fold, by_source in run["buffer_removed_from_training_by_fold"].items():
        for source, n in by_source.items():
            removed_rows.append({"buffer_m": buffer_m, "fold": fold, "source": source, **n})
    p0, p1 = pooled(BASE_DIR), pooled(folder)
    for metric in METRICS:
        w0, w1 = wide(BASE_DIR, metric), wide(folder, metric)
        for what in w0.columns:
            for subset in SUBSETS:
                d = (w1[what] - w0[what]).xs(subset, level="test_presences").dropna()
                rows.append({
                    "buffer_m": buffer_m, "metric": metric, "test_presences": subset, "what": what,
                    "no_buffer_per_fold_mean": w0[what].xs(subset, level="test_presences").mean(),
                    "buffer_per_fold_mean": w1[what].xs(subset, level="test_presences").mean(),
                    "diff_mean": d.mean(), "diff_sd": d.std(), "n_folds": len(d),
                    "folds_up": int((d > 0).sum()), "folds_down": int((d < 0).sum()),
                    "criterion_met": met(d) if metric == "sensitivity_at_10pct" else None,
                    "no_buffer_pooled": p0.loc[subset, what] if metric == "sensitivity_at_10pct" else None,
                    "buffer_pooled": p1.loc[subset, what] if metric == "sensitivity_at_10pct" else None,
                })
    for name in ["per_fold.csv", "summary.csv", "run.json"]:
        inputs[(folder / name).relative_to(ROOT).as_posix()] = manifest.sha256_file(folder / name)
for name in ["per_fold.csv", "summary.csv", "run.json"]:
    inputs[(BASE_DIR / name).relative_to(ROOT).as_posix()] = manifest.sha256_file(BASE_DIR / name)

paired = pd.DataFrame(rows)
sens = paired[paired["metric"] == "sensitivity_at_10pct"]
verdict = {str(b): {"comparisons": int(len(g)), "met": int(g["criterion_met"].sum())} for b, g in sens.groupby("buffer_m")}

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
    "buffers_m": BUFFERS_M, "conditions": CONDITIONS, "test_presences": SUBSETS,
    "criterion": "sensitivity at 10% of area: |mean paired difference across folds| < its sd, in all comparisons",
    "criterion_met_count": verdict,
    "inputs_sha256": inputs,
}, indent=1))
print(json.dumps(verdict, indent=1))
print(f"saved to {OUT_DIR.relative_to(ROOT)}")
