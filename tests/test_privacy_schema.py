import pytest
from socialhar.synthetic import generate
from socialhar.schema import validate
from socialhar.privacy import redact, pseudonymize, prepare

def test_contact_redaction():
    text = redact("Ask @sample via a.b@example.org or https://example.org at +49 123 4567890")
    assert all(value not in text for value in ["@sample", "example.org", "123"])
    assert "[EMAIL]" in text and "[PHONE]" in text

def test_pseudonyms_are_keyed():
    assert pseudonymize("a", "x" * 32) == pseudonymize("a", "x" * 32)
    assert pseudonymize("a", "x" * 32) != pseudonymize("a", "y" * 32)
    with pytest.raises(ValueError):
        pseudonymize("a", "short")

@pytest.mark.parametrize("column,value", [
    ("permission", "public"), ("label", "diagnosis"), ("source_type", "dm"),
    ("text", ""), ("timestamp", "2026-01-01"), ("subject_id", None)])
def test_validation_rejects_ineligible_rows(column, value):
    frame = generate(10)
    frame.loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        validate(frame)

def test_duplicate_ids_fail():
    frame = generate(10)
    frame.loc[1, "record_id"] = frame.loc[0, "record_id"]
    with pytest.raises(ValueError):
        validate(frame)

def test_preparation_removes_repeated_normalized_text():
    frame = generate(10)
    frame.loc[1, "text"] = frame.loc[0, "text"]
    assert len(prepare(validate(frame))) == len(frame) - 1
