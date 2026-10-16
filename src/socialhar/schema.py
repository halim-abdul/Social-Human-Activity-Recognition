"""Fail-closed input validation and auditable eligibility."""
import pandas as pd

LABELS = ("work", "study", "exercise", "food", "leisure", "social", "other")
REQUIRED = {"record_id", "subject_id", "text", "timestamp", "label", "source_type",
            "permission", "provenance"}
PERMISSIONS = {"synthetic", "consented", "public_reviewed"}

def validate(frame):
    """Return an independent normalized frame or raise a descriptive ValueError.

    public_reviewed means a researcher reviewed reuse rights and ethics; public
    visibility by itself is not a reuse authorization.
    """
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    out = frame.copy()
    if out[list(REQUIRED)].isna().any().any():
        raise ValueError("Required fields cannot be null")
    for key in REQUIRED - {"timestamp"}:
        if not out[key].map(lambda v: isinstance(v, str) and bool(v.strip())).all():
            raise ValueError(f"{key} must contain nonempty strings")
    if out.record_id.duplicated().any():
        raise ValueError("record_id must be unique")
    if not out.permission.isin(PERMISSIONS).all():
        raise ValueError("Unreviewed permission status")
    if not out.source_type.isin(["post", "profile", "comment"]).all():
        raise ValueError("Unsupported source_type")
    if not out.label.isin(LABELS).all():
        raise ValueError("Unknown activity label")
    # Require an explicit timezone instead of silently assigning local times.
    if not out.timestamp.map(lambda x: pd.Timestamp(x).tzinfo is not None).all():
        raise ValueError("Timestamps require a timezone")
    out["timestamp"] = pd.to_datetime(out.timestamp, utc=True, errors="raise")
    if out.text.str.len().gt(10000).any():
        raise ValueError("Text exceeds 10,000-character research limit")
    return out
