
import pymupdf
from redactor import count_matches


def render_pdf_page(pdf_data: bytes, page_number: int = 0) -> bytes:
    """Render one PDF page as a PNG image."""

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:
        if doc.needs_pass:
            raise ValueError("Password-protected PDF.")

        if not 0 <= page_number < doc.page_count:
            raise ValueError("Invalid page number.")

        page = doc[page_number]

        # Limit image size to avoid excessive memory usage.
        longest_side = max(page.rect.width, page.rect.height)
        if longest_side <= 0:
            raise ValueError("Invalid page dimensions.")

        zoom = min(1.5, 1400 / longest_side)

        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(zoom, zoom),
            alpha=False
        )

        return pixmap.tobytes("png")


def build_verification_report(
    original: bytes,
    output: bytes,
    targets: list[str]
) -> dict:
    """Generate a limited PDF redaction verification report."""

    targets = list(dict.fromkeys(
        value.strip() for value in targets if value.strip()
    ))

    if not targets:
        raise ValueError("At least one target is required.")

    with pymupdf.open(stream=output, filetype="pdf") as doc:
        if doc.needs_pass:
            raise ValueError("Password-protected PDF.")

        page_count = doc.page_count
        textless_pages = []
        image_pages = []

        for index, page in enumerate(doc):
            if not page.get_text("text").strip():
                textless_pages.append(index + 1)

            if page.get_image_info():
                image_pages.append(index + 1)

        attachment_count = doc.embfile_count()

        metadata = doc.metadata or {}
        metadata_text = " ".join(
            str(value) for value in metadata.values() if value
        )
        metadata_text += " " + doc.get_xml_metadata()
        metadata_text = metadata_text.casefold()

    results = []

    for target in targets:
        before = count_matches(original, target)
        after = count_matches(output, target)

        results.append({
            "target": target,
            "before": before,
            "after": after,
            "text_passed": before > 0 and after == 0,
            "metadata_match": target.casefold() in metadata_text
        })

    return {
        "page_count": page_count,
        "results": results,
        "textless_pages": textless_pages,
        "image_pages": image_pages,
        "attachment_count": attachment_count
    }
