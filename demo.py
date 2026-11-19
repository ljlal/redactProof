import pymupdf

def make_unsafe_masked_pdf() -> bytes:
    """Create a fictional PDF with visually hidden text."""

    with pymupdf.open() as doc:
        page = doc.new_page()

        page.insert_text(
            (72, 72),
            "Unsafe PDF Masking Demo",
            fontsize=18
        )

        page.insert_text(
            (72, 116),
            "Name: Johnny Lee",
            fontsize=12
        )

        page.insert_text(
            (72, 160),
            "A black rectangle only hides the name visually."
        )

        #locate the text without deleting it
        matches = page.search_for("Johnny Lee")

        if len(matches) != 1:
            raise ValueError("Demo target not found.")

        #draw a black rectangle ON TOP of the text
        page.draw_rect(
            matches[0],
            color=(0, 0, 0),
            fill=(0, 0, 0),
            overlay=True
        )

        return doc.tobytes()
