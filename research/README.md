# Research protocol

## Primary question
Can an explicitly supervised text model recognize self-described activity categories
in eligible text from previously unseen authors?

## Predeclared comparison
Majority-class control, TF-IDF logistic regression and a fine-tuned transformer.
Primary measure: macro-F1 on held-out authors. Secondary measures: per-class recall,
log loss, coverage, selective accuracy and calibration. Use the same frozen test
subjects for comparisons and paired subject-cluster uncertainty estimation.

## Study stages
1. Eligibility and sampling review; define target population and reuse rights.
2. Dual-annotator pilot with disagreements and revised boundaries documented.
3. Deduplication and author-disjoint train/validation/test allocation.
4. Baseline reproduction and transformer tuning on validation only.
5. Negation, hypothetical, sarcasm, multilingual and profile-text challenge sets.
6. Final test, source-type analysis and limitations, followed by a reproducible report.

## Open experiments
Template-disjoint synthetic split; near-duplicate clustering; multi-label extension;
calibration with validation-only fitting; cross-platform transfer; hierarchical
analysis for repeated observations. These are research extensions, not implemented
performance claims.

## What would falsify the claim?
Poor recall on ambiguous classes, collapse under template-disjoint evaluation,
large unseen-platform degradation, or confidence that stays high on unsupported
text. Report failures and abstentions. Do not hide low-support classes.
