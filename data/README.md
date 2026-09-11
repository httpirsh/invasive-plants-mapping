# Data

```
data/
├── raw/                  ← original, unmodified data
│   ├── citizen_science/
│   └── satellite/
├── interim/              ← data after intermediate processing
│   ├── citizen_science/
│   ├── satellite/
│   └── spatial/          ← intermediate spatial joins/products
├── processed/            ← final data used by the models
│   ├── datasets/          ← labelled ML-ready datasets
│   ├── features/          ← conventional (non-foundation-model) features
│   └── embeddings/        ← Earth Observation Foundation Model embeddings
└── external/             ← auxiliary third-party data
    ├── shapefiles/
    ├── land_cover/
    └── auxiliary/
```

Data files are not version-controlled (see `.gitignore`); this file
documents the provenance of each dataset used.

## Datasets

### Dataset: <name>

- **Source:**
- **URL:**
- **Access date:**
- **Spatial coverage:**
- **Temporal coverage:**
- **License:**
- **Preprocessing:**
