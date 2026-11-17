
import re
import pymupdf

# Match common email address patterns
EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])"
)

# Match selected international phone formats
# Examples: +64 21 123 4567, +1 202-555-0123
PHONE_PATTERN = re.compile(
    r"(?<!\w)\+\d{1,3}(?:[ .-]?\d{2,4}){2,4}(?!\w)"
)


def detect_sensitive_info(pdf_data: bytes) -> list[dict]:
    """To find possible emails and international phone numbers."""

    found = {}

    with pymupdf.open(stream=pdf_data, filetype="pdf") as doc:

        if doc.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        for page in doc:
            text = page.get_text("text")

            patterns = [
                ("Email", EMAIL_PATTERN),
                ("Phone", PHONE_PATTERN)
            ]

            for kind, pattern in patterns:
                for match in pattern.finditer(text):

                    value = match.group(0)

                    if kind == "Phone":
                        digits = len(re.sub(r"\D", "", value))

                        if not (8 <= digits <= 15):
                            continue

                    key = (kind, value)
                    found[key] = found.get(key, 0) + 1

    results = []

    for (kind, value), count in found.items():
        results.append({
            "kind": kind,
            "value": value,
            "count": count
        })

    return results
