"""Manifest of the derived files in data/processed/ (file, hash, inputs, seed, parameters).

data/processed/ is not versioned, so data/processed_manifest.csv records what each file
was built from. `record` writes one row; `verify` stops a notebook that is about to read
a derived file whose content or inputs no longer match its row.
"""
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

MANIFEST = Path("data") / "processed_manifest.csv"
COLUMNS = ["file", "sha256", "built_on", "built_by", "inputs", "seed", "params"]
UNKNOWN_INPUTS = "unknown (built before the manifest)"


class StaleDerivedFile(RuntimeError):
    """A derived file, or one of its inputs, does not match the manifest."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_dir(path: Path) -> str:
    """Hash of a folder: sha256 over the sorted "<name> <sha256>" lines of its files."""
    lines = [f"{p.name} {sha256_file(p)}" for p in sorted(path.iterdir()) if p.is_file()]
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_dir(path) if path.is_dir() else sha256_file(path)


def input_ref(root: Path, path: Path) -> str:
    """One input as "<path relative to the repository>@<sha256>" (folders end in "/")."""
    rel = path.relative_to(root).as_posix() + ("/" if path.is_dir() else "")
    return f"{rel}@{sha256_path(path)}"


def read(root: Path) -> dict[str, dict]:
    path = root / MANIFEST
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {row["file"]: row for row in csv.DictReader(f)}


def record(root: Path, file: Path, built_by: str, inputs: list[str] | str, seed=None,
           params: dict | None = None, built_on: str | None = None) -> dict:
    """Write (or replace) the row of `file`. `built_on` defaults to the file's modification time."""
    rows = read(root)
    rel = file.relative_to(root).as_posix()
    if built_on is None:
        built_on = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    rows[rel] = {
        "file": rel,
        "sha256": sha256_file(file),
        "built_on": built_on,
        "built_by": built_by,
        "inputs": inputs if isinstance(inputs, str) else ";".join(inputs),
        "seed": "" if seed is None else str(seed),
        "params": json.dumps(params or {}, sort_keys=True),
    }
    with open(root / MANIFEST, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows[k] for k in sorted(rows))
    return rows[rel]


def verify(root: Path, file: Path) -> dict:
    """Return the manifest row of `file`, or raise StaleDerivedFile saying what changed."""
    rel = file.relative_to(root).as_posix()
    row = read(root).get(rel)
    fix = "run notebooks/05_data_integration/background_pools.ipynb"
    if row is None:
        raise StaleDerivedFile(f"{rel} has no row in {MANIFEST.as_posix()}: {fix}.")
    if not file.exists():
        raise StaleDerivedFile(f"{rel} is in the manifest but the file is missing: {fix}.")
    if sha256_file(file) != row["sha256"]:
        raise StaleDerivedFile(f"{rel} does not match the hash in the manifest: {fix}.")
    if row["inputs"] != UNKNOWN_INPUTS:
        for ref in row["inputs"].split(";"):
            path, _, recorded = ref.rpartition("@")
            if not (root / path).exists():
                raise StaleDerivedFile(f"{rel}: its input {path} is missing.")
            if sha256_path(root / path) != recorded:
                raise StaleDerivedFile(
                    f"{rel} was built from another version of {path} (the input changed since "
                    f"{row['built_on']}): {fix}."
                )
    return row
