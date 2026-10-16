# Research notebooks

Install `python -m pip install -e ".[dev]"`, then open notebooks in numeric order.
Each has a concrete experiment, runnable cells, interpretation, and a research extension.

| Notebook | Question |
|---|---|
| [01_data_audit](01_data_audit.ipynb) | Dataset audit |
| [02_privacy](02_privacy.ipynb) | Redaction and minimization |
| [03_splits](03_splits.ipynb) | Leakage-resistant evaluation |
| [04_baseline](04_baseline.ipynb) | Interpretable text baseline |
| [05_transformers](05_transformers.ipynb) | Supervised transformer experiment |
| [06_topics](06_topics.ipynb) | Exploratory topic modeling |
| [07_temporal](07_temporal.ipynb) | Posting-time summaries |
| [08_psychology](08_psychology.ipynb) | Sentiment and annotation reliability |
| [09_explainability](09_explainability.ipynb) | Signed feature contributions |
| [10_uncertainty](10_uncertainty.ipynb) | Uncertainty and selective prediction |

All default cells are offline. Optional transformer and psychology runs require
the extras and explicit environment flags documented in notebooks 05 and 08.
Execute all default cells with `python scripts/check_notebooks.py`.
Committed notebooks are intentionally unexecuted; no fabricated outputs or benchmark claims.
