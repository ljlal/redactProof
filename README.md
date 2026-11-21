# RedactProof

**A Privacy-First PDF Redaction & Verification Tool**

Bulit for **SafeSpace Hacks 2026**.


## Overview

RedactProof is a Python-based application designed to help users identify, redact, and verify selected sensitive information in PDF documents.

Simply cover sensitive text with black rectangles may leave the underlying information accessible. RedactProof uses PyMuPDF's redaction operations to remove content from selected page regions and performs limited verification on the exported document.

The project focuses on four principles:

- **Detection:** Identify potentially sensitive information.
- **User Control:** Let users choose what to remove.
- **Redaction:** Apply PDF redaction operations.
- **Verification:** Check the result and communicate limitations.

## Features (v0.5)

### 1. PDF Redaction

- Upload PDF documents up to 10 MB.
- Manually search for and redact selected text.
- Users can automatically detect email addresses and selected international phone number formats.
- Review and select detected information before redaction.
- Process multiple selected targets in one operation.
- Download the resulting PDF document.

### 2. Security Hardening

- Check that every selected target can be located before redaction.
- Reject operations when selected targets cannot be found.
- Verify selected targets after exporting the modified PDF.
- Avoid reporting success when the text verification fails.

### 3. Verification & Preview

- Compare original and redacted PDF pages side by side.
- Generate a verification report.
- Display before-and-after text match counts.
- Report limited page-text verification results.
- Warn when selected information is also found in checked PDF metadata.
- Highlight pages containing images or no extractable text.
- Warn about embedded attachments.

### 4. Automated Testing

RedactProof uses pytest to test:

- Single-target redaction
- Multiple matches
- Multiple targets in one operation
- Missing and empty targets
- Automatic email and phone detection
- PDF preview generation
- Verification reports
- Selected metadata and failure scenarios

### 5. Automated Testing

- Automated tests using pytest.

- Redaction and sensitive information detection tests.

- Invalid input and error handling tests.

- Verification report and PDF preview tests.

- Unsafe masking demonstration tests.

## Tech Stack

- **Python:** Core application logic
- **Streamlit:** Web interface
- **PyMuPDF:** PDF processing, redaction, and rendering
- **Regular Expressions:** Pattern-based sensitive information detection
- **pytest:** Automated testing

## Project Structure

- `app.py` — Streamlit user interface and workflow
- `detector.py` — Pattern-based sensitive information detection
- `redactor.py` — PDF text search, redaction, and verification
- `report.py` — Verification reports and PDF preview rendering
- `test_detector.py` — Detection tests
- `test_redactor.py` — Redaction tests
- `test_report.py` — Report and preview tests
- `requirements.txt` — Application dependencies

## Getting Started

### 1. Clone the Repository

`git clone https://github.com/ljlal/redactProof.git`

`cd redactProof`

### 2. Create a Virtual Environment

`python -m venv .venv`

### 3. Install Dependencies

On Windows PowerShell:

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

### 4. Run RedactProof

`.\.venv\Scripts\python.exe -m streamlit run app.py`

Open `http://localhost:8501` in your browser.

## How to Use

1. Download the built-in fictional test PDF or upload a suitable PDF.
2. Enter text manually or review automatically detected information.
3. Select the information to remove.
4. Confirm and execute the redaction.
5. Review the verification report and before-and-after PDF previews.
6. Download the processed document if the result meets your needs.

## Running Tests

Install pytest:

`python -m pip install pytest`

Run the test suite:

`python -m pytest -v`

The automated tests cover core processing, detection, verification, and selected failure scenarios. Passing tests do not establish that every PDF can be safely processed.

## Security & Limitations

**RedactProof is an experimental prototype, not a complete PDF sanitization or privacy certification solution.**

### Limitations

RedactProof is an experimental prototype developed for SafeSpace Hacks 2026.
- Automatic detection may produce false positives or miss sensitive information.
- Phone number detection supports limited formats.
- Verification checks selected searchable page text, not the complete contents of a PDF.
- Images, metadata, annotations, forms, and attachments may still contain sensitive information.
- Scanned documents are not fully supported.
- Redaction may affect nearby or overlapping content.
- Users should manually review exported documents.
RedactProof does not guarantee complete removal of all sensitive information.
Use fictional or synthetic data for testing.

## Development & Credits

RedactProof was developed for **SafeSpace Hacks 2026**.

Development includes Python implementation, PDF processing, automated testing, and iterative improvements to verification and user experience.

AI assistance from ChatGPT was used during development for code scaffolding, debugging guidance, and documentation. 

Third-party tools and libraries include Streamlit, PyMuPDF, and pytest.

## Future Improvements

- More reliable detection across complex PDF layouts
- Expanded phone number and identifier support
- Improved handling of scanned documents
- More comprehensive PDF structure and metadata inspection
- Additional regression and security tests
- Further user interface improvements

---

**RedactProof — Detect. Review. Redact. Verify.**