# Data and eligibility

The bundled [activities.csv](synthetic/activities.csv) contains 490 fictional English
records from 70 fictional subjects. Seven labels have 70 records each.
Source types are post/profile/comment. Nothing was scraped or collected from people.
Regenerate with `python scripts/generate_data.py`; default seed is 42.

## Required schema

| Field | Meaning |
|---|---|
| record_id | Unique record key, no platform URL |
| subject_id | Project-local pseudonym; grouping key |
| text | Text eligible for research, <=10,000 characters |
| timestamp | ISO timestamp with explicit timezone |
| label | work, study, exercise, food, leisure, social, other |
| source_type | post, profile, comment |
| permission | synthetic, consented, public_reviewed |
| provenance | Source and reuse-review reference |

public_reviewed is an internal eligibility assertion after a documented review of
reuse rights, platform restrictions, and the research protocol. The validator
checks the assertion, not the underlying permission. Public visibility alone does
not settle reuse rights. Never commit real raw social-media text to this repository.

See [datasheet](datasheet.md) and [annotation guide](../docs/annotation.md).
