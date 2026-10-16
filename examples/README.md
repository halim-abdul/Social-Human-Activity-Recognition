# Reproducible examples

From the repository root:

```bash
python -m pip install -e ".[dev]"
socialhar demo --output outputs/demo
socialhar train --data data/synthetic/activities.csv --output outputs/fixture --seed 42
socialhar predict --model outputs/demo/baseline.joblib --text "I am cooking soup"
python -m pytest -q
python scripts/check_notebooks.py
```

The demo writes metrics.json, manifest.json, predictions.csv, topics.json,
aggregate_activity.csv, explanation.json and baseline.joblib. Nothing is uploaded.
CLI prediction text may appear in local shell history; use only fictional text
in these examples. Raw real inputs belong outside this repository.
