"""Exploratory topic factors fitted on training text only."""
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from .privacy import redact

def fit_topics(texts, n_topics=5, seed=42):
    vectorizer = TfidfVectorizer(preprocessor=redact, stop_words="english",
                                 min_df=2, max_df=.95)
    matrix = vectorizer.fit_transform(texts)
    if n_topics < 1 or n_topics > min(matrix.shape):
        raise ValueError("Topic count exceeds available samples or vocabulary")
    model = NMF(n_components=n_topics, init="nndsvda", random_state=seed, max_iter=500)
    weights = model.fit_transform(matrix)
    terms = vectorizer.get_feature_names_out()
    topics = [[str(terms[i]) for i in component.argsort()[-10:][::-1]]
              for component in model.components_]
    return vectorizer, model, weights, topics
