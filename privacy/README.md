# Privacy and responsible research

## Data flow
Accept only project-authorized consented data, documented public reuse, or synthetic
records. Keep a separate provenance register. Validate eligibility before training.
Redact contact patterns and manually audit contextual identifiers. Use keyed
pseudonyms when grouping real subjects, and store the key outside the dataset.

Regex replacement is a minimization baseline, not anonymization. Models can retain
training vocabulary and memorize text. Keep checkpoints, split identifiers and
raw inputs access-controlled; do not commit them. Prediction exports omit text
and subject IDs, but record IDs can still be linkable inside a project.

## Access, retention and withdrawal
Record an owner, purpose, retention deadline and access list for every real corpus.
Keep the pseudonym-to-source mapping separately. Resolve deletion requests through
that controlled mapping; delete raw rows, processed copies and cached exports,
then assess retraining and backup expiry. This repository does not automate deletion
across external systems.

## Reporting
Temporal cells require at least five distinct subjects by default. Suppression is
not differential privacy: overlapping aggregates may permit reconstruction. Do not
publish repeated narrow slices or person-level timelines. No identity resolution,
covert surveillance, high-stakes scoring or psychological diagnosis is supported.
