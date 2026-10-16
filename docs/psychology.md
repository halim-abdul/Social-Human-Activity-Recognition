# Psychology-informed analysis

Supported Python tools:

| Tool | Implemented use | Interpretation limit |
|---|---|---|
| NLTK VADER | Expressed sentiment scores | Text valence, not mood or diagnosis |
| scikit-learn | Cohen kappa for paired annotation | Agreement depends on prevalence |
| Pingouin | Independent-subject Welch t-test | Predeclared group comparison only |
| statsmodels (optional extra) | Available for study extensions | No mixed-effects implementation claimed |
| SciPy | Scientific computing dependency | No physiological signals in text |

Install with `python -m pip install -e ".[psychology]"`.
Download the licensed NLTK resource explicitly:
`python -m nltk.downloader vader_lexicon`.
Notebook 08 opt-in: set SOCIALHAR_RUN_PSYCHOLOGY=1.

The framework does not infer personality, mental-health conditions, protected
attributes or physiological state. Physiological libraries such as NeuroKit are
not included because this dataset contains no ECG, EDA or other physiological
signals. Repeated posts are not independent participants: aggregate within subject
or use a study-appropriate hierarchical model. Predeclare effect sizes, uncertainty,
confounders and multiplicity correction before interpreting real comparisons.

Sentiment is language/domain dependent. Never equate negative language with a
clinical condition or a stable trait. Obtain independent construct validation if
designing a new psychological measure.
