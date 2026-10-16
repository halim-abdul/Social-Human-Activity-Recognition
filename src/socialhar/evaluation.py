"""Metrics with explicit class order and uncertainty."""
import numpy as np
from sklearn.metrics import (accuracy_score, f1_score, classification_report,
                             confusion_matrix, log_loss)
from .schema import LABELS

def evaluate(model, frame):
    predictions = model.predict(frame.text)
    probabilities = model.predict_proba(frame.text)
    return {
        "n": len(frame), "accuracy": float(accuracy_score(frame.label, predictions)),
        "macro_f1": float(f1_score(frame.label, predictions, labels=LABELS,
                                  average="macro", zero_division=0)),
        "log_loss": float(log_loss(frame.label, probabilities, labels=model.classes_)),
        "label_order": list(LABELS),
        "confusion_matrix": confusion_matrix(frame.label, predictions, labels=LABELS).tolist(),
        "per_class": classification_report(frame.label, predictions, labels=LABELS,
                                           output_dict=True, zero_division=0),
    }

def cluster_bootstrap_f1(frame, predictions, repeats=500, seed=42):
    """Resample subjects, keeping every record from each sampled subject together."""
    if repeats < 20:
        raise ValueError("Use at least 20 bootstrap replicates")
    if len(frame) != len(predictions):
        raise ValueError("Predictions and rows must align")
    rng = np.random.default_rng(seed)
    groups = frame.subject_id.unique()
    if len(groups) < 2:
        raise ValueError("Need at least two subjects")
    truth, pred = frame.label.to_numpy(), np.asarray(predictions)
    subject_ids = frame.subject_id.to_numpy()
    values = []
    for _ in range(repeats):
        indices = np.concatenate([np.flatnonzero(subject_ids == g)
                                  for g in rng.choice(groups, len(groups), replace=True)])
        values.append(f1_score(truth[indices], pred[indices], labels=LABELS,
                               average="macro", zero_division=0))
    return dict(low=float(np.quantile(values, .025)), high=float(np.quantile(values, .975)),
                repeats=repeats, method="subject-cluster percentile bootstrap")

def reliability(y, probabilities, classes, bins=10):
    confidence = probabilities.max(axis=1)
    correct = np.asarray(classes)[probabilities.argmax(axis=1)] == np.asarray(y)
    result = []
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        mask = (confidence >= lo) & ((confidence <= hi) if i == bins - 1 else (confidence < hi))
        if mask.any():
            result.append(dict(n=int(mask.sum()), confidence=float(confidence[mask].mean()),
                               accuracy=float(correct[mask].mean())))
    ece = sum(r["n"] * abs(r["confidence"] - r["accuracy"]) for r in result) / len(y)
    return {"bins": result, "ece": float(ece)}
