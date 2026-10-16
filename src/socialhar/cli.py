"""Reproducible command-line demo with machine-readable artifacts."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import joblib
import pandas as pd
from .synthetic import generate
from .schema import validate, LABELS
from .privacy import prepare
from .split import grouped_split
from .models import baseline, predict_selective, explain_linear
from .evaluation import evaluate, cluster_bootstrap_f1, reliability
from .temporal import aggregate_activity
from .topics import fit_topics

def run(frame, output, seed=42, threshold=.5):
    clean = prepare(validate(frame))
    train, test = grouped_split(clean, seed=seed)
    if set(train.label) != set(LABELS):
        raise ValueError("Training split must contain all seven labels")
    model = baseline(seed).fit(train.text, train.label)
    report = evaluate(model, test)
    report["bootstrap_macro_f1"] = cluster_bootstrap_f1(test, model.predict(test.text), seed=seed)
    report["reliability"] = reliability(test.label, model.predict_proba(test.text), model.classes_)
    selected = predict_selective(model, test.text, threshold)
    report["coverage"] = sum(p["label"] != "abstain" for p in selected) / len(selected)
    kept = [i for i, p in enumerate(selected) if p["label"] != "abstain"]
    report["selective_accuracy"] = (
        sum(selected[i]["label"] == test.iloc[i].label for i in kept) / len(kept)
        if kept else None)
    report["scope"] = ("synthetic smoke test only" if clean.permission.eq("synthetic").all()
                       else "research dataset; review provenance before interpretation")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    # No raw text or subject IDs are written to prediction exports.
    pd.DataFrame([{"record_id": rid, **p} for rid, p in zip(test.record_id, selected)]
                 ).drop(columns="probabilities").to_csv(output / "predictions.csv", index=False)
    aggregate_activity(clean).to_csv(output / "aggregate_activity.csv", index=False)
    _, _, _, topics = fit_topics(train.text)
    (output / "topics.json").write_text(json.dumps(topics, indent=2), encoding="utf-8")
    (output / "explanation.json").write_text(
        json.dumps(explain_linear(model, test.iloc[0].text), indent=2), encoding="utf-8")
    # Fitted vectorizers retain vocabulary: treat this artifact as potentially sensitive.
    joblib.dump(model, output / "baseline.joblib")
    digest = hashlib.sha256(clean.to_csv(index=False).encode()).hexdigest()
    manifest = {"seed": seed, "threshold": threshold, "input_sha256": digest,
                "train_rows": len(train), "test_rows": len(test),
                "train_subjects": train.subject_id.nunique(),
                "test_subjects": test.subject_id.nunique(), "classes": list(model.classes_),
                "versions": {p: importlib.metadata.version(p) for p in
                             ["socialhar", "numpy", "pandas", "scikit-learn"]}}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    demo = subs.add_parser("demo")
    demo.add_argument("--output", default="outputs/demo")
    demo.add_argument("--seed", type=int, default=42)
    train = subs.add_parser("train")
    train.add_argument("--data", required=True)
    train.add_argument("--output", required=True)
    train.add_argument("--seed", type=int, default=42)
    train.add_argument("--threshold", type=float, default=.5)
    predict = subs.add_parser("predict")
    predict.add_argument("--model", required=True)
    predict.add_argument("--text", required=True)
    predict.add_argument("--threshold", type=float, default=.5)
    args = parser.parse_args()
    if args.command == "predict":
        # Never load a pickle/joblib file from an untrusted source.
        print(json.dumps(predict_selective(joblib.load(args.model), [args.text], args.threshold)))
    else:
        frame = generate(seed=args.seed) if args.command == "demo" else pd.read_csv(args.data)
        print(json.dumps(run(frame, args.output, args.seed, getattr(args, "threshold", .5)),
                         indent=2))

if __name__ == "__main__":
    main()
