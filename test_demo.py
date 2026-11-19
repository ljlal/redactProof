
from demo import make_unsafe_masked_pdf
from redactor import count_matches, redact_pdf

def test_visual_masking_is_not_redaction():
    original = make_unsafe_masked_pdf()

    # The black rectangle did NOT remove the text
    assert count_matches(original, "Johnny Lee") == 1

    # Actual redaction should remove searchable text
    output = redact_pdf(original, "Johnny Lee")
    assert count_matches(output, "Johnny Lee") == 0
