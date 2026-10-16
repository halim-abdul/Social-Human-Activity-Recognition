import numpy as np
import pytest
from socialhar.synthetic import generate
from socialhar.schema import validate, LABELS
from socialhar.privacy import prepare
from socialhar.split import grouped_split, chronological_split
from socialhar.models import baseline, predict_selective, explain_linear
from socialhar.evaluation import evaluate, cluster_bootstrap_f1, reliability
from socialhar.temporal import aggregate_activity, posting_entropy
from socialhar.topics import fit_topics
from socialhar.cli import run

@pytest.fixture
def partitions():
    return grouped_split(prepare(validate(generate(35))))

def test_group_split_is_disjoint_and_deterministic(partitions):
    a, b = partitions
    assert not set(a.subject_id) & set(b.subject_id)
    assert len(a) + len(b) == 245
    assert set(a.label) == set(LABELS)
    assert a.record_id.tolist() == grouped_split(prepare(validate(generate(35))))[0].record_id.tolist()

def test_model_explanation_reconstructs_logit(partitions):
    a, b = partitions
    model = baseline().fit(a.text, a.label)
    report = evaluate(model, b)
    assert 0 <= report["macro_f1"] <= 1
    explanation = explain_linear(model, b.iloc[0].text)
    assert np.isclose(explanation["logit"],
                      explanation["intercept"] + explanation["contribution_sum"])
    assert all(p["label"] == "abstain" for p in predict_selective(model, b.text, 1))
    assert all(p["label"] != "abstain" for p in predict_selective(model, b.text, 0))
    with pytest.raises(ValueError):
        predict_selective(model, b.text, -1)

def test_metrics_and_topics(partitions):
    a, b = partitions
    model = baseline().fit(a.text, a.label)
    ci = cluster_bootstrap_f1(b, model.predict(b.text), repeats=20)
    assert 0 <= ci["low"] <= ci["high"] <= 1
    assert 0 <= reliability(b.label, model.predict_proba(b.text), model.classes_)["ece"] <= 1
    _, _, weights, topics = fit_topics(a.text, 3)
    assert weights.shape == (len(a), 3) and len(topics) == 3

def test_aggregate_suppression_and_entropy():
    frame = validate(generate(35))
    assert aggregate_activity(frame, min_subjects=100).empty
    assert np.isclose(posting_entropy([1, 1]), 1)
    with pytest.raises(ValueError):
        posting_entropy([0, 0])
    a, b = chronological_split(frame, "2026-01-15T00:00:00Z")
    assert a.timestamp.max() < b.timestamp.min()

def test_end_to_end_exports(tmp_path):
    report = run(generate(35), tmp_path)
    assert report["scope"] == "synthetic smoke test only"
    assert (tmp_path / "metrics.json").exists()
    assert "text" not in (tmp_path / "predictions.csv").read_text().splitlines()[0]
