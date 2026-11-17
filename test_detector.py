import pymupdf
from detector import detect_sensitive_info

def make_test_pdf(lines):
    with pymupdf.open() as doc:
        page = doc.new_page()

        for index, line in enumerate(lines):
            y = 72 + index * 25
            page.insert_text((72, y), line)

        return doc.tobytes()


def test_detect_email():
    pdf = make_test_pdf([
        "Email: johnny.lee@example.com",
        "Backup: johnny.lee@example.com"
    ])

    results = detect_sensitive_info(pdf)

    assert len(results) == 1
    assert results[0]["kind"] == "Email"
    assert results[0]["count"] == 2

def test_detect_phone():
    pdf = make_test_pdf([
        "Phone: +64 21 123 4567"
    ])

    results = detect_sensitive_info(pdf)

    assert len(results) == 1
    assert results[0]["kind"] == "Phone"
    assert results[0]["value"] == "+64 21 123 4567"