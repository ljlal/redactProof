
import pymupdf


def count_matches(pdf_data: bytes, target: str) -> int:
    """Count matching searchable text regions."""

    target = target.strip()

    if not target:
        return 0

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:
        if doc.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        return sum(len(page.search_for(target)) for page in doc)


def verify_redaction(pdf_data: bytes, target: str) -> bool:
    """Check whether selected text remains searchable."""

    if not target.strip():
        raise ValueError("Target text cannot be empty.")

    return count_matches(pdf_data, target) == 0


def redact_pdf_many(pdf_data: bytes, targets: list[str]) -> bytes:
    """Redact multiple targets in one PDF processing operation."""

    targets = list(dict.fromkeys(
        value.strip()
        for value in targets
        if value and value.strip()
    ))

    if not targets:
        raise ValueError("Target text cannot be empty.")

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:

        if doc.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        #check all targets before editing
        counts = {value: 0 for value in targets}

        for page in doc:
            for value in targets:
                counts[value] += len(page.search_for(value))

        missing = [
            value for value, count in counts.items()
            if count == 0
        ]

        if missing:
            raise ValueError(
                "No matching text found for one or more targets."
            )

        #mark every selected target
        for page in doc:
            has_redactions = False

            for value in targets:
                matches = page.search_for(value)

                for rect in matches:
                    page.add_redact_annot(
                        rect,
                        fill=(0, 0, 0)
                    )
                    has_redactions = True

            # apply all marks on this page together
            if has_redactions:
                page.apply_redactions()

        output = doc.tobytes(
            garbage=4,
            deflate=True
        )

    #Verify every selected target
    for value in targets:
        if not verify_redaction(output, value):
            raise ValueError(
                "Redaction verification failed."
            )

    return output

def redact_pdf(pdf_data: bytes, target: str) -> bytes:
    """Single-target interface, kept for backwards compatibility."""

    return redact_pdf_many(pdf_data, [target])
