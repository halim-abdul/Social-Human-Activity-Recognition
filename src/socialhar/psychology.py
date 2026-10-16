"""Psychology research helpers: expressed sentiment and annotation agreement."""
def sentiment_scores(texts):
    """VADER scores language valence, not a person's mental health.

    Requires: python -m nltk.downloader vader_lexicon
    No automatic downloads occur inside this function.
    """
    from nltk.sentiment import SentimentIntensityAnalyzer
    from .privacy import redact
    analyzer = SentimentIntensityAnalyzer()
    return [analyzer.polarity_scores(redact(t)) for t in texts]

def annotation_agreement(rater_a, rater_b):
    from sklearn.metrics import cohen_kappa_score
    if len(rater_a) != len(rater_b) or len(rater_a) == 0:
        raise ValueError("Paired, nonempty annotations required")
    return float(cohen_kappa_score(rater_a, rater_b))

def compare_subject_scores(frame, score, group):
    """Welch test via Pingouin; one independent observation per subject required."""
    import pingouin as pg
    if frame.subject_id.duplicated().any():
        raise ValueError("Aggregate repeated observations within each subject first")
    levels = frame[group].dropna().unique()
    if len(levels) != 2:
        raise ValueError("Exactly two comparison groups required")
    a, b = [frame.loc[frame[group] == level, score].dropna() for level in levels]
    if min(len(a), len(b)) < 3:
        raise ValueError("At least three subjects per group required")
    return pg.ttest(a, b, paired=False, correction=True)
