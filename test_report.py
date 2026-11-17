
import pymupdf
import pytest

from redactor import redact_pdf
from report import (
    render_pdf_page,
    build_verification_report
)


def make_test_pdf():
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 72), "Name: Johnny Lee")
        page.insert_text((72, 100), "Email: johnny@example.com")
        return doc.tobytes()

def test_verification_report():
    original = make_test_pdf()
    output = redact_pdf(original, "Johnny Lee")

    report = build_verification_report(
        original, output, ["Johnny Lee"]
    )

    result = report["results"][0]

    assert result["before"] == 1
    assert result["after"] == 0
    assert result["text_passed"] is True
    assert report["page_count"] == 1


def test_pdf_preview():
    original = make_test_pdf()

    image = render_pdf_page(original, 0)

    assert image.startswith(b"\x89PNG\r\n\x1a\n")


def test_invalid_page_number():
    original = make_test_pdf()

    with pytest.raises(ValueError):
        render_pdf_page(original, 100)


def test_missing_target_cannot_pass():
    original = make_test_pdf()
    output = redact_pdf(original, "Johnny Lee")

    report = build_verification_report(
        original, output, ["Not Present"]
    )

    assert report["results"][0]["text_passed"] is False


def test_metadata_warning():
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 72), "Johnny Lee")
        doc.set_metadata({"title": "Johnny Lee"})
        original = doc.tobytes()

    output = redact_pdf(original, "Johnny Lee")

    report = build_verification_report(
        original, output, ["Johnny Lee"]
    )

    assert report["results"][0]["metadata_match"] is True
