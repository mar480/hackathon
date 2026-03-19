import streamlit as st
from services.extraction_service import ExtractionResult


def render_extraction_result(result: ExtractionResult, default_filename: str):
    if result.ok:
        st.success("Extraction completed.")
    else:
        st.error("Extraction failed or produced no CSV output.")

    with st.expander("Arelle command output"):
        st.code(" ".join(result.run_result.command), language="bash")
        st.subheader("stdout")
        st.text(result.run_result.stdout or "(empty)")
        st.subheader("stderr")
        st.text(result.run_result.stderr or "(empty)")

    st.subheader("Preview")
    st.dataframe(result.dataframe, use_container_width=True)

    if result.csv_path.exists():
        st.download_button(
            "Download CSV",
            data=result.csv_path.read_bytes(),
            file_name=default_filename,
            mime="text/csv",
        )