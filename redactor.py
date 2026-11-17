
import pymupdf


def count_matches(pdf_data: bytes, target: str) -> int:
    """Count matching text regions in a PDF."""

    target = target.strip()

    if not target:
        return 0

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:

        if doc.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        count = 0

        for page in doc:
            matches = page.search_for(target)
            count += len(matches)

        return count


def verify_redaction(pdf_data: bytes, target: str) -> bool:
    """Check whether target text is still searchable."""

    if not target.strip():
        raise ValueError("Target text cannot be empty.")

    return count_matches(pdf_data, target) == 0


def redact_pdf(pdf_data: bytes, target: str) -> bytes:
    """Remove matching page text and verify the output."""

    target = target.strip()

    if not target:
        raise ValueError("Target text cannot be empty.")

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:

        if doc.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        total_matches = 0

        for page in doc:
            matches = page.search_for(target)
            total_matches += len(matches)

            for rect in matches:
                page.add_redact_annot(
                    rect,
                    fill=(0, 0, 0)
                )

            if matches:
                page.apply_redactions()

        if total_matches == 0:
            raise ValueError("No matching text found.")

        output = doc.tobytes(
            garbage=4,
            deflate=True
        )

    if not verify_redaction(output, target):
        raise ValueError("Redaction verification failed.")

    return output
