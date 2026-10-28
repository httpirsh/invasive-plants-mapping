# src

Reusable Python modules, extracted from notebooks only once code is
stable and would otherwise be duplicated. Subfolders (e.g. `data/`,
`features/`, `evaluation/`) are created when first needed.

Modules:
- `burned_areas.py`: downloads the ICNF burned areas and applies the
  burned-between-observation-and-2023 rule (used by both
  citizen-science notebooks).
