# RedactProof
A privacy-first PDF redaction and verification tool.

Bulit for SafeSpace Hacks 2026.

## Overview

RedactProof is a Python application that helps users remove selected sensitive text from PDF documents.

Unlike simply covering text with black rectangles, RedactProof uses PDF redaction operation to remove from selected regions.

## Features (v0.1)

- Upload a PDF document
- Search for specific text
- Remove matching text regions
- Reopen and verify the exported PDF
- Download the redacted document
- Generate a fictional PDF for testing

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

## Limitations

This is an early prototype.

Verification currently checks whether specified text remains
searchable in the exported PDF's page text.

It does not provide complete protection against sensitive
information in images, metadata, attachments, or other PDF
structures. Scanned documents are not supported.

Do not use real sensitive documents for testing.

## Development

Created for SafeSpace Hacks 2026.