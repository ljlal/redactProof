
import hashlib
import pymupdf
import streamlit as st

st.set_page_config(
    page_title="RedactProof",
    page_icon="🔒"
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

        return doc.tobytes()


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
        with pymupdf.open(stream=raw, filetype="pdf") as doc:

            if doc.needs_pass:
                st.error("Password-protected PDFs are not supported.")
                st.stop()

            count = sum(
                len(page.search_for(target))
                for page in doc
            )

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

                    # Remove all matching text regions
                    for page in doc:
                        matches = page.search_for(target)

                        for rect in matches:
                            page.add_redact_annot(
                                rect,
                                fill=(0, 0, 0)
                            )

                        if matches:
                            page.apply_redactions()

                    output = doc.tobytes(
                        garbage=4,
                        deflate=True
                    )

                    # Part 4: Verify the exported PDF
                    with pymupdf.open(
                        stream=output,
                        filetype="pdf"
                    ) as checked:

                        remaining = sum(
                            len(page.search_for(target))
                            for page in checked
                        )

                    if remaining == 0:
                        st.session_state["result"] = output
                    else:
                        st.error(
                            "Verification failed. No download provided."
                        )

        # Part 5: Download the result
        if st.session_state.get("result"):

            st.success(
                "Verification passed: no matching searchable "
                "page text was found in the exported PDF."
            )

            st.download_button(
                "4. Download redacted PDF",
                data=st.session_state["result"],
                file_name="redacted.pdf",
                mime="application/pdf"
            )

    except Exception as error:
        st.error(f"Unable to process PDF: {error}")
