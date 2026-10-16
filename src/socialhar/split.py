"""Group disjoint partitions prevent repeated-author leakage."""
from sklearn.model_selection import GroupShuffleSplit

def grouped_split(frame, seed=42, test_size=0.2):
    if frame.subject_id.nunique() < 5:
        raise ValueError("Need at least five distinct subjects")
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train, test = next(splitter.split(frame, groups=frame.subject_id))
    a, b = frame.iloc[train].copy(), frame.iloc[test].copy()
    if set(a.subject_id) & set(b.subject_id):
        raise RuntimeError("Subject leakage")
    return a, b

def chronological_split(frame, cutoff):
    """Strict future holdout; authors can overlap. Use for a separate research question."""
    import pandas as pd
    boundary = pd.Timestamp(cutoff)
    if boundary.tzinfo is None:
        raise ValueError("Cutoff must include timezone")
    a, b = frame[frame.timestamp < boundary].copy(), frame[frame.timestamp >= boundary].copy()
    if a.empty or b.empty:
        raise ValueError("Cutoff produces an empty partition")
    return a, b
