# Synthetic dataset datasheet

## Motivation and composition
A reproducible software fixture for testing data contracts, leakage controls,
training, inference and reports. 490 records, 70 subjects, seven balanced labels.
No real people, identities, demographics, locations, or consent claims.

## Creation
First-person English templates combined with eight context phrases and unique
fictional diary numbers. Each subject has exactly one record per label.
Hours and source type are deterministic functions of subject, label and seed.
The generator is in src/socialhar/synthetic.py. License: MIT, as project-authored text.

## Intended use
Unit tests, tutorials and smoke tests. No external validity, psychological validity,
population representativeness or evidence of transformer superiority is implied.
The diary number is a synthetic artifact; exclude it in real research and test
sensitivity to template overlap and annotation artifacts.

## Leakage and bias
Exact texts are unique, but templates overlap across subjects and partitions.
An author-disjoint split does not remove template leakage. Balanced English
sentences do not model sarcasm, dialect, multilingual text, missingness, platform
selection bias, or ambiguity. Results should never be called a real-world benchmark.

## Maintenance and deletion
Regenerate from source. There are no human records to withdraw. For external data,
maintain a separate eligible-data register, withdrawal process and retention plan.
Do not reuse synthetic performance estimates in a deployment model card.
