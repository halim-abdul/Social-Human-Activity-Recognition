"""Transparent TF-IDF baseline with a selective prediction interface."""
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .privacy import redact

def baseline(seed=42):
    return Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=redact, lowercase=True,
                                 ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ("classifier", LogisticRegression(C=2.0, max_iter=1000, random_state=seed,
                                          class_weight="balanced")),
    ])

def predict_selective(model, texts, threshold=0.5):
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must lie in [0,1]")
    probabilities = model.predict_proba(list(texts))
    best = probabilities.argmax(axis=1)
    return [dict(label=str(model.classes_[i]) if p[i] >= threshold else "abstain",
                 confidence=float(p[i]), probabilities={
                     str(c): float(q) for c, q in zip(model.classes_, p)})
            for i, p in zip(best, probabilities)]

def explain_linear(model, text, top_k=10):
    """Exact logit contributions including signed unigram/bigram features.

    Contributions plus intercept equal the selected class logit. These explain
    model associations; they do not establish a causal effect.
    """
    vector = model["tfidf"].transform([text])
    scores = np.asarray(model.decision_function([text]))
    if model["classifier"].coef_.shape[0] == 1:
        raise ValueError("This explanation requires a multiclass model")
    selected = int(scores[0].argmax())
    weights = model["classifier"].coef_[selected]
    contributions = vector.toarray()[0] * weights
    names = model["tfidf"].get_feature_names_out()
    indices = np.flatnonzero(contributions)
    indices = sorted(indices, key=lambda i: abs(contributions[i]), reverse=True)
    return {"label": str(model.classes_[selected]),
            "intercept": float(model["classifier"].intercept_[selected]),
            "logit": float(scores[0, selected]),
            "contribution_sum": float(contributions.sum()),
            "features": [{"feature": str(names[i]), "contribution": float(contributions[i])}
                         for i in indices[:top_k]]}
