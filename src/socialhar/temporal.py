"""Aggregate posting-time patterns, never inferred physical routines."""
import numpy as np
import pandas as pd

def aggregate_activity(frame, min_subjects=5, timezone="UTC"):
    if min_subjects < 2:
        raise ValueError("min_subjects must be >=2")
    out = frame.copy()
    out["hour"] = pd.to_datetime(out.timestamp, utc=True).dt.tz_convert(timezone).dt.hour
    groups = out.groupby(["hour", "label"]).agg(
        n=("record_id", "count"), subjects=("subject_id", "nunique")).reset_index()
    # Suppression is a minimum reporting rule, not differential privacy.
    return groups[groups.subjects >= min_subjects].reset_index(drop=True)

def posting_entropy(counts):
    values = np.asarray(counts, dtype=float)
    if np.any(values < 0) or values.sum() <= 0:
        raise ValueError("Counts must be nonnegative with positive total")
    p = values[values > 0] / values.sum()
    return float(-(p * np.log2(p)).sum())
