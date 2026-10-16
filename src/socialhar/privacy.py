"""Conservative text redaction; regexes are not a complete anonymizer."""
import hashlib
import hmac
import re

PATTERNS = [
    (r"https?://\S+", "[URL]"),
    (r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "[EMAIL]"),
    (r"(?<!\w)@[A-Za-z0-9_]+", "[HANDLE]"),
    (r"(?<!\w)\+?\d[\d ().-]{7,}\d(?!\w)", "[PHONE]"),
]

def redact(text):
    for pattern, replacement in PATTERNS:
        text = re.sub(pattern, replacement, text)
    return " ".join(text.split())

def pseudonymize(subject_id, secret):
    if len(secret.encode()) < 32:
        raise ValueError("Use a secret of at least 32 bytes, stored outside the dataset")
    return hmac.new(secret.encode(), subject_id.encode(), hashlib.sha256).hexdigest()[:24]

def prepare(frame):
    """Drop exact duplicate normalized text before any train/test allocation."""
    out = frame.copy()
    out["text"] = out.text.map(redact)
    return out.drop_duplicates("text").reset_index(drop=True)
