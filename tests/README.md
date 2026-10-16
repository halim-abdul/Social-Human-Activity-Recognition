# Verification

Run `python -m pytest -q` after installing `.[dev]`.
Tests exercise contact redaction, keyed identifiers, fail-closed eligibility,
duplicate rejection, exact-text deduplication, author separation, reproducibility,
logit reconstruction, abstention, bootstrap bounds, topic shape, temporal suppression,
chronological allocation and full output generation.

CI runs core tests and the offline notebooks on Python 3.10, 3.11 and 3.12.
Optional transformer/GPU training and downloaded VADER resources are outside the
offline CI matrix. No passing test count is claimed without a completed run.
