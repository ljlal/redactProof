# RedactProof
A privacy-first PDF redaction and verification tool.

Bulit for SafeSpace Hacks 2026.

## Overview

RedactProof is a Python application that helps users remove selected sensitive text from PDF documents.

Unlike simply covering text with black rectangles, RedactProof uses PDF redaction operation to remove from selected regions.

## Features (v0.3)

###PDF Redaction
- Upload and process PDF documents
- Manually search and redact selected text
- Automatically detect email addresses and selected phone number formats
- Select which detected information to redact
- Download the processed PDF

### Verification & Preview
- Verify whether selected text remains searchable
- Compare original and redacted PDF pages
- Generate a verification report
- Display before-and-after match counts
- Warn about possible privacy risks in images, metadata, and attachments

### Testing
- Automated tests using pytest
- Single and multiple redaction tests
- Invalid input and error handing tests
- Verification report and PDF preview tests

## Tech Stack

- Python
- Streamlit
- PyMuPDF

## Getting Started

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```
## Running Tests

Install development dependencies:

```bash
pip install pytest
```

Run all automated tests:

```bash
python -m pytest -v
```

The test suite covers redaction, detection,
verification, and selected error scenarios.

## Limitations

RedactProof is an experimental prototype develoed for SafeSpace Hacks 2026.

- Automatic detection uses pattern matching and may produce false positives or miss sensitive information.
- Phone number detection supports limited formats.
- Verification checks selected searchable page text, not the complete contents of a PDF.
- Image, metadata, attachments, and other PDF structures may still contain sensitive infromation.
- Scanned documents are not fully supported.
- Users should manually review exported documents.

RedactProof does not guarantee complete removal of all sensitive information.

Use fictional or synthetic data for testing.

## Development

Created for SafeSpace Hacks 2026.