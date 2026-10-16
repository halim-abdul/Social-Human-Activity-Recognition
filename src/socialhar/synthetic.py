"""Deterministic fictional examples. No social platform data is downloaded."""
from datetime import datetime, timedelta, timezone
import pandas as pd

TEMPLATES = {
    "work": ["I am reviewing the project budget", "I just finished a client meeting",
             "Working on a presentation for my team", "I am preparing a sales report"],
    "study": ["I am revising algebra for tomorrow", "Reading my lecture notes now",
              "I just solved a calculus exercise", "Studying vocabulary for my language class"],
    "exercise": ["I went running in the park", "Finished a strength workout today",
                 "I am cycling along the river", "I just completed a yoga session"],
    "food": ["I am cooking vegetable soup", "Just baked bread for dinner",
             "I am preparing a pasta lunch", "Eating breakfast before my day begins"],
    "leisure": ["I am watching a comedy tonight", "I just played a new video game",
                "Reading a novel on the sofa", "Listening to my favorite music album"],
    "social": ["I met my friends for a chat", "I am visiting my cousin this afternoon",
               "We are celebrating a birthday together", "I called a friend to catch up"],
    "other": ["The sky looks cloudy", "What does this phrase mean",
              "There is a new update available", "I have no activity to report"],
}
def generate(n_subjects=70, seed=42):
    if n_subjects < 10:
        raise ValueError("Use at least ten synthetic subjects")
    rows = []
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    contexts = ["at home", "this morning", "after lunch", "before sunset",
                "on Monday", "during the weekend", "for a change", "as planned"]
    for subject in range(n_subjects):
        for j, (label, phrases) in enumerate(TEMPLATES.items()):
            phrase = phrases[(subject + j) % len(phrases)]
            context = contexts[(subject // len(phrases) + j) % len(contexts)]
            # Numbered fictional diary tags permit exact reproducibility and dedup auditing.
            text = f"{phrase} {context}. Diary entry {subject * 7 + j}."
            rows.append(dict(record_id=f"r{len(rows):05d}", subject_id=f"fictional-{subject:03d}",
                             text=text, timestamp=(start + timedelta(
                                 days=subject, hours=(subject * 13 + j * 3 + seed) % 24)).isoformat(),
                             label=label, source_type=["post", "profile", "comment"][(subject + j) % 3],
                             permission="synthetic", provenance="socialhar-generator-v1"))
    return pd.DataFrame(rows)
