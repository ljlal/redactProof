import pymupdf
import pytest

from redactor import (
    count_matches,
    redact_pdf,
    redact_pdf_many,
    verify_redaction
)


def make_test_pdf():
    """Generate a fictional PDF for automated tests."""
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 110), "Name: Johnny Lee")
        page.insert_text((72, 135), "Email: johnny.lee@example.com")
        page.insert_text((72, 160), "Backup: johnny.lee@example.com")
        return doc.tobytes()


def test_single_redaction():
    original = make_test_pdf()

    assert count_matches(original, "Johnny Lee") == 1

    output = redact_pdf(original, "Johnny Lee")

    assert verify_redaction(output, "Johnny Lee")
    assert count_matches(output, "johnny.lee@example.com") == 2


def test_multiple_matches():
    original = make_test_pdf()

    assert count_matches(original, "johnny.lee@example.com") == 2

    output = redact_pdf(original, "johnny.lee@example.com")

    assert count_matches(output, "johnny.lee@example.com") == 0
    assert count_matches(output, "Johnny Lee") == 1


def test_no_match():
    original = make_test_pdf()

    assert count_matches(original, "not_found") == 0

    with pytest.raises(ValueError, match="No matching text found"):
        redact_pdf(original, "not_found")


def test_empty_target():
    original = make_test_pdf()

    with pytest.raises(ValueError, match="Target text cannot be empty"):
        redact_pdf(original, "   ")


def test_multiple_targets_in_one_pass():
    original = make_test_pdf()

    output = redact_pdf_many(
        original,
        ["Johnny Lee", "johnny.lee@example.com"]
    )

    assert count_matches(output, "Johnny Lee") == 0
    assert count_matches(output, "johnny.lee@example.com") == 0

    with pymupdf.open(stream=output, filetype="pdf") as doc:
        assert "Name:" in doc[0].get_text()


def test_missing_target_blocks_operation():
    original = make_test_pdf()

    with pytest.raises(ValueError, match="No matching text found"):
        redact_pdf_many(
            original,
            ["Johnny Lee", "not_found@example.com"]
        )
