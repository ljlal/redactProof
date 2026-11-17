
import hashlib
import pymupdf
import streamlit as st
from redactor import count_matches, redact_pdf
from detector import detect_sensitive_info
from report import render_pdf_page, build_verification_report

st.set_page_config(
    page_title="RedactProof",
    page_icon="🔒",
    layout="wide"
)

st.title("RedactProof")
st.write("Remove sensitive text from your PDFs and verify the result.")
st.caption("Prototype: selectable page text only. Use fictional files for testing.")


# Part 1: Generate a fictional PDF
def make_demo_pdf():
    with pymupdf.open() as doc:
        page = doc.new_page()

        page.insert_text((72, 72), "This is a Demo", fontsize=18)
        page.insert_text((72, 110), "Name: Johnny Lee")
        page.insert_text((72, 135), "Email: johnny.lee@example.com")
        page.insert_text((72, 160), "Backup: johnny.lee@example.com")
        page.insert_text((72, 185), "Phone: +64 21 123 4567")

        return doc.tobytes()

def show_verification_result(original, output, targets, key):
    """Display the report and before/after previews."""

    report = build_verification_report(
        original, output, targets
    )

    st.subheader("Verification Report")

    all_passed = all(
        item["text_passed"]
        for item in report["results"]
    )

    for item in report["results"]:
        st.write(f"**Target:** {item['target']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Before", item["before"])
        col2.metric("After", item["after"])
        col3.metric(
            "Page-text check",
            "PASS" if item["text_passed"] else "FAIL"
        )

        if item["metadata_match"]:
            st.error(
                "The selected text was also found in PDF metadata. "
                "This version does not remove it."
            )

    if all_passed:
        st.success("Selected searchable page-text checks passed.")
    else:
        st.error("One or more page-text checks failed.")

    # Warnings for content not covered by the text check
    if report["textless_pages"]:
        st.warning(
            "Pages without extractable text: "
            f"{report['textless_pages']}. "
            "These may be scans or empty pages."
        )

    if report["image_pages"]:
        st.warning(
            "Images detected on pages: "
            f"{report['image_pages']}. "
            "Image content has not been checked with OCR."
        )

    if report["attachment_count"]:
        st.warning(
            f"{report['attachment_count']} embedded file(s) detected. "
            "Attachments were not inspected or removed."
        )

    st.info(
        "This is a limited verification, not a certificate "
        "that the entire PDF is free of sensitive information."
    )

    st.subheader("Before & After Preview")

    page_number = st.selectbox(
        "Choose a page",
        options=list(range(report["page_count"])),
        format_func=lambda index: f"Page {index + 1}",
        key=f"preview_page_{key}"
    )

    left, right = st.columns(2)

    with left:
        st.write("**Original PDF**")
        st.image(render_pdf_page(original, page_number))

    with right:
        st.write("**Redacted PDF**")
        st.image(render_pdf_page(output, page_number))

st.download_button(
    "Download fictional test PDF",
    data=make_demo_pdf(),
    file_name="demo.pdf",
    mime="application/pdf"
)


# Part 2: Upload PDF and enter text
uploaded = st.file_uploader(
    "1. Upload a PDF",
    type=["pdf"]
)

target = st.text_input(
    "2. Text to remove",
    placeholder="Johnny Lee"
).strip()


# Part 3: Process the uploaded PDF
if uploaded is not None and target:

    raw = uploaded.getvalue()

    if len(raw) > 10 * 1024 * 1024:
        st.error("This prototype supports files up to 10 MB only.")
        st.stop()

    job_key = hashlib.sha256(
        raw + target.encode("utf-8")
    ).hexdigest()

    if st.session_state.get("job_key") != job_key:
        st.session_state["job_key"] = job_key
        st.session_state.pop("result", None)
        st.session_state.pop("confirm", None)

    
    try:
        count = count_matches(raw, target)

        st.info(f"Found {count} matching text regions in the PDF.")

        if count == 0:
            st.warning(
                "No match found. Scanned pages may not have "
                "searchable text."
            )

        else:
            confirmed = st.checkbox(
                f"I reviewed and approve removing all {count} matches.",
                key="confirm"
            )

            if st.button(
                "3. Redact and verify",
                disabled=not confirmed
            ):
                output = redact_pdf(raw, target)
                st.session_state["result"] = output

        if st.session_state.get("result"):

            show_verification_result(
                raw,
                st.session_state["result"],
                [target],
                "manual"
            )

            st.download_button(
                "4. Download redacted PDF",
                data=st.session_state["result"],
                file_name="redacted.pdf",
                mime="application/pdf"
            )

    except Exception as error:
        st.error(f"Unable to process PDF: {error}")

# Part 6: Automatic detection
st.divider()
st.subheader("Automatic Sensitive Information Detection")

if uploaded is not None:

    raw = uploaded.getvalue()

    if len(raw) > 10 * 1024 * 1024:
        st.error("This prototype supports files up to 10 MB only.")
        st.stop()

    try:
        findings = detect_sensitive_info(raw)

        if not findings:
            st.info("No supported sensitive patterns detected.")

        else:
            labels = {
                item["value"]: (
                    f'{item["kind"]}: {item["value"]} '
                    f'({item["count"]} occurrences)'
                )
                for item in findings
            }

            selected = st.multiselect(
                "Select information to redact",
                options=list(labels.keys()),
                format_func=lambda value: labels[value]
            )

            # Prevent downloading results from an old selection
            selection_key = (
                hashlib.sha256(raw).hexdigest(),
                tuple(sorted(selected))
            )

            if st.session_state.get("auto_result_key") != selection_key:
                st.session_state.pop("auto_result", None)

            if st.button(
                "Redact Selected Information",
                disabled=not selected
            ):
                st.session_state.pop("auto_result", None)

                try:
                    output = raw

                    for value in selected:
                        output = redact_pdf(output, value)

                    st.session_state["auto_result"] = output
                    st.session_state["auto_result_key"] = selection_key

                except Exception as error:
                    st.error(f"Redaction failed: {error}")

            if (
                st.session_state.get("auto_result_key") == selection_key
                and st.session_state.get("auto_result") is not None
            ):
                show_verification_result(
                    raw,
                    st.session_state["auto_result"],
                    selected,
                    "automatic"
                )

                st.download_button(
                    "Download Automatically Redacted PDF",
                    data=st.session_state["auto_result"],
                    file_name="auto_redacted.pdf",
                    mime="application/pdf"
                )

    except Exception as error:
        st.error(f"Automatic detection failed: {error}")

