# Evaluation plan

1. Freeze eligibility rules, labels, annotation guide and primary macro-F1 metric.
2. Remove exact duplicates before splitting; audit paraphrases and shared templates.
3. Allocate train/validation/test by subject. Record split IDs in controlled storage.
4. Select hyperparameters and abstention threshold on validation data only.
5. Evaluate once on the untouched test partition; compare majority and TF-IDF baselines.
6. Report per-class precision/recall/F1, confusion matrix, log loss, calibration,
   coverage and selective accuracy. Bootstrap subjects, not individual posts.
7. Repeat seeds and test platform, language and temporal shifts.

The CLI demo uses fixed baseline hyperparameters and a fixed default threshold,
so it does not tune on its test set. Notebook 10 demonstrates a test-set sensitivity
curve only; do not use that curve for threshold selection.

Temporal holdout and unseen-author holdout answer different questions. For both,
hold out future records from entirely held-out subjects. Perform text ablations,
negation/sarcasm tests and source-type slices. Suppress slices with too few subjects.

A percentile bootstrap interval does not account for dataset selection or annotation
bias. ECE depends on bins and sample size. Neither confidence nor an explanation
proves correctness. Synthetic metrics are software diagnostics only.
