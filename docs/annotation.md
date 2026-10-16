# Annotation protocol

The target is the activity explicitly expressed in a text, not verified behavior.
Read the entire text. Assign one dominant activity; use other if there is no
unambiguous dominant class. A future production extension could use multi-label
annotation, but the present implementation is single-label.

| Label | Include | Boundary |
|---|---|---|
| work | Employment or professional tasks | Studying for a class is study |
| study | Coursework, exams, structured learning | Reading fiction for fun is leisure |
| exercise | Running, fitness, sports participation | Watching sports is leisure |
| food | Preparing or consuming meals | Employment as a chef needs contextual review |
| leisure | Entertainment and hobbies | Explicit interaction with friends is social |
| social | Visiting, chatting, shared celebrations | Merely mentioning a person is insufficient |
| other | Unsupported, ambiguous, mixed, negated or hypothetical activity | Do not guess |

Examples: "I went running" -> exercise. "I did not go running" -> other.
"I wish I could run" -> other. "I ran and cooked" -> other unless an agreed
dominance rule applies. Baseline models may fail these examples; they are challenge
cases for an external evaluation, not solved claims.

Use two independent annotators on a pilot set. Record rationales and adjudicate
disagreements after computing Cohen's kappa and raw agreement. Do not disclose
user handles to annotators. Report annotation guidelines, disagreement rates and
class frequencies separately for posts, comments and profiles. Profiles may
express interests or occupations rather than current activities: annotate only
supported text and evaluate this domain separately.
