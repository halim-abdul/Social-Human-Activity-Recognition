# Model card: SocialHAR baseline and optional transformer

## Status
Research software, version 0.1.0. No trained production checkpoint or externally
validated real-world benchmark is supplied. The baseline trains locally from a
fictional fixture; transformer training is implemented but no performance is claimed.

## Intended task
Single-label classification of explicitly expressed work, study, exercise, food,
leisure, social, or other activity. Inputs may be eligible posts, comments or profile
text. Outputs express model associations with words, not proof of activities.

## Training and evaluation
TF-IDF unigrams/bigrams + class-balanced logistic regression. Optional DistilBERT
fine-tuning uses the same class mapping and separate validation authors.
Default author-grouped holdout, subject-cluster bootstrap, confusion matrix,
probability diagnostics and optional abstention. See docs/evaluation.md.

## Limitations
English toy templates overlap across subjects. Domain shift, quoted statements,
negation, sarcasm, multiple activities and profile interests can invalidate
predictions. Confidence scores are not guaranteed calibrated. No evidence supports
clinical, personality, physiological or protected-trait inference.

## Artifacts and security
Local joblib artifacts contain vocabulary and use pickle serialization. Load only
trusted artifacts. Do not publish a checkpoint trained on real text without a
memorization and privacy review. Record dataset, package versions and seed in the
generated manifest. Supply a new model card for any real-data experiment.
